FROM python:3.8

RUN pip install fastapi uvicorn sqlalchemy

EXPOSE 80

RUN mkdir data

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]