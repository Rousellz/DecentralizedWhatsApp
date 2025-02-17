FROM python:3.12-slim

RUN pip install typer fastapi uvicorn sqlalchemy requests pydantic typing

RUN mkdir -p /home/app

RUN apt-get update && apt-get install -y iproute2 iptables iputils-ping && rm -rf /var/lib/apt/lists/*


COPY . /home/app
COPY server.sh /home/app

RUN chmod +x /home/app/server.sh

EXPOSE 8030

CMD ["sh", "-c", "/home/app/server.sh"]

