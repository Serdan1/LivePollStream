from datetime import datetime, timedelta
from typing import List, Optional
from src.models.encuesta import Encuesta
from src.models.voto import Voto
from src.repositories.encuesta_repository import EncuestaRepository
from src.patterns.observer import Subject
from src.patterns.strategy import DesempateStrategy, RandomDesempate

class PollService(Subject):
    def __init__(self, encuesta_repository: EncuestaRepository, desempate_strategy: DesempateStrategy = RandomDesempate()):
        self.encuesta_repository = encuesta_repository
        self.desempate_strategy = desempate_strategy
        self._observers = []

    def create_poll(self, pregunta: str, opciones: List[str], duracion_segundos: int, tipo: str = "simple") -> Encuesta:
        encuesta = Encuesta(pregunta, opciones, duracion_segundos, tipo)
        self.encuesta_repository.save_encuesta(encuesta)
        return encuesta

    def vote(self, poll_id: str, username: str, opcion: str):
        encuesta = self.encuesta_repository.get_encuesta(poll_id)
        if not encuesta or encuesta.estado != "activa":
            raise ValueError("Encuesta no válida o cerrada")
        if self._has_voted(poll_id, username):
            raise ValueError("Usuario ya votó")
        if opcion not in encuesta.opciones:
            raise ValueError("Opción no válida")
        
        voto = Voto(poll_id, username, opcion)
        self.encuesta_repository.save_voto(voto)
        encuesta.votos[opcion] += 1
        self.encuesta_repository.save_encuesta(encuesta)
        self._notify_observers({"event": "vote", "poll_id": poll_id, "username": username})

    def close_poll(self, poll_id: str):
        encuesta = self.encuesta_repository.get_encuesta(poll_id)
        if not encuesta or encuesta.estado != "activa":
            raise ValueError("Encuesta no válida o ya cerrada")
        encuesta.estado = "cerrada"
        self.encuesta_repository.save_encuesta(encuesta)
        self._notify_observers({"event": "poll_closed", "poll_id": poll_id})

    def check_expired_polls(self):
        with sqlite3.connect(self.encuesta_repository.db_path) as conn:
            cursor = conn.execute("SELECT id, timestamp_inicio, duracion_segundos FROM encuestas WHERE estado = 'activa'")
            for row in cursor.fetchall():
                poll_id, timestamp_str, duracion = row
                start_time = datetime.fromisoformat(timestamp_str)
                if datetime.now() > start_time + timedelta(seconds=duracion):
                    self.close_poll(poll_id)

    def _has_voted(self, poll_id: str, username: str) -> bool:
        with sqlite3.connect(self.encuesta_repository.db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM votos WHERE poll_id = ? AND username = ?", (poll_id, username))
            return cursor.fetchone()[0] > 0