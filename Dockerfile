# Usa una imagen base de Python
FROM python:3.14.0a1-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos requeridos
COPY app.py /app/app.py
COPY requirements.txt /app/requirements.txt


# Instala las dependencias desde requirements.txt
RUN pip install -r /app/requirements.txt

# Expone el puerto en el que la aplicación correrá
EXPOSE 5000

# Define el comando para correr la aplicación
CMD ["python", "app.py"]
