from datetime import datetime
from typing import List, Dict
from uuid import uuid4

class Encuesta:
    def __init__(self, pregunta: str, opciones: List[str], duracion_segundos: int, tipo: str = "simple"):
        self.id = str(uuid4())
        self.pregunta = pregunta
        self.opciones = opciones
        self.votos: Dict[str, int] = {op: 0 for op in opciones}
        self.estado = "activa"
        self.timestamp_inicio = datetime.now()
        self.duracion_segundos = duracion_segundos
        self.tipo = tipo