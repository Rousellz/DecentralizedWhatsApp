FROM python

RUN pip install typer fastapi uvicorn sqlalchemy requests pydantic typing tk
RUN mkdir -p /home/app

COPY . /home/app

EXPOSE 8070

CMD ["python", "/home/app/client_app.py"]