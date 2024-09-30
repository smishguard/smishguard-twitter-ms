from flask import Flask, request, jsonify
import tweepy
from dotenv import load_dotenv
import os
import random
import json

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

# Cargar los mensajes desde un archivo JSON
def cargar_mensajes():
    with open('./messages.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['messages']

# Cargar los mensajes una vez al iniciar la app
messages_templates = cargar_mensajes()

@app.route('/tweet', methods=['POST'])
def create_tweet():
    try:
        # Recibir el SMS del cuerpo de la solicitud
        data = request.json
        sms_message = data.get('sms', '')

        # Seleccionar un template al azar
        selected_template = random.choice(messages_templates)

        # Insertar el SMS en el template
        tweet_text = selected_template.replace("[MENSAJE AQUÍ]", sms_message)

        # Publicar el tweet
        response = cliente.create_tweet(text=tweet_text)

        # Devolver la respuesta de la API de Twitter
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Manejo de errores

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
