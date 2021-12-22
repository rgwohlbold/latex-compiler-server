FROM python:3.9-slim

WORKDIR /usr/src/app

RUN apt update && apt install -y texlive-full

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install flask gunicorn

COPY app.py .

CMD ["gunicorn", "--conf", "app.py", "--bind", "0.0.0.0:5000", "app:app"]

