FROM python:3.10.7-alpine

WORKDIR /app

COPY requirement.txt .
RUN pip3 install -r requirement.txt

COPY server.py .
COPY jerm.py .

CMD ["python", "server.py"]
