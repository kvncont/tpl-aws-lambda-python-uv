import json
import os


def lambda_handler(event, context):
    """AWS Lambda handler"""
    try:
        body = event.get("body", {})
        if isinstance(body, str):
            body = json.loads(body)

        name = body.get("name", "World")
        env = os.environ.get("ENVIRONMENT")

        message = f"Hello, {name}!"
        if env:
            message = f"Hello, {name}! Environment: {env}"

        return {"statusCode": 200, "body": json.dumps({"message": message})}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
