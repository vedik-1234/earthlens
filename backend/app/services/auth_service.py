"""Production-grade authentication service with security best practices."""
import os
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any

import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

DB_PATH = Path(os.getenv('EARTHLENS_DB_PATH', '/tmp/earthlens.db'))
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

JWT_SECRET = os.getenv('EARTHLENS_JWT_SECRET')
if not JWT_SECRET or JWT_SECRET == 'earthlens-dev-secret-change-me':
    import secrets
    JWT_SECRET = os.getenv('EARTHLENS_JWT_SECRET', secrets.token_urlsafe(32))
    print(f"⚠️  WARNING: No JWT_SECRET set. Generated: {JWT_SECRET}")
    print("    Set EARTHLENS_JWT_SECRET environment variable for production.")

JWT_ALGORITHM = 'HS256'
JWT_TTL_HOURS = int(os.getenv('EARTHLENS_JWT_TTL_HOURS', 24))
REFRESH_TTL_DAYS = int(os.getenv('EARTHLENS_REFRESH_TTL_DAYS', 7))

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto', bcrypt__rounds=12)


class AuthError(Exception):
    """Base authentication error."""
    pass


class InvalidCredentialsError(AuthError):
    """Raised when credentials are invalid."""
    pass


class DuplicateUserError(AuthError):
    """Raised when trying to create a duplicate user."""
    pass


class PasswordValidationError(AuthError):
    """Raised when password does not meet requirements."""
    pass


def _connect() -> sqlite3.Connection:
    """Get database connection with row factory."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize database with secure schema."""
    conn = _connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE COLLATE NOCASE,
            password_hash TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            email_verified BOOLEAN DEFAULT 0,
            failed_login_attempts INTEGER DEFAULT 0,
            locked_until TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL,
            ip_address TEXT,
            user_agent TEXT,
            status TEXT DEFAULT 'success',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token_jti TEXT NOT NULL UNIQUE,
            ip_address TEXT,
            user_agent TEXT,
            expires_at TIMESTAMP NOT NULL,
            revoked BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
        CREATE INDEX IF NOT EXISTS idx_sessions_jti ON sessions(token_jti);
        CREATE INDEX IF NOT EXISTS idx_audit_user_id ON audit_logs(user_id);
        CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
        """
    )

    conn.commit()
    conn.close()


def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against bcrypt hash."""
    return pwd_context.verify(plain_password, hashed_password)


def validate_password(password: str) -> None:
    """Validate password meets security requirements."""
    if len(password) < 8:
        raise PasswordValidationError('Password must be at least 8 characters long.')
    if not any(c.isupper() for c in password):
        raise PasswordValidationError('Password must contain at least one uppercase letter.')
    if not any(c.islower() for c in password):
        raise PasswordValidationError('Password must contain at least one lowercase letter.')
    if not any(c.isdigit() for c in password):
        raise PasswordValidationError('Password must contain at least one digit.')
    if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
        raise PasswordValidationError('Password must contain at least one special character.')


def create_user(
    name: str,
    email: str,
    password: str,
) -> Dict[str, Any]:
    """Create a new user with security validations."""
    name = (name or '').strip()
    email = (email or '').strip().lower()
    password = (password or '').strip()

    # Validation
    if not name or len(name) < 2:
        raise ValueError('Name must be at least 2 characters.')
    if not email or '@' not in email:
        raise ValueError('Please provide a valid email address.')
    if len(email) > 254:
        raise ValueError('Email address is too long.')

    try:
        validate_password(password)
    except PasswordValidationError as e:
        raise ValueError(str(e))

    conn = _connect()
    try:
        # Check for duplicates
        existing = conn.execute(
            'SELECT id FROM users WHERE email = ?',
            (email,),
        ).fetchone()
        if existing:
            raise DuplicateUserError('An account with this email already exists.')

        password_hash = hash_password(password)
        cursor = conn.execute(
            'INSERT INTO users (name, email, password_hash, is_active) VALUES (?, ?, ?, 1)',
            (name, email, password_hash),
        )
        user_id = cursor.lastrowid
        conn.commit()

        _log_audit(
            conn,
            user_id=user_id,
            action='USER_CREATED',
            status='success',
        )

        return {'id': user_id, 'name': name, 'email': email}
    finally:
        conn.close()


def verify_user(email: str, password: str, ip_address: str = '') -> Optional[Dict[str, Any]]:
    """Verify user credentials with rate limiting and logging."""
    email = (email or '').strip().lower()

    conn = _connect()
    try:
        user = conn.execute(
            'SELECT id, name, email, password_hash, is_active, locked_until FROM users WHERE email = ?',
            (email,),
        ).fetchone()

        if not user:
            _log_audit(
                conn,
                user_id=None,
                action='LOGIN_FAILED_INVALID_EMAIL',
                ip_address=ip_address,
                status='failed',
            )
            return None

        user_dict = dict(user)

        # Check if account is active
        if not user_dict.get('is_active'):
            _log_audit(
                conn,
                user_id=user_dict['id'],
                action='LOGIN_FAILED_INACTIVE',
                ip_address=ip_address,
                status='failed',
            )
            return None

        # Check if account is locked
        locked_until = user_dict.get('locked_until')
        if locked_until:
            locked_until_dt = datetime.fromisoformat(locked_until)
            if datetime.utcnow() < locked_until_dt:
                _log_audit(
                    conn,
                    user_id=user_dict['id'],
                    action='LOGIN_FAILED_LOCKED',
                    ip_address=ip_address,
                    status='failed',
                )
                return None
            else:
                # Unlock account
                conn.execute(
                    'UPDATE users SET locked_until = NULL, failed_login_attempts = 0 WHERE id = ?',
                    (user_dict['id'],),
                )

        # Verify password
        if not verify_password(password, user_dict['password_hash']):
            failed_attempts = (user_dict.get('failed_login_attempts') or 0) + 1
            lock_time = None

            # Lock account after 5 failed attempts for 30 minutes
            if failed_attempts >= 5:
                lock_time = (datetime.utcnow() + timedelta(minutes=30)).isoformat()
                _log_audit(
                    conn,
                    user_id=user_dict['id'],
                    action='ACCOUNT_LOCKED',
                    ip_address=ip_address,
                    status='failed',
                )
            else:
                _log_audit(
                    conn,
                    user_id=user_dict['id'],
                    action='LOGIN_FAILED_INVALID_PASSWORD',
                    ip_address=ip_address,
                    status='failed',
                )

            update_query = 'UPDATE users SET failed_login_attempts = ?'
            params = [failed_attempts]
            if lock_time:
                update_query += ', locked_until = ?'
                params.append(lock_time)
            update_query += ' WHERE id = ?'
            params.append(user_dict['id'])

            conn.execute(update_query, params)
            conn.commit()
            return None

        # Successful login
        conn.execute(
            'UPDATE users SET failed_login_attempts = 0, locked_until = NULL WHERE id = ?',
            (user_dict['id'],),
        )
        _log_audit(
            conn,
            user_id=user_dict['id'],
            action='LOGIN_SUCCESS',
            ip_address=ip_address,
            status='success',
        )
        conn.commit()

        return {'id': user_dict['id'], 'name': user_dict['name'], 'email': user_dict['email']}
    finally:
        conn.close()


def issue_token(
    user: Dict[str, Any],
    ip_address: str = '',
    user_agent: str = '',
) -> str:
    """Issue JWT token with session tracking."""
    import uuid

    jti = str(uuid.uuid4())
    exp_time = datetime.utcnow() + timedelta(hours=JWT_TTL_HOURS)

    payload = {
        'sub': str(user['id']),
        'email': user['email'],
        'name': user['name'],
        'jti': jti,
        'exp': exp_time,
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    # Store session in database
    conn = _connect()
    try:
        conn.execute(
            'INSERT INTO sessions (user_id, token_jti, ip_address, user_agent, expires_at) VALUES (?, ?, ?, ?, ?)',
            (user['id'], jti, ip_address, user_agent, exp_time.isoformat()),
        )
        conn.commit()
    finally:
        conn.close()

    return token


def get_user_from_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify and decode token, check if session is valid."""
    if not token:
        return None

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except Exception:
        return None

    jti = payload.get('jti')
    user_id = payload.get('sub')

    if not jti or not user_id:
        return None

    conn = _connect()
    try:
        # Check if session is valid and not revoked
        session = conn.execute(
            'SELECT id FROM sessions WHERE user_id = ? AND token_jti = ? AND revoked = 0',
            (int(user_id), jti),
        ).fetchone()

        if not session:
            return None

        # Get user info
        user = conn.execute(
            'SELECT id, name, email, is_active FROM users WHERE id = ? AND is_active = 1',
            (int(user_id),),
        ).fetchone()

        if not user:
            return None

        return dict(user)
    finally:
        conn.close()


def revoke_token(token: str) -> bool:
    """Revoke a token by marking its session as revoked."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except Exception:
        return False

    jti = payload.get('jti')
    if not jti:
        return False

    conn = _connect()
    try:
        conn.execute(
            'UPDATE sessions SET revoked = 1 WHERE token_jti = ?',
            (jti,),
        )
        conn.commit()
        return True
    finally:
        conn.close()


def _log_audit(
    conn: sqlite3.Connection,
    user_id: Optional[int] = None,
    action: str = '',
    ip_address: str = '',
    user_agent: str = '',
    status: str = 'success',
) -> None:
    """Log audit event to database."""
    conn.execute(
        'INSERT INTO audit_logs (user_id, action, ip_address, user_agent, status) VALUES (?, ?, ?, ?, ?)',
        (user_id, action, ip_address, user_agent, status),
    )
