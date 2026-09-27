from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel

from app.models.schemas import AnalysisRequest, TrendDetectRequest, CompareRequest, ExplanationRequest, SignupRequest, SigninRequest
from app.services.analysis_service import AnalysisEngine
from app.services.dataset_service import DatasetService
from app.services.auth_service import init_db, create_user, verify_user, issue_token, get_user_from_token

app = FastAPI(
    title='EarthLens',
    version='1.0.0',
    description='Interactive NASA Earth-observation platform for discovering environmental trends',
    docs_url='/docs',
    redoc_url='/redoc',
)

configured_origins = os.getenv('EARTHLENS_ALLOWED_ORIGINS', 'http://localhost:5173')
allowed_origins = [origin.strip() for origin in configured_origins.split(',') if origin.strip()]
if os.getenv('EARTHLENS_ENV', 'development') == 'development':
    allowed_origins.append('*')

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

analysis_engine = AnalysisEngine()
dataset_service = DatasetService()

@app.on_event('startup')
async def startup_event():
    init_db()


async def get_current_user(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='Authentication required.')

    token = authorization.split(' ', 1)[1]
    user = get_user_from_token(token)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid or expired session.')
    return user


@app.get('/')
def root():
    return {'app': 'EarthLens', 'version': '1.0.0', 'docs': '/docs', 'health': '/health'}


@app.get('/health')
def health():
    return {
        'status': 'ok',
        'app': 'EarthLens',
        'mode': os.getenv('NASA_DATA_MODE', 'demo'),
        'message': 'EarthLens backend is running.',
    }


@app.post('/api/auth/signup')
def signup(payload: SignupRequest):
    try:
        user = create_user(payload.name, payload.email, payload.password)
        token = issue_token(user)
        return {'status': 'success', 'token': token, 'user': {'id': user['id'], 'name': user['name'], 'email': user['email']}}
    except ValueError as exc:
        return {'status': 'error', 'message': str(exc)}


@app.post('/api/auth/signin')
def signin(payload: SigninRequest):
    user = verify_user(payload.email, payload.password)
    if not user:
        return {'status': 'error', 'message': 'Invalid email or password.'}
    token = issue_token(user)
    return {'status': 'success', 'token': token, 'user': {'id': user['id'], 'name': user['name'], 'email': user['email']}}


@app.get('/api/auth/me')
def get_me(user=Depends(get_current_user)):
    return {'status': 'success', 'user': {'id': user['id'], 'name': user['name'], 'email': user['email']}}


@app.get('/api/datasets')
def get_datasets(user=Depends(get_current_user)):
    return {'status': 'success', 'datasets': dataset_service.list_datasets()}


@app.get('/api/regions')
def get_regions(user=Depends(get_current_user)):
    return {'status': 'success', 'regions': dataset_service.list_regions()}


@app.post('/api/analyze')
def analyze(request: AnalysisRequest, user=Depends(get_current_user)):
    try:
        return analysis_engine.analyze(request.variable, request.region, request.start_year, request.end_year)
    except Exception as exc:
        return {'status': 'error', 'error': 'AnalysisError', 'message': str(exc)}


@app.post('/api/trend-detect')
def detect_trends(request: TrendDetectRequest, user=Depends(get_current_user)):
    try:
        return analysis_engine.detect_trends(request.region, request.start_year, request.end_year)
    except Exception as exc:
        return {'status': 'error', 'error': 'TrendDetectionError', 'message': str(exc)}


@app.post('/api/compare')
def compare_variables(request: CompareRequest, user=Depends(get_current_user)):
    try:
        return analysis_engine.compare(request.variable_a, request.variable_b, request.region, request.start_year, request.end_year)
    except Exception as exc:
        return {'status': 'error', 'error': 'ComparisonError', 'message': str(exc)}


@app.post('/api/explain')
def explain_result(request: ExplanationRequest, user=Depends(get_current_user)):
    try:
        return analysis_engine.explain(request.variable, request.region, request.start_year, request.end_year, request.trend_value, request.p_value, request.total_change, request.unit)
    except Exception as exc:
        return {'status': 'error', 'error': 'ExplanationError', 'message': str(exc)}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
