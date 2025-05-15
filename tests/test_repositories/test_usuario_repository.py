import pytest
import os
from src.models.usuario import User
from src.repositories.usuario_repository import UsuarioRepository

@pytest.fixture
def usuario_repo(tmpdir):
    """Crea un repositorio temporal para las pruebas."""
    storage_path = str(tmpdir)
    return UsuarioRepository(storage_path, "json")

def test_save_and_get_user(usuario_repo):
    """Prueba guardar y recuperar un usuario."""
    user = User("user1", "password123")
    user.add_token("token1")
    user.generate_session_token()
    usuario_repo.save_user(user)
    retrieved_user = usuario_repo.get_user("user1")
    assert retrieved_user.username == user.username
    assert retrieved_user.password_hash == user.password_hash
    assert retrieved_user.session_token == user.session_token
    assert retrieved_user.tokens == user.tokens

def test_user_exists(usuario_repo):
    """Prueba verificar si un usuario existe."""
    user = User("user1", "password123")
    usuario_repo.save_user(user)
    assert usuario_repo.user_exists("user1")
    assert not usuario_repo.user_exists("user2")

def test_get_all_users(usuario_repo):
    """Prueba recuperar todos los usuarios."""
    user1 = User("user1", "password123")
    user2 = User("user2", "password456")
    usuario_repo.save_user(user1)
    usuario_repo.save_user(user2)
    users = usuario_repo.get_all_users()
    assert len(users) == 2
    assert any(user.username == "user1" for user in users)
    assert any(user.username == "user2" for user in users)