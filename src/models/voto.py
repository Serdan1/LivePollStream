from uuid import uuid4

class Voto:
    def __init__(self, poll_id: str, username: str, opcion: str):
        self.id = str(uuid4())
        self.poll_id = poll_id
        self.username = username
        self.opcion = opcion