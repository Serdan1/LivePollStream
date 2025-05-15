from datetime import datetime
from uuid import uuid4

class TokenNFT:
    def __init__(self, poll_id: str, username: str, opcion: str):
        self.token_id = str(uuid4())
        self.owner = username
        self.poll_id = poll_id
        self.opcion = opcion
        self.issued_at = datetime.now()