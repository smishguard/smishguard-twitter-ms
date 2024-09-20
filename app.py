from flask import Flask, request, jsonify
import tweepy
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

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

@app.route('/tweet', methods=['POST'])
def create_tweet():
    try:
        data = request.json  # Recibe los datos JSON del cuerpo de la solicitud
        text = data.get('text', '')  # Extrae el texto del tweet
        response = cliente.create_tweet(text=text)  # Publica el tweet
        return jsonify(response.data), 200  # Devuelve la respuesta de la API de Twitter
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Manejo de errores

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
