from src.app import get_ping


def test_get_ping():
    assert get_ping() == "pong"
