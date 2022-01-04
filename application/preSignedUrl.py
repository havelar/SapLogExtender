from application.src.formatResponse import format_response
from application.src.RouteError import RouteError
import traceback
import boto3
import os

def main(event, context):
    try:
        if 'queryStringParameters' not in event.keys():
            raise RouteError('Messing Params', 401)

        params = event["queryStringParameters"]
        file_name = params['file_name']

        bucket_name = os.environ.get('BUCKET_NAME')
        expires_in = os.environ.get('EXPIRES_IN')

        url = boto3.client('s3').generate_presigned_post(
            Bucket=bucket_name,
            Key=f"raw/{file_name}",
            ExpiresIn=int(expires_in),
            Fields = {
                "acl": "public-read",
                "Content-Type": "multipart/form-data"
            },
            Conditions = [
                {"acl": "public-read"},
                ["content-length-range", 1, 33554432],
                ["starts-with", "$Content-Type", ""]
            ], 
        )

        response = format_response(
            url,
            status_code=200
        )

    except RouteError as e:
        response = format_response({'message': e.message}, e.status_code)

    except Exception as e:
        error ={
            "exception": str(e),
            "error": traceback.format_exc(),
            "function": 'addAnswer',
            "event": event
        }
        print(error)
        # Send to SNS
        response = format_response({'message': 'Something went wrong.', 'error': error}, 500)

    finally:
        return response