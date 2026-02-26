import json

from src.lambda_function import lambda_handler


def test_handler_success(event, context):
    response = lambda_handler(event, context)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["message"] == "Hello, TestUser!"


def test_handler_default_name(context):
    response = lambda_handler({"body": "{}"}, context)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["message"] == "Hello, World!"


def test_handler_with_environment(context, monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "dev")
    response = lambda_handler({"body": '{"name": "TestUser"}'}, context)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["message"] == "Hello, TestUser! Environment: dev"


def test_handler_without_environment(context, monkeypatch):
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    response = lambda_handler({"body": '{"name": "TestUser"}'}, context)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["message"] == "Hello, TestUser!"


def test_handler_invalid_json(context):
    response = lambda_handler({"body": "invalid{"}, context)

    assert response["statusCode"] == 500
    body = json.loads(response["body"])
    assert "error" in body
