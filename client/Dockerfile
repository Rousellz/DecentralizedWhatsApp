# Dockerfile for Client
FROM python:3.11-buster

# Set the working directory in the container
WORKDIR /app


# Copy all files into the container
COPY client/ /app

COPY client/client.sh /app

# Update and install system dependencies
# RUN apk add --no-cache build-base cmake bash

# Install dependencies from requirements.txt
RUN chmod +x /app/client.sh
RUN pip install --no-cache-dir -r /app/requirements.txt


# Expose the port Streamlit will run on
EXPOSE 8501

# Run routing.sh and then Streamlit client

CMD /app/client.sh