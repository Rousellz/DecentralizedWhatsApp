FROM python:3.11-slim

RUN pip install typer fastapi uvicorn sqlalchemy requests pydantic typing
RUN apt-get update && apt-get install -y iproute2 iptables iputils-ping && rm -rf /var/lib/apt/lists/*
WORKDIR /home/app

COPY . /home/app
COPY server.sh /home/app

RUN chmod +x /home/app/server.sh

EXPOSE 8030

ENTRYPOINT ["sh", "/home/app/server.sh"]
CMD ["first-server"]
# CMD ["sh", "-c", "/home/app/server.sh"]
# CMD ["python", "/home/app/server_app.py", "first-server"]