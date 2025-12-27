import pytest
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """Test the /health endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}


def test_index_route(client):
    """Test the index route /."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"message": "Subtraction API. Use /subtract?a=<num>&b=<num>"}


def test_subtraction_success(client):
    """Test successful subtraction with integer inputs."""
    response = client.get('/subtract?a=15&b=5')
    assert response.status_code == 200
    assert response.json == {"a": 15.0, "b": 5.0, "result": 10.0}


def test_subtraction_with_floats(client):
    """Test successful subtraction with float inputs."""
    response = client.get('/subtract?a=10.5&b=2.2')
    assert response.status_code == 200
    assert response.json['result'] == pytest.approx(8.3)


def test_subtraction_with_negative_numbers(client):
    """Test subtraction with negative number inputs."""
    response = client.get('/subtract?a=-10&b=-5')
    assert response.status_code == 200
    assert response.json == {"a": -10.0, "b": -5.0, "result": -5.0}


def test_subtraction_missing_parameter(client):
    """Test subtraction endpoint with a missing parameter."""
    response = client.get('/subtract?a=10')
    assert response.status_code == 400
    assert "Missing required query parameters" in response.json['error']


def test_subtraction_invalid_parameter(client):
    """Test subtraction endpoint with a non-numeric parameter."""
    response = client.get('/subtract?a=ten&b=5')
    assert response.status_code == 400
    assert "Invalid input" in response.json['error']
