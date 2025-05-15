import pytest
from src.models.usuario import User

def test_create_user():
    """Prueba la creación de un usuario."""
    user = User("user1", "password123")
    assert user.username == "user1"
    assert user.password_hash is not None
    assert user.session_token is None
    assert user.tokens == []

def test_verify_password():
    """Prueba la verificación de la contraseña."""
    user = User("user1", "password123")
    assert user.verify_password("password123")
    assert not user.verify_password("wrongpassword")

def test_generate_session_token():
    """Prueba la generación de un token de sesión."""
    user = User("user1", "password123")
    token = user.generate_session_token()
    assert user.session_token == token
    assert isinstance(token, str)
    assert len(token) > 0

def test_add_remove_token():
    """Prueba añadir y eliminar tokens NFT."""
    user = User("user1", "password123")
    user.add_token("token1")
    assert "token1" in user.tokens
    user.add_token("token2")
    assert user.tokens == ["token1", "token2"]
    user.remove_token("token1")
    assert user.tokens == ["token2"]