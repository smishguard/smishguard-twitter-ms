# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos requeridos
COPY app.py /app/app.py
#COPY .env /app/.env

# Instala las dependencias
RUN pip install flask tweepy python-dotenv

# Expone el puerto en el que la aplicación correrá
EXPOSE 5000

# Define el comando para correr la aplicación
CMD ["python", "app.py"]
