FROM python:3.8.3-alpine

RUN apk add -U --no-cache python3-dev py3-pip build-base

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

RUN rm -f requirements.txt

COPY ./api-maria.py /app/

WORKDIR /app

ENV FLASK_APP=api-maria.py

EXPOSE 8080

CMD ["python3", "-u", "-m", "flask", "run", "--host=0.0.0.0", "--port=8080"]

