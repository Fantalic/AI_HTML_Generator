from aigen_html.services.jwt import create_jwt, verify_jwt

SECRET = "test_secret"


def test_create_and_verify_jwt():
    token = create_jwt(42, SECRET)
    assert token is not None
    assert isinstance(token, str)
    assert token.count(".") == 2

    payload = verify_jwt(token, SECRET)
    assert payload is not None
    assert payload["sub"] == "42"


def test_verify_invalid_token():
    result = verify_jwt("invalid.token.here", SECRET)
    assert result is None


def test_verify_wrong_secret():
    token = create_jwt(1, SECRET)
    result = verify_jwt(token, "wrong_secret")
    assert result is None
