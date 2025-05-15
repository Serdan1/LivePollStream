import json
import os
from src.models.usuario import User
from src.config import RUTA_ALMACENAMIENTO, TIPO_ALMACENAMIENTO

class UsuarioRepository:
    def __init__(self, storage_path, storage_type):
        self.storage_path = storage_path
        self.storage_type = storage_type
        self.users_file = os.path.join(self.storage_path, "users.json")
        self._initialize_storage()

    def _initialize_storage(self):
        """Crea el archivo JSON si no existe."""
        if self.storage_type != "json":
            raise NotImplementedError("Solo se soporta almacenamiento JSON por ahora.")
        if not os.path.exists(self.users_file):
            with open(self.users_file, "w") as f:
                json.dump([], f)

    def save_user(self, user):
        """Guarda un usuario en el archivo JSON."""
        with open(self.users_file, "r") as f:
            users = json.load(f)
        user_data = {
            "username": user.username,
            "password_hash": user.password_hash,
            "session_token": user.session_token,
            "tokens": user.tokens
        }
        # Actualizar si el usuario ya existe, o añadirlo
        for i, existing_user in enumerate(users):
            if existing_user["username"] == user.username:
                users[i] = user_data
                break
        else:
            users.append(user_data)
        with open(self.users_file, "w") as f:
            json.dump(users, f)

    def get_user(self, username):
        """Recupera un usuario por su username."""
        with open(self.users_file, "r") as f:
            users = json.load(f)
        for user_data in users:
            if user_data["username"] == username:
                user = User(user_data["username"], "")  # Contraseña no necesaria para instanciar
                user.password_hash = user_data["password_hash"]
                user.session_token = user_data["session_token"]
                user.tokens = user_data["tokens"]
                return user
        return None

    def user_exists(self, username):
        """Verifica si un usuario ya existe."""
        return self.get_user(username) is not None

    def get_all_users(self):
        """Recupera todos los usuarios."""
        with open(self.users_file, "r") as f:
            users = json.load(f)
        result = []
        for user_data in users:
            user = User(user_data["username"], "")
            user.password_hash = user_data["password_hash"]
            user.session_token = user_data["session_token"]
            user.tokens = user_data["tokens"]
            result.append(user)
        return result