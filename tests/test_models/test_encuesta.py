import pytest
from src.models.encuesta import Encuesta
from datetime import datetime

def test_encuesta_creation():
    encuesta = Encuesta("¿Quién ganará?", ["Equipo A", "Equipo B"], 300)
    assert encuesta.pregunta == "¿Quién ganará?"
    assert encuesta.opciones == ["Equipo A", "Equipo B"]
    assert encuesta.duracion_segundos == 300
    assert encuesta.estado == "activa"
    assert isinstance(encuesta.timestamp_inicio, datetime)
    assert encuesta.votos == {"Equipo A": 0, "Equipo B": 0}