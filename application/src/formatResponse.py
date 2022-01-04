import json

headers = {
    "Access-Control-Allow-Headers" : "Content-Type",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "OPTIONS,GET"
}

def format_response(message, status_code, include_headers=True):
    """
    Format the response to correct schema
    """
    response = {
        'statusCode': status_code,
        'body': json.dumps(message, default=str)
    }

    if include_headers:
        response["headers"] = headers

    return response