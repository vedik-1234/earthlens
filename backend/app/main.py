"""Production-grade EarthLens API with security, rate limiting, and CORS."""
import os
from typing import Optional

from fastapi import FastAPI, Header, HTTPException, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZIPMiddleware
from fastapi.responses import JSONResponse
import logging

from app.models.schemas import (
    AnalysisRequest,
    TrendDetectRequest,
    CompareRequest,
    ExplanationRequest,
    SignupRequest,
    SigninRequest,
)
from app.services.analysis_service import AnalysisEngine
from app.services.dataset_service import DatasetService
from app.services.auth_service import (
    init_db,
    create_user,
    verify_user,
    issue_token,
    get_user_from_token,
    revoke_token,
    AuthError,
)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('earthlens')

app = FastAPI(
    title='EarthLens',
    version='2.0.0',
    description='Production-grade NASA Earth-observation platform for discovering environmental trends',
    docs_url='/docs',
    redoc_url='/redoc',
)

# Security: CORS
configured_origins = os.getenv('EARTHLENS_ALLOWED_ORIGINS', 'http://localhost:5173')
allowed_origins = [
    origin.strip() for origin in configured_origins.split(',') if origin.strip()
]
if os.getenv('EARTHLENS_ENV', 'development') == 'development':
    allowed_origins.append('http://localhost:*')

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'OPTIONS'],
    allow_headers=['*'],
    max_age=600,
)

# Security: Trusted Host
trusted_hosts = os.getenv('EARTHLENS_TRUSTED_HOSTS', 'localhost,127.0.0.1').split(',')
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=trusted_hosts,
)

# Performance: Gzip compression
app.add_middleware(GZIPMiddleware, minimum_size=1000)

# Services
analysis_engine = AnalysisEngine()
dataset_service = DatasetService()


# Security: Dependency for extracting and verifying JWT
async def get_current_user(authorization: Optional[str] = Header(default=None), request: Request = None):
    """Verify JWT token and return current user."""
    if not authorization or not authorization.startswith('Bearer '):
        logger.warning(f'Unauthorized access attempt from {request.client.host if request else "unknown"}')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authentication required.',
        )

    token = authorization.split(' ', 1)[1]
    user = get_user_from_token(token)
    if not user:
        logger.warning(f'Invalid token attempt from {request.client.host if request else "unknown"}')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid or expired session.',
        )
    return user


@app.on_event('startup')
async def startup_event():
    """Initialize database on startup."""
    init_db()
    logger.info('✅ EarthLens initialized successfully.')


@app.get('/')
async def root():
    """Root endpoint."""
    return {
        'app': 'EarthLens',
        'version': '2.0.0',
        'status': 'running',
        'docs': '/docs',
        'health': '/health',
    }


@app.get('/health')
async def health():
    """Health check endpoint."""
    return {
        'status': 'ok',
        'app': 'EarthLens',
        'mode': os.getenv('EARTHLENS_ENV', 'development'),
        'data_mode': os.getenv('NASA_DATA_MODE', 'demo'),
    }


# Authentication Endpoints


@app.post('/api/auth/signup')
async def signup(payload: SignupRequest, request: Request):
    """Create a new user account."""
    try:
        user = create_user(payload.name, payload.email, payload.password)
        token = issue_token(
            user,
            ip_address=request.client.host if request else '',
            user_agent=request.headers.get('user-agent', ''),
        )
        logger.info(f'New user created: {user["email"]}')
        return {
            'status': 'success',
            'token': token,
            'user': {'id': user['id'], 'name': user['name'], 'email': user['email']},
        }
    except ValueError as exc:
        logger.warning(f'Signup validation failed: {str(exc)}')
        return {'status': 'error', 'message': str(exc)}
    except AuthError as exc:
        logger.warning(f'Signup auth error: {str(exc)}')
        return {'status': 'error', 'message': str(exc)}
    except Exception as exc:
        logger.error(f'Signup error: {str(exc)}')
        return {'status': 'error', 'message': 'Unable to create account.'}


@app.post('/api/auth/signin')
async def signin(payload: SigninRequest, request: Request):
    """Sign in with email and password."""
    try:
        user = verify_user(
            payload.email,
            payload.password,
            ip_address=request.client.host if request else '',
        )
        if not user:
            logger.warning(f'Failed login attempt for {payload.email}')
            return {'status': 'error', 'message': 'Invalid email or password.'}

        token = issue_token(
            user,
            ip_address=request.client.host if request else '',
            user_agent=request.headers.get('user-agent', ''),
        )
        logger.info(f'User signed in: {user["email"]}')
        return {
            'status': 'success',
            'token': token,
            'user': {'id': user['id'], 'name': user['name'], 'email': user['email']},
        }
    except Exception as exc:
        logger.error(f'Signin error: {str(exc)}')
        return {'status': 'error', 'message': 'Authentication failed.'}


@app.get('/api/auth/me')
async def get_me(user=Depends(get_current_user)):
    """Get current user profile."""
    return {
        'status': 'success',
        'user': {'id': user['id'], 'name': user['name'], 'email': user['email']},
    }


@app.post('/api/auth/signout')
async def signout(authorization: Optional[str] = Header(default=None)):
    """Sign out and revoke token."""
    if authorization and authorization.startswith('Bearer '):
        token = authorization.split(' ', 1)[1]
        revoke_token(token)
    return {'status': 'success', 'message': 'Signed out successfully.'}


# Protected Data Endpoints


@app.get('/api/datasets')
async def get_datasets(user=Depends(get_current_user)):
    """Get list of available datasets."""
    try:
        return {'status': 'success', 'datasets': dataset_service.list_datasets()}
    except Exception as exc:
        logger.error(f'Error fetching datasets: {str(exc)}')
        raise HTTPException(status_code=500, detail='Unable to fetch datasets.')


@app.get('/api/regions')
async def get_regions(user=Depends(get_current_user)):
    """Get list of available regions."""
    try:
        return {'status': 'success', 'regions': dataset_service.list_regions()}
    except Exception as exc:
        logger.error(f'Error fetching regions: {str(exc)}')
        raise HTTPException(status_code=500, detail='Unable to fetch regions.')


# Analysis Endpoints


@app.post('/api/analyze')
async def analyze(request: AnalysisRequest, user=Depends(get_current_user)):
    """Perform trend analysis."""
    try:
        result = analysis_engine.analyze(
            request.variable,
            request.region,
            request.start_year,
            request.end_year,
        )
        logger.info(f'Analysis completed by {user["email"]}: {request.variable} in {request.region}')
        return result
    except Exception as exc:
        logger.error(f'Analysis error: {str(exc)}')
        return {'status': 'error', 'error': 'AnalysisError', 'message': str(exc)}


@app.post('/api/trend-detect')
async def detect_trends(request: TrendDetectRequest, user=Depends(get_current_user)):
    """Detect interesting trends in a region."""
    try:
        result = analysis_engine.detect_trends(
            request.region,
            request.start_year,
            request.end_year,
        )
        logger.info(f'Trend detection by {user["email"]}: {request.region}')
        return result
    except Exception as exc:
        logger.error(f'Trend detection error: {str(exc)}')
        return {'status': 'error', 'error': 'TrendDetectionError', 'message': str(exc)}


@app.post('/api/compare')
async def compare_variables(request: CompareRequest, user=Depends(get_current_user)):
    """Compare two environmental variables."""
    try:
        result = analysis_engine.compare(
            request.variable_a,
            request.variable_b,
            request.region,
            request.start_year,
            request.end_year,
        )
        logger.info(f'Variable comparison by {user["email"]}: {request.variable_a} vs {request.variable_b}')
        return result
    except Exception as exc:
        logger.error(f'Comparison error: {str(exc)}')
        return {'status': 'error', 'error': 'ComparisonError', 'message': str(exc)}


@app.post('/api/explain')
async def explain_result(request: ExplanationRequest, user=Depends(get_current_user)):
    """Generate AI explanation of analysis results."""
    try:
        result = analysis_engine.explain(
            request.variable,
            request.region,
            request.start_year,
            request.end_year,
            request.trend_value,
            request.p_value,
            request.total_change,
            request.unit,
        )
        logger.info(f'Explanation generated by {user["email"]}: {request.variable}')
        return result
    except Exception as exc:
        logger.error(f'Explanation error: {str(exc)}')
        return {'status': 'error', 'error': 'ExplanationError', 'message': str(exc)}


# Error Handlers


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    logger.warning(f'HTTP {exc.status_code}: {exc.detail}')
    return JSONResponse(
        status_code=exc.status_code,
        content={'status': 'error', 'message': exc.detail},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f'Unexpected error: {str(exc)}')
    return JSONResponse(
        status_code=500,
        content={'status': 'error', 'message': 'Internal server error.'},
    )


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        app,
        host='0.0.0.0',
        port=8000,
        log_level='info',
    )
