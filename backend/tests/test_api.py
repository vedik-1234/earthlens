import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.analysis_service import AnalysisEngine

client = TestClient(app)


def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_dataset_and_region_metadata():
    datasets = client.get('/api/datasets').json()
    regions = client.get('/api/regions').json()
    assert {item['id'] for item in datasets['datasets']} == {'temperature', 'precipitation', 'vegetation'}
    assert 'global' in regions['regions']


def test_analysis_result_is_reproducible_and_statistical():
    payload = {'variable': 'temperature', 'region': 'global', 'start_year': 2003, 'end_year': 2025}
    first = client.post('/api/analyze', json=payload).json()
    second = client.post('/api/analyze', json=payload).json()
    assert first['status'] == 'success'
    assert first == second
    assert first['sample_size'] == 23
    assert len(first['confidence_interval']) == 2
    assert 0 <= first['p_value'] <= 1
    assert first['statistically_significant'] == (first['p_value'] < first['significance_threshold'])


def test_invalid_requests_are_explained():
    invalid_years = client.post('/api/analyze', json={'variable': 'temperature', 'region': 'global', 'start_year': 2025, 'end_year': 2003}).json()
    invalid_region = client.post('/api/analyze', json={'variable': 'temperature', 'region': 'not-a-region', 'start_year': 2003, 'end_year': 2025}).json()
    assert invalid_years['status'] == 'error'
    assert 'time range' in invalid_years['message'].lower()
    assert invalid_region['status'] == 'error'
    assert 'region' in invalid_region['message'].lower()


def test_detector_compare_and_explanation():
    detector = client.post('/api/trend-detect', json={'region': 'global', 'start_year': 2003, 'end_year': 2025}).json()
    comparison = client.post('/api/compare', json={'variable_a': 'temperature', 'variable_b': 'precipitation', 'region': 'global', 'start_year': 2003, 'end_year': 2025}).json()
    explanation = client.post('/api/explain', json={'variable': 'temperature', 'region': 'global', 'start_year': 2003, 'end_year': 2025, 'trend_value': 0.03, 'p_value': 0.01, 'total_change': 0.7, 'unit': '°C/year'}).json()
    assert detector['status'] == 'success' and len(detector['results']) == 3
    assert comparison['status'] == 'success'
    assert 'correlation' in comparison['association']
    assert explanation['status'] == 'success'
    assert len(explanation['segments']) >= 4


def test_linear_regression_known_values():
    engine = AnalysisEngine()
    result = engine._analyze_linear_trend([2000, 2001, 2002, 2003], [1, 2, 3, 4], 'temperature')
    assert result['slope'] == pytest.approx(1.0)
    assert result['r_squared'] == pytest.approx(1.0)
    assert result['p_value'] < 0.05
