import sqlite3
from typing import List, Optional
from src.models.encuesta import Encuesta
from src.models.voto import Voto

class EncuestaRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS encuestas (
                    id TEXT PRIMARY KEY,
                    pregunta TEXT,
                    opciones TEXT,
                    votos TEXT,
                    estado TEXT,
                    timestamp_inicio TEXT,
                    duracion_segundos INTEGER,
                    tipo TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS votos (
                    id TEXT PRIMARY KEY,
                    poll_id TEXT,
                    username TEXT,
                    opcion TEXT
                )
            """)

    def save_encuesta(self, encuesta: Encuesta):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO encuestas (id, pregunta, opciones, votos, estado, timestamp_inicio, duracion_segundos, tipo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (encuesta.id, encuesta.pregunta, ",".join(encuesta.opciones), str(encuesta.votos), encuesta.estado, encuesta.timestamp_inicio.isoformat(), encuesta.duracion_segundos, encuesta.tipo)
            )

    def save_voto(self, voto: Voto):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO votos (id, poll_id, username, opcion) VALUES (?, ?, ?, ?)",
                (voto.id, voto.poll_id, voto.username, voto.opcion)
            )

    def get_encuesta(self, poll_id: str) -> Optional[Encuesta]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM encuestas WHERE id = ?", (poll_id,))
            row = cursor.fetchone()
            if row:
                votos = eval(row[3])  # Convertir string a dict (mejor usar JSON en producción)
                return Encuesta(
                    pregunta=row[1],
                    opciones=row[2].split(","),
                    duracion_segundos=row[6],
                    tipo=row[7]
                )
        return None