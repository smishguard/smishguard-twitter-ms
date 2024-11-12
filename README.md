# SmishGuard Twitter Microservice

Este microservicio está diseñado para detectar y alertar sobre posibles mensajes de smishing (estafas de SMS) relacionados con bancos en Colombia. Cuando se envía un mensaje sospechoso al endpoint `/tweet`, el servicio selecciona un mensaje de advertencia predefinido, agrega etiquetas de bancos mencionados en el mensaje y publica el tweet a través de la API de Twitter.

## Requisitos Previos

- Python 3.7 o superior
- Una cuenta de Twitter con acceso a la API y las credenciales correspondientes (API Key, API Secret Key, Access Token, Access Token Secret, y Bearer Token)

## Instalación

1. Clona este repositorio:

    ```bash
    git clone https://github.com/tu_usuario/smishguard-twitter-ms.git
    cd smishguard-twitter-ms
    ```

2. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

3. Configuración:

    Crea un archivo `.env` en el directorio raíz del proyecto para almacenar las credenciales de la API de Twitter. El archivo `.env` debe contener las siguientes variables:

    ```plaintext
    API_KEY=tu_api_key
    API_KEY_SECRET=tu_api_key_secret
    ACCESS_TOKEN=tu_access_token
    ACCESS_TOKEN_SECRET=tu_access_token_secret
    BEARER_TOKEN=tu_bearer_token
    ```

    Asegúrate de que las credenciales de Twitter son correctas y tienen los permisos adecuados para publicar tweets.

## Uso

Para ejecutar el servicio Flask, ejecuta el siguiente comando en el directorio raíz del proyecto:

```bash
python app.py
```

Esto iniciará el servidor en `http://localhost:5000`.

## Endpoints

### GET /ping

Este endpoint es una prueba simple para verificar si el servicio está en funcionamiento.

- **Respuesta:** `{ "message": "pong" }`
- **Código de Estado:** `200 OK`

**Ejemplo de Solicitud:**

```bash
curl http://localhost:5000/ping
```

### POST /tweet

Este endpoint recibe un mensaje SMS sospechoso en formato JSON y publica un tweet con una advertencia sobre smishing, incluyendo etiquetas de los bancos mencionados en el mensaje.

- **URL:** `/tweet`
- **Método:** `POST`
- **Formato de Datos:** `JSON`
- **Datos de Entrada:**
  - `sms` (string, obligatorio): El mensaje SMS sospechoso que se desea analizar y publicar en Twitter.

- **Respuesta:** Datos del tweet publicado si es exitoso, o un mensaje de error en caso de fallo.

- **Códigos de Estado:**
  - `200 OK`: Si el tweet se publicó con éxito.
  - `400 Bad Request`: Si no se proporcionó el campo `sms`.
  - `500 Internal Server Error`: Si ocurrió algún error interno en el servicio.

**Ejemplo de Solicitud:**

```bash
curl -X POST http://localhost:5000/tweet -H "Content-Type: application/json" -d "{\"sms\":\"Alerta de fraude en Bancolombia\"}"
```

**Ejemplo de Respuesta Exitosa:**

```json
{
  "id": "1234567890123456789",
  "text": "⚠️ Alerta de smishing ⚠️ Mensajes como 'Alerta de fraude en Bancolombia' buscan estafarte. ¡No caigas! #Ciberseguridad @caivirtual @Bancolombia"
}
```

**Ejemplo de Respuesta con Error:**

```json
{
  "error": "No se proporcionó ningún mensaje SMS"
}
```

## Pruebas

Este servicio incluye pruebas unitarias para verificar el funcionamiento de los endpoints y de la función `verificar_bancos`.

### Ejecución de Pruebas

Asegúrate de estar en el directorio raíz del proyecto.

Ejecuta las pruebas usando `pytest`:

```bash
pytest
```

Las pruebas verifican:

- Que el endpoint `/ping` responda correctamente.
- Que el endpoint `/tweet` publique un tweet correctamente y maneje errores adecuadamente.
- Que la función `verificar_bancos` detecte correctamente los nombres de bancos en el mensaje SMS y añada las etiquetas correspondientes.
## Despliegue en Render
Este servicio está desplegado en Render. Al realizar una solicitud a cualquiera de los endpoints documentados, asegúrate de usar la URL de despliegue proporcionada por Render.

La API está disponible en: https://smishguard-twitter-ms.onrender.com.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT.