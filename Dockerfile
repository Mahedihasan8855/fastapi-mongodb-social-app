FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8005

ENV MONGO_HOST mymongo
ENV MONGO_PORT 27017
ENV MONGO_USER sa
ENV MONGO_PASSWORD VERY_STRONG_PASSWORD

RUN python3 script.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005"]
