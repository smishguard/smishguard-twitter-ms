import unittest
from unittest.mock import patch, Mock
from app import app, verificar_bancos  # Importar app y función de verificación de bancos
import json

class APITestCase(unittest.TestCase):
    # Configuración inicial para el cliente de prueba de Flask
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
        self.assertIn("id", response.json)  # Comprueba que la respuesta contiene un ID
        self.assertIn("text", response.json)  # Comprueba que la respuesta contiene el texto del tweet

        # Verifica que la función create_tweet se llamó una vez con el texto del tweet
        mock_create_tweet.assert_called_once()
        called_args = mock_create_tweet.call_args[1]
        self.assertIn("Alerta de fraude de Bancolombia", called_args['text'])

    # Prueba para el caso en que no se proporciona un mensaje SMS en /tweet
    def test_create_tweet_no_sms(self):
        data = {}  # No se proporciona el campo 'sms'
        response = self.app.post('/tweet', data=json.dumps(data),
                                 content_type='application/json')

        # Verifica que responde con un error 400
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'No se proporcionó ningún mensaje SMS'})

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
        self.assertEqual(etiquetas3, "@caivirtual")  # Solo debe incluir @caivirtual si no se menciona ningún banco

if __name__ == '__main__':
    unittest.main()
