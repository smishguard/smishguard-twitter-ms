from flask import Flask, request, jsonify
import tweepy
from dotenv import load_dotenv
import os
import random
from flask_cors import CORS  # Importa CORS

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

# Definimos las variables que nos identifican junto con nuestra app
api_key = os.getenv('API_KEY')
api_key_secret = os.getenv('API_KEY_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
bearer_token = os.getenv('BEARER_TOKEN')

# Creamos un cliente tweepy
cliente = tweepy.Client(bearer_token=bearer_token,
                        consumer_key=api_key,
                        consumer_secret=api_key_secret,
                        access_token=access_token,
                        access_token_secret=access_token_secret)

# Lista de mensajes predefinidos
mensajes = [
    "🛑 Cuidado con este SMS fraudulento 🛑 Si recibes un mensaje diciendo: '[MENSAJE AQUÍ]', ¡no hagas clic! Es una estafa. #Smishing #ProtegeTuInformación",
    "🛑 Nuevo smishing detectado 🛑 Si ves un SMS que dice: '[MENSAJE AQUÍ]', ¡ignóralo! No compartas información personal. #FraudeSMS #Ciberseguridad",
    "🛑 Atención: Smishing en curso 🛑 Mensajes como '[MENSAJE AQUÍ]' son intentos de estafa. ¡No caigas en la trampa! #ProtegeTusDatos #Ciberseguridad",
    "🛑 Alerta de smishing 🛑 Recibiste un mensaje que dice: '[MENSAJE AQUÍ]'? No hagas clic, es un fraude para robar tu información. #Ciberseguridad #FraudeSMS",
    "🛑 Nuevo intento de estafa 🛑 Si te llega un SMS como '[MENSAJE AQUÍ]', ¡es un fraude! No proporciones datos personales. #ProtegeTuMóvil #Ciberseguridad",
    "🛑 Smishing en acción 🛑 Si ves un mensaje diciendo: '[MENSAJE AQUÍ]', no hagas clic. ¡Es una estafa! #FraudeSMS #ProtecciónDigital",
    "🛑 Cuidado con este mensaje 🛑 '[MENSAJE AQUÍ]' es un intento de smishing. No sigas el enlace. #Ciberseguridad #ProtegeTuInformación",
    "🛑 Advertencia: Smishing 🛑 Si recibes un SMS diciendo: '[MENSAJE AQUÍ]', no hagas clic. Es un fraude. #Ciberseguridad #FraudeSMS"
]

@app.route('/tweet', methods=['POST'])
def create_tweet():
    try:
        # Recibe los datos JSON del cuerpo de la solicitud
        data = request.json
        sms_message = data.get('sms', '')  # Extrae el mensaje SMS
        
        if not sms_message:
            return jsonify({'error': 'No se proporcionó ningún mensaje SMS'}), 400

        # Selecciona un mensaje aleatorio de la lista
        mensaje_aleatorio = random.choice(mensajes)
        
        # Inserta el mensaje SMS en el texto del tweet
        tweet_text = mensaje_aleatorio.replace('[MENSAJE AQUÍ]', sms_message)

        # Publica el tweet
        response = cliente.create_tweet(text=tweet_text)

        # Devuelve la respuesta de la API de Twitter
        return jsonify(response.data), 200

    except Exception as e:
        # Manejo de errores
        return jsonify({'error': str(e)}), 500

@app.route("/ping")
def ping():
    return jsonify({"message": "pong"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
