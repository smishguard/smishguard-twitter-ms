import unittest
from unittest.mock import patch, Mock
from app import app, verificar_bancos  # Importar app y función de verificación de bancos
import json

class APITestCase(unittest.TestCase):
    # Configuración inicial
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Prueba para el endpoint /ping
    def test_ping(self):
        response = self.app.get('/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "pong"})

    # Prueba para el endpoint /tweet
    @patch('app.cliente.create_tweet')
    def test_create_tweet(self, mock_create_tweet):
        # Simula la respuesta de Twitter API
        mock_response = Mock()
        mock_response.data = {"id": "12345", "text": "Mock tweet"}
        mock_create_tweet.return_value = mock_response

        # Define los datos de prueba
        data = {
            "sms": "Alerta de fraude de Bancolombia"
        }
        response = self.app.post('/tweet', data=json.dumps(data),
                                 content_type='application/json')

        # Verifica que la API respondió correctamente
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json)  # Comprueba que hay un ID en la respuesta

        # Verifica que la función create_tweet se llamó una vez
        mock_create_tweet.assert_called_once()

    # Prueba para la función verificar_bancos
    def test_verificar_bancos(self):
        sms_message = "El banco BBVA le informa de un posible fraude"
        etiquetas = verificar_bancos(sms_message)
        self.assertIn("@BBVA_Colombia", etiquetas)
        self.assertIn("@caivirtual", etiquetas)

        sms_message2 = "Notificación del banco Davivienda"
        etiquetas2 = verificar_bancos(sms_message2)
        self.assertIn("@Davivienda", etiquetas2)
        self.assertIn("@caivirtual", etiquetas2)

        sms_message3 = "Mensaje sin banco mencionado"
        etiquetas3 = verificar_bancos(sms_message3)
        self.assertEqual(etiquetas3, "@caivirtual")  # Solo debe incluir @caivirtual

if __name__ == '__main__':
    unittest.main()
