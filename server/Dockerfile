# Dockerfile for Server
# This Dockerfile creates a container for the server that handles messaging logic using Flask

# Use the official Python image as a base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies and add iproute2 for `ip` command if needed
RUN apt-get update && apt-get install -y iproute2

# Copy the server files into the container
COPY server/ /app
# Install dependencies
# RUN pip install --upgrade pip
RUN pip install --no-cache-dir Flask
# RUN pip install --upgrade werkzeug  # Asegúrate de instalar la versión más reciente de werkzeug

# Expose the port Flask will run on
EXPOSE 5001

# Set the environment variable to ensure output is not buffered
ENV PYTHONUNBUFFERED=1

# Run the Flask server
CMD ["python", "server.py"]
