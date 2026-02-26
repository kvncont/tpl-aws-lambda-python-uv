import pytest


@pytest.fixture
def event():
    return {"body": '{"name": "TestUser"}'}


@pytest.fixture
def context():
    return None
