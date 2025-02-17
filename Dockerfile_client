FROM python

RUN pip install typer fastapi uvicorn sqlalchemy requests pydantic typing tk
WORKDIR /home/app

RUN apt-get update && apt-get install -y iproute2 iptables iputils-ping && rm -rf /var/lib/apt/lists/*


COPY . /home/app

EXPOSE 8070

CMD ["sh", "-c", "/home/app/client.sh"]

