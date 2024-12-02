# Dockerfile for Client
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies and add iproute2 for `ip` command
RUN apt-get update && apt-get install -y iproute2 curl

# Copy all files into the container
COPY client/ /app

# Update pip to the latest version
RUN pip install --upgrade pip

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Make routing.sh executable (assuming routing.sh is included in the copy above)
RUN chmod +x /app/routing.sh

# Expose the port Streamlit will run on
EXPOSE 8501

# Run routing.sh and then Streamlit client
CMD ["/bin/sh", "-c", "/app/routing.sh && streamlit run client.py --server.port=8501 --server.enableCORS=false"]
