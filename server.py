from flask_cors import CORS, cross_origin
from flask import Flask, request
import os
import boto3
import random
import json
from mimetypes import MimeTypes
from dotenv import load_dotenv

load_dotenv()

PORT = os.environ.get('PORT', 3030)
QUEUE_URL = os.environ.get('SQS_QUEUE_URL')
BUCKET_NAME = os.environ.get('BUCKET_NAME')
CHAR_LIST = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

mime = MimeTypes()
app = Flask(__name__)
client_ses = boto3.client('ses')
client_s3 = boto3.client('s3')
client_sqs = boto3.client('sqs')


def random_id():
    return ''.join(random.choice(CHAR_LIST) for _ in range(10))


def check_verified_email(email: str) -> bool:
    response = client_ses.list_verified_email_addresses()
    return email in response['VerifiedEmailAddresses']

@app.get('/healthz')
@cross_origin()
def healthz():
    return {'message': 'health OK'}

@app.post('/upload')
@cross_origin()
def send_file():
    form = request.form
    file = request.files['file']

    file_id = random_id()

    open(f'./{file_id}', 'wb').close()
    file_length = len(file.read())

    if file_length > 8 * 1024 * 1024:
        return {'message': 'File too large'}, 400

    email = form['email']

    if file.mimetype != 'application/pdf':
        return {'message': 'File must be PDF'}, 400

    if not check_verified_email(email):
        return {'message': 'Email not verified'}, 400

    file_id = random_id()
    client_s3.upload_fileobj(file, BUCKET_NAME, f'raw/{file_id}.pdf')
    client_sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(
            {'file_id': file_id, 's3_key': f'raw/{file_id}.pdf',  'email': email}),
        MessageAttributes={
            'file_id': {
                'DataType': 'String',
                'StringValue': file_id
            },
            'email': {
                'DataType': 'String',
                'StringValue': email
            },
            's3_key': {
                'DataType': 'String',
                'StringValue': f'raw/{file_id}.pdf'
            }
        }
    )

    return {'fileId': file_id}


@app.post('/verify')
@cross_origin()
def verify_email():
    json = request.get_json()
    email = json['email']

    if check_verified_email(email):
        return {'message': 'Email already verified'}, 400

    client_ses.verify_email_identity(EmailAddress=email)
    return {'message': 'Verification email sent'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
