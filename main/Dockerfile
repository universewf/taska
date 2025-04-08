
FROM python:3.9-alpine3.16

WORKDIR /myapp

EXPOSE 8000

COPY requirements.txt .

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]