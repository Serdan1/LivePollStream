import pytest
from datetime import datetime, timedelta
from src.models.encuesta import Poll

# Fixture para crear una encuesta base
@pytest.fixture
def poll():
    return Poll(None, "Pregunta", ["Opción 1", "Opción 2"], 60, poll_type="simple")

def test_add_vote_simple(poll):
    """Prueba que una encuesta simple permita un solo voto por usuario."""
    poll.add_vote("user1", "Opción 1")
    assert poll.votes["user1"] == "Opción 1"
    with pytest.raises(ValueError, match="El usuario ya ha votado"):
        poll.add_vote("user1", "Opción 2")

def test_add_vote_multiple():
    """Prueba que una encuesta múltiple permita varios votos por usuario."""
    poll = Poll(None, "Pregunta", ["Opción 1", "Opción 2"], 60, poll_type="multiple")
    poll.add_vote("user1", "Opción 1")
    poll.add_vote("user1", "Opción 2")
    assert poll.votes["user1"] == ["Opción 1", "Opción 2"]

def test_add_vote_weighted():
    """Prueba que una encuesta ponderada almacene los pesos de los votos."""
    poll = Poll(None, "Pregunta", ["Opción 1", "Opción 2"], 60, poll_type="weighted")
    poll.add_vote("user1", "Opción 1", weight=3)
    poll.add_vote("user1", "Opción 2", weight=2)
    assert poll.weights["user1"] == {"Opción 1": 3, "Opción 2": 2}

def test_get_results_simple():
    """Prueba el cálculo de resultados para una encuesta simple."""
    poll = Poll(None, "Pregunta", ["Opción 1", "Opción 2"], 60, poll_type="simple")
    poll.add_vote("user1", "Opción 1")
    poll.add_vote("user2", "Opción 1")
    poll.add_vote("user3", "Opción 2")
    results = poll.get_results()
    assert results["Opción 1"] == 2
    assert results["Opción 2"] == 1

def test_get_results_multiple():
    """Prueba el cálculo de resultados para una encuesta múltiple."""
    poll = Poll(None, "Pregunta", ["Opción 1", "Opción 2"], 60, poll_type="multiple")
    poll.add_vote("user1", "Opción 1")
    poll.add_vote("user1", "Opción 2")
    poll.add_vote("user2", "Opción 1")
    results = poll.get_results()
    assert results["Opción 1"] == 2
    assert results["Opción 2"] == 1

def test_get_results_weighted():
    """Prueba el cálculo de resultados para una encuesta ponderada."""
    poll = Poll(None, "Pregunta", ["Opción 1", "Opción 2"], 60, poll_type="weighted")
    poll.add_vote("user1", "Opción 1", weight=3)
    poll.add_vote("user1", "Opción 2", weight=2)
    poll.add_vote("user2", "Opción 1", weight=1)
    results = poll.get_results()
    assert results["Opción 1"] == 4
    assert results["Opción 2"] == 2

def test_add_vote_invalid_option(poll):
    """Prueba que se lance un error al votar por una opción inválida."""
    with pytest.raises(ValueError, match="Opción inválida"):
        poll.add_vote("user1", "Opción 3")

def test_add_vote_closed_poll():
    """Prueba que no se pueda votar en una encuesta cerrada."""
    poll = Poll(None, "Pregunta", ["Opción 1", "Opción 2"], 60, poll_type="simple")
    poll.close()
    with pytest.raises(ValueError, match="La encuesta está cerrada"):
        poll.add_vote("user1", "Opción 1")

def test_is_active_expired():
    """Prueba que una encuesta expire después de su duración."""
    # Crear una encuesta con duración de 1 segundo
    poll = Poll(None, "Pregunta", ["Opción 1", "Opción 2"], 1, poll_type="simple")
    # Simular que ha pasado más tiempo
    poll.timestamp_start = datetime.now() - timedelta(seconds=2)
    assert not poll.is_active()