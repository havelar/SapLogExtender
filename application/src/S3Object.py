from application.src.Zipfile import ZipFile
from io import BytesIO
import boto3
import os

BUCKET_NAME = os.environ.get('BUCKET_NAME', 'sap-logs-stash')

def getObject(file_name):
    s3 = boto3.resource('s3')
    

    obj = s3.Object(BUCKET_NAME, f"raw/{file_name}")

    file_io = BytesIO(obj.get()['Body'].read())

    if file_name.endswith('.zip'):
        zipfile = ZipFile(file_io)
        f_name = zipfile.namelist()[0]
        file_text = zipfile.open(f_name).read().decode()
        file_name = file_name.replace('.zip', '.txt')
    else:
        file_text = file_io.read().decode()
    
    return file_text, file_name

def putObject(zipFileIO, file_name):
    s3_resource = boto3.resource('s3')
    s3_client = boto3.client('s3')

    file_name = file_name.replace('.txt', '.zip')

    s3_object = s3_resource.Object(BUCKET_NAME, f"done/{file_name}")

    zipFileIO.seek(0)
    s3_object.put(Body=zipFileIO.read())

    presigned_url = s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': BUCKET_NAME,
            'Key': f'done/{file_name}'
        }
    )

    return presigned_url