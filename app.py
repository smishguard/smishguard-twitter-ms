from flask import Flask, request, jsonify
import tweepy
from dotenv import load_dotenv
import os
import random
from flask_cors import CORS
import re  # Para usar expresiones regulares y buscar nombres de bancos

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
CORS(app)

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

# Diccionario de bancos colombianos y sus etiquetas
bancos_colombianos = {
    "bancolombia": "@Bancolombia",
    "davivienda": "@Davivienda",
    "banco de bogota": "@BancoDeBogota",
    "banco popular": "@PopularColombia",
    "banco de occidente": "@Bco_Occidente",
    "bbva": "@BBVA_Colombia",
    "scotiabank colpatria": "@scotiabank_co",
    "banco caja social": "@BancoCajaSocial",
    "itau": "@Itaú",
    "citibank": "@Citibank",
    "nequi": "@Nequi",
    "daviplata": "@Davivienda",
}

# Lista de mensajes predefinidos
mensajes = [
    "⚠️ Alerta de smishing ⚠️ Mensajes como '[MENSAJE AQUÍ]' buscan estafarte. ¡No caigas! #Ciberseguridad",
    "🚨 Cuidado con el fraude 🚨 Si ves un SMS diciendo: '[MENSAJE AQUÍ]', ignóralo. #ProtegeTuInfo",
    "🛑 Alerta 🛑 Recibiste un mensaje que dice: '[MENSAJE AQUÍ]'? ¡No hagas clic! #EstafaSMS",
    "🔒 Protege tus datos 🔒 Mensajes como '[MENSAJE AQUÍ]' son intentos de estafa. #SeguridadDigital",
    "⚠️ Estafa detectada ⚠️ Un SMS diciendo '[MENSAJE AQUÍ]' es fraude. No des tu info. #Cuídate",
]

# Función para verificar y agregar etiquetas de bancos
def verificar_bancos(sms_message):
    etiquetas = "@caivirtual"
    for banco, etiqueta in bancos_colombianos.items():
        if re.search(rf"\b{banco}\b", sms_message, re.IGNORECASE):
            etiquetas += f" {etiqueta}"
    return etiquetas

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

        # Agrega etiquetas de bancos si se menciona alguno
        etiquetas = verificar_bancos(sms_message)
        tweet_text += f" {etiquetas}"

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
