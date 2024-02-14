FROM python:3.10

WORKDIR /currency-manager

COPY requirements.txt .
COPY .env .
COPY /python .
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
