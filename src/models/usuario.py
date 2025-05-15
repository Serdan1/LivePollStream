import hashlib
import uuid

class User:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = self._hash_password(password)
        self.session_token = None
        self.tokens = []  # Lista de token_id de NFTs

    def _hash_password(self, password):
        """Hashea la contraseña usando pbkdf2_hmac."""
        return hashlib.pbkdf2_hmac('sha256', password.encode(), b'salt', 100000).hex()

    def verify_password(self, password):
        """Verifica si la contraseña coincide con el hash almacenado."""
        return self.password_hash == self._hash_password(password)

    def generate_session_token(self):
        """Genera un token de sesión único para el usuario."""
        self.session_token = str(uuid.uuid4())
        return self.session_token

    def add_token(self, token_id):
        """Añade un token NFT a la lista del usuario."""
        if token_id not in self.tokens:
            self.tokens.append(token_id)

    def remove_token(self, token_id):
        """Elimina un token NFT de la lista del usuario."""
        if token_id in self.tokens:
            self.tokens.remove(token_id)

    def __repr__(self):
        return f"User(username={self.username}, tokens={self.tokens})"