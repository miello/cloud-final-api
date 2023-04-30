FROM python:3.10.7-alpine

WORKDIR /app

COPY requirement.txt .
RUN pip install -r requirement.txt

COPY server.py .
CMD ["python", "server.py"]
