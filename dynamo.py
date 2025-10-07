import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

def criar_tabelas():
    try:
        table_usuarios = dynamodb.create_table(
            TableName='Usuarios',
            KeySchema=[
                {'AttributeName': 'user_id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'user_id', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        table_usuarios.wait_until_exists()
        print("Tabela usuários criada.")
    except ClientError as e:
        if e.response['Error']['Code'] != 'ResourceInUseException':
            raise

    try:
        table_filmes = dynamodb.create_table(
            TableName='Filmes',
            KeySchema=[
                {'AttributeName': 'filme_id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'filme_id', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        table_filmes.wait_until_exists()
        print("Tabela filmes criada.")
    except ClientError as e:
        if e.response['Error']['Code'] != 'ResourceInUseException':
            raise

    try:
        table_avaliacoes = dynamodb.create_table(
            TableName='Avaliacoes',
            KeySchema=[
                {'AttributeName': 'user_id', 'KeyType': 'HASH'},
                {'AttributeName': 'filme_id', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'user_id', 'AttributeType': 'S'},
                {'AttributeName': 'filme_id', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'FilmeAvaliacoesIndex',
                    'KeySchema': [
                        {'AttributeName': 'filme_id', 'KeyType': 'HASH'},
                        {'AttributeName': 'user_id', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'}
                }
            ],
            BillingMode='PAY_PER_REQUEST' 
        )
        table_avaliacoes.wait_until_exists()
        print("Tabela avaliacoes criada.")
    except ClientError as e:
        if e.response['Error']['Code'] != 'ResourceInUseException':
            raise

if __name__ == '__main__':
    criar_tabelas()