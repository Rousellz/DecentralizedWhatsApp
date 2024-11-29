# Usamos la imagen local cp4 como base
FROM python:3.11-buster

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /

# Copiamos el archivo requirements.txt (si lo tienes) al contenedor
COPY requirements.txt requirements.txt
COPY . .
# Instalamos las dependencias listadas en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Exponemos el puerto en el que correrá la aplicación Flask
EXPOSE 8001

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]