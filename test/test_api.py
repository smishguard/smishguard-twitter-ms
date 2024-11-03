import pytest
from app import app

# Fixture de prueba para crear un cliente de prueba Flask
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Prueba del endpoint /ping
def test_ping(client):
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json == {"message": "pong"}

# Prueba del endpoint /tweet
def test_create_tweet(client, mocker):
    # Simula la respuesta de Twitter API
    mock_create_tweet = mocker.patch('app.cliente.create_tweet')
    mock_create_tweet.return_value.data = {"id": "12345", "text": "Mock tweet"}

    # Datos de prueba para el SMS
    data = {"sms": "Alerta de fraude en Bancolombia"}
    response = client.post("/tweet", json=data)

    # Verificaciones de la respuesta
    assert response.status_code == 200
    assert "id" in response.json

    # Verifica que se llamó a la función create_tweet
    mock_create_tweet.assert_called_once_with(text=pytest.anything())

# Prueba para verificar la falta de mensaje SMS en /tweet
def test_create_tweet_no_sms(client):
    data = {}  # No se proporciona el campo sms
    response = client.post("/tweet", json=data)
    
    # Verifica que responde con un error 400
    assert response.status_code == 400
    assert response.json == {'error': 'No se proporcionó ningún mensaje SMS'}
