# Dockerfile for Client
# This Dockerfile creates a container for the client that runs the Streamlit front end

# Use the official Python image as a base
FROM python:3.11-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the client files into the container
COPY client/ /app

# Install dependencies
RUN pip install --no-cache-dir streamlit requests

# Expose the port Streamlit will run on
EXPOSE 8501

# Run the Streamlit client
CMD ["streamlit", "run", "client.py", "--server.port=8501", "--server.enableCORS=false"]