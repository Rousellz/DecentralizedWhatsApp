# Dockerfile for Client
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# # Install dependencies and add iproute2 for `ip` command

# Copy all files into the container
COPY client/ /app

COPY client/client.sh /app

# Install dependencies from requirements.txt
RUN chmod +x /app/client.sh
RUN pip install --no-cache-dir -r /app/requirements.txt


# Expose the port Streamlit will run on
EXPOSE 8501

# Run routing.sh and then Streamlit client

CMD /app/client.sh