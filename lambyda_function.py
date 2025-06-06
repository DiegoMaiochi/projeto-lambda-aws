import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    SENDER = "diegoabreu382@gmail.com"
    AWS_REGION = "sa-east-1"

    try:
        to_email = event['to_email']
        subject = event['subject']
        body_text = event['body']
    except KeyError as e:
        print(f"Erro: A chave {e} está faltando no evento de entrada.")
        return {
            'statusCode': 400,
            'body': json.dumps(f"Erro de entrada: A chave {e} é obrigatória.")
        }

    client = boto3.client('ses', region_name=AWS_REGION)

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    to_email,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': "UTF-8",
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': "UTF-8",
                    'Data': subject,
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': json.dumps(f"Erro ao enviar e-mail: {e.response['Error']['Message']}")
        }
    else:
        message_id = response['MessageId']
        print(f"E-mail enviado com sucesso! Message ID: {message_id}")
        return {
            'statusCode': 200,
            'body': json.dumps(f"E-mail enviado para {to_email}! Message ID: {message_id}")
        }