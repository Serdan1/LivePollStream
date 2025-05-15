from src.models.usuario import User
from src.repositories.usuario_repository import UsuarioRepository

class UserService:
    def __init__(self, usuario_repository):
        self.usuario_repository = usuario_repository

    def register(self, username, password):
        """Registra un nuevo usuario si el username no existe."""
        if self.usuario_repository.user_exists(username):
            raise ValueError("El nombre de usuario ya existe.")
        user = User(username, password)
        self.usuario_repository.save_user(user)
        return user

    def login(self, username, password):
        """Autentica a un usuario y genera un token de sesión."""
        user = self.usuario_repository.get_user(username)
        if not user or not user.verify_password(password):
            raise ValueError("Credenciales inválidas.")
        return user.generate_session_token()

    def get_user(self, username):
        """Obtiene un usuario por su username."""
        user = self.usuario_repository.get_user(username)
        if not user:
            raise ValueError("Usuario no encontrado.")
        return user

    def verify_session(self, username, session_token):
        """Verifica si un token de sesión es válido para un usuario."""
        user = self.get_user(username)
        return user.session_token == session_token