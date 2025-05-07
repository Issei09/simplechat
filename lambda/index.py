import json
import urllib.request

# FastAPI の /generate エンドポイント
FASTAPI_ENDPOINT = "https://a750-34-19-79-110.ngrok-free.app/generate"

def lambda_handler(event, context):
    try:
        # イベントからクエリ本文を取得して JSON に変換
        body = json.loads(event['body'])
        message = body.get('message')

        # FastAPI に送るペイロードを構築（/generate 用）
        payload = {
            "prompt": message,
            "max_new_tokens": 512,
            "do_sample": True,
            "temperature": 0.7,
            "top_p": 0.9
        }

        # HTTP POSTリクエスト
        req = urllib.request.Request(
            FASTAPI_ENDPOINT,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        with urllib.request.urlopen(req) as response:
            response_body = response.read().decode('utf-8')
            result = json.loads(response_body)

        # フロントエンドが期待する形式に整形して返す
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "message": result["generated_text"]  # フロントに合わせた形式
            })
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
