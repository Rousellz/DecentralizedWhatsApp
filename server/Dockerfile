# # Dockerfile for Server
# # This Dockerfile creates a container for the server that handles messaging logic using Flask

# # Use the official Python image as a base
FROM python:3.9-slim
# FROM image_server

# # Set the working directory in the container
WORKDIR /app

RUN apt-get update && apt-get install -y iproute2
# # Copy the server files into the container
COPY server/ /app

COPY server/server.sh /app

RUN chmod +x /app/server.sh

RUN pip install --no-cache-dir Flask

# # Expose the port Flask will run on
EXPOSE 5000

# # Set the environment variable to ensure output is not buffered
ENV PYTHONUNBUFFERED=1

# # Run the Flask server
CMD /app/server.sh && python server.py