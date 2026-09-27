import os
from datetime import datetime, timedelta
from pathlib import Path
import sqlite3
import jwt

DB_PATH = Path(os.getenv('EARTHLENS_DB_PATH', '/tmp/earthlens.db'))
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
JWT_SECRET = os.getenv('EARTHLENS_JWT_SECRET', 'earthlens-dev-secret-change-me')
JWT_ALGORITHM = 'HS256'
JWT_TTL_HOURS = 24


def _connect():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = _connect()
    conn.execute(
        '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    conn.commit()
    conn.close()


def _hash_password(password: str) -> str:
    import hashlib
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def create_user(name: str, email: str, password: str):
    name = (name or '').strip()
    email = (email or '').strip().lower()
    password = (password or '').strip()

    if not name:
        raise ValueError('Name is required.')
    if not email or '@' not in email:
        raise ValueError('Please provide a valid email address.')
    if len(password) < 6:
        raise ValueError('Password must be at least 6 characters long.')

    conn = _connect()
    try:
        existing = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        if existing:
            raise ValueError('An account with this email already exists.')

        cursor = conn.execute(
            'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
            (name, email, _hash_password(password)),
        )
        user_id = cursor.lastrowid
        conn.commit()
        return {'id': user_id, 'name': name, 'email': email}
    finally:
        conn.close()


def verify_user(email: str, password: str):
    email = (email or '').strip().lower()
    password_hash = _hash_password((password or '').strip())

    conn = _connect()
    try:
        user = conn.execute(
            'SELECT id, name, email FROM users WHERE email = ? AND password_hash = ?',
            (email, password_hash),
        ).fetchone()
        if not user:
            return None
        return dict(user)
    finally:
        conn.close()


def issue_token(user):
    payload = {
        'sub': str(user['id']),
        'email': user['email'],
        'name': user['name'],
        'exp': datetime.utcnow() + timedelta(hours=JWT_TTL_HOURS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def get_user_from_token(token: str):
    if not token:
        return None
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except Exception:
        return None

    conn = _connect()
    try:
        user = conn.execute(
            'SELECT id, name, email FROM users WHERE id = ?',
            (int(payload.get('sub')),),
        ).fetchone()
        if not user:
            return None
        return dict(user)
    finally:
        conn.close()
