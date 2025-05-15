import json
import os
from datetime import datetime
from src.models.encuesta import Poll
from src.models.voto import Vote
from src.config import RUTA_ALMACENAMIENTO, TIPO_ALMACENAMIENTO

class EncuestaRepository:
    def __init__(self, storage_path, storage_type):
        self.storage_path = storage_path
        self.storage_type = storage_type
        self.polls_file = os.path.join(self.storage_path, "polls.json")
        self.votes_file = os.path.join(self.storage_path, "votes.json")
        self._initialize_storage()

    def _initialize_storage(self):
        """Crea los archivos JSON si no existen."""
        if self.storage_type != "json":
            raise NotImplementedError("Solo se soporta almacenamiento JSON por ahora.")
        for file_path in [self.polls_file, self.votes_file]:
            if not os.path.exists(file_path):
                with open(file_path, "w") as f:
                    json.dump([], f)

    def save_poll(self, poll):
        """Guarda una encuesta en el archivo JSON."""
        # Leer las encuestas existentes
        with open(self.polls_file, "r") as f:
            polls = json.load(f)

        # Actualizar o añadir la encuesta
        poll_data = {
            "poll_id": poll.poll_id,
            "question": poll.question,
            "options": poll.options,
            "votes": poll.votes,
            "status": poll.status,
            "timestamp_start": poll.timestamp_start.isoformat(),
            "duration_seconds": poll.duration_seconds,
            "poll_type": poll.poll_type
        }
        # Si la encuesta ya existe, actualizarla; si no, añadirla
        for i, existing_poll in enumerate(polls):
            if existing_poll["poll_id"] == poll.poll_id:
                polls[i] = poll_data
                break
        else:
            polls.append(poll_data)

        # Guardar las encuestas actualizadas
        with open(self.polls_file, "w") as f:
            json.dump(polls, f)

    def get_poll(self, poll_id):
        """Recupera una encuesta por su ID."""
        with open(self.polls_file, "r") as f:
            polls = json.load(f)
        for poll_data in polls:
            if poll_data["poll_id"] == poll_id:
                poll = Poll(
                    poll_id=poll_data["poll_id"],
                    question=poll_data["question"],
                    options=poll_data["options"],
                    duration_seconds=poll_data["duration_seconds"],
                    poll_type=poll_data["poll_type"]
                )
                poll.votes = poll_data["votes"]
                poll.status = poll_data["status"]
                poll.timestamp_start = datetime.fromisoformat(poll_data["timestamp_start"])
                return poll
        return None

    def get_all_polls(self):
        """Recupera todas las encuestas."""
        with open(self.polls_file, "r") as f:
            polls = json.load(f)
        result = []
        for poll_data in polls:
            poll = Poll(
                poll_id=poll_data["poll_id"],
                question=poll_data["question"],
                options=poll_data["options"],
                duration_seconds=poll_data["duration_seconds"],
                poll_type=poll_data["poll_type"]
            )
            poll.votes = poll_data["votes"]
            poll.status = poll_data["status"]
            poll.timestamp_start = datetime.fromisoformat(poll_data["timestamp_start"])
            result.append(poll)
        return result

    def save_vote(self, vote):
        """Guarda un voto en el archivo JSON."""
        with open(self.votes_file, "r") as f:
            votes = json.load(f)
        votes.append({
            "poll_id": vote.poll_id,
            "username": vote.username,
            "option": vote.option,
            "timestamp": vote.timestamp.isoformat()
        })
        with open(self.votes_file, "w") as f:
            json.dump(votes, f)

    def get_votes_for_poll(self, poll_id):
        """Recupera todos los votos de una encuesta."""
        with open(self.votes_file, "r") as f:
            votes = json.load(f)
        result = []
        for vote_data in votes:
            if vote_data["poll_id"] == poll_id:
                vote = Vote(
                    poll_id=vote_data["poll_id"],
                    username=vote_data["username"],
                    option=vote_data["option"],
                    timestamp=datetime.fromisoformat(vote_data["timestamp"])
                )
                result.append(vote)
        return result

    def has_user_voted(self, poll_id, username):
        """Verifica si un usuario ya votó en una encuesta."""
        votes = self.get_votes_for_poll(poll_id)
        return any(vote.username == username for vote in votes)