from datetime import datetime
import uuid

class Poll:
    def __init__(self, poll_id, question, options, duration_seconds, poll_type="simple"):
        self.poll_id = poll_id if poll_id else str(uuid.uuid4())  # Usar UUID si no se proporciona ID
        self.question = question
        self.options = options  # Lista de strings
        self.votes = {}  # Diccionario {username: option}
        self.status = "active"
        self.timestamp_start = datetime.now()
        self.duration_seconds = duration_seconds
        self.poll_type = poll_type

    def is_active(self):
        """Verifica si la encuesta está activa basado en la duración."""
        if self.status == "closed":
            return False
        elapsed_time = (datetime.now() - self.timestamp_start).total_seconds()
        return elapsed_time < self.duration_seconds

    def add_vote(self, username, option):
        """Registra un voto si la encuesta está activa y la opción es válida."""
        if not self.is_active():
            raise ValueError("La encuesta está cerrada.")
        if option not in self.options:
            raise ValueError("Opción inválida.")
        if username in self.votes:
            raise ValueError("El usuario ya ha votado.")
        self.votes[username] = option

    def close(self):
        """Cierra la encuesta manualmente."""
        self.status = "closed"

    def get_results(self):
        """Devuelve los resultados actuales de la encuesta."""
        if not self.votes:
            return {option: 0 for option in self.options}
        results = {option: 0 for option in self.options}
        for vote in self.votes.values():
            results[vote] += 1
        return results