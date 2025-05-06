# lambda/index.py
import json
import urllib.request

FASTAPI_ENDPOINT = "https://cdc6-34-142-252-55.ngrok-free.app/chat"

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        message = body.get('message')
        conversation_history = body.get('conversationHistory', [])

        payload = {
            "message": message,
            "conversationHistory": conversation_history
        }

        req = urllib.request.Request(
            FASTAPI_ENDPOINT,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        with urllib.request.urlopen(req) as response:
            response_body = response.read().decode('utf-8')
            result = json.loads(response_body)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps(result)
        }

    except Exception as error:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": False,
                "error": str(error)
            })
        }
