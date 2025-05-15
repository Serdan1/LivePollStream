import pytest
from src.models.usuario import User
from src.repositories.usuario_repository import UsuarioRepository
from src.services.user_service import UserService

@pytest.fixture
def user_service(tmpdir):
    """Crea un servicio de usuarios con un repositorio temporal."""
    storage_path = str(tmpdir)
    repo = UsuarioRepository(storage_path, "json")
    return UserService(repo)

def test_register(user_service):
    """Prueba registrar un usuario."""
    user = user_service.register("user1", "password123")
    assert user.username == "user1"
    assert user.password_hash is not None
    assert user_service.usuario_repository.user_exists("user1")  # Usamos user_service.usuario_repository

def test_register_duplicate(user_service):
    """Prueba que no se pueda registrar un usuario con un nombre duplicado."""
    user_service.register("user1", "password123")
    with pytest.raises(ValueError, match="El nombre de usuario ya existe"):
        user_service.register("user1", "password456")

def test_login(user_service):
    """Prueba iniciar sesión con credenciales correctas."""
    user_service.register("user1", "password123")
    session_token = user_service.login("user1", "password123")
    assert isinstance(session_token, str)
    assert len(session_token) > 0

def test_login_invalid_credentials(user_service):
    """Prueba iniciar sesión con credenciales incorrectas."""
    user_service.register("user1", "password123")
    with pytest.raises(ValueError, match="Credenciales inválidas"):
        user_service.login("user1", "wrongpassword")

def test_verify_session(user_service):
    """Prueba verificar un token de sesión."""
    user_service.register("user1", "password123")
    session_token = user_service.login("user1", "password123")
    # Depuración: Recuperar el usuario del repositorio y verificar el token
    user = user_service.usuario_repository.get_user("user1")
    assert user.session_token == session_token  # Verificar que el token coincide
    assert user_service.verify_session("user1", session_token)
    assert not user_service.verify_session("user1", "invalid_token")