FROM python:3.11-slim

RUN pip install typer fastapi uvicorn sqlalchemy requests pydantic typing
RUN mkdir -p /home/app

COPY . /home/app

EXPOSE 8030

CMD ["python", "/home/app/server_app.py", "first-server"]