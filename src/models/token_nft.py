import uuid
from datetime import datetime

class TokenNFT:
    def __init__(self, poll_id, option, owner, issued_at=None):
        self.token_id = str(uuid.uuid4())  # Identificador único
        self.poll_id = poll_id  # ID de la encuesta
        self.option = option  # Opción votada
        self.owner = owner  # Username del propietario
        self.issued_at = issued_at or datetime.now()  # Fecha de emisión

    def __repr__(self):
        return f"TokenNFT(token_id={self.token_id}, poll_id={self.poll_id}, option={self.option}, owner={self.owner}, issued_at={self.issued_at})"