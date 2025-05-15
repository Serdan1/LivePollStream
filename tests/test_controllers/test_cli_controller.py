import pytest
from io import StringIO
from unittest.mock import patch
from src.controllers.cli_controller import CLIController
from src.services.poll_service import PollService
from src.services.user_service import UserService
from src.services.nft_service import NFTService
from src.services.chatbot_service import ChatbotService
from src.repositories.encuesta_repository import EncuestaRepository
from src.repositories.usuario_repository import UsuarioRepository
from src.repositories.nft_repository import NFTRepository
from src.patterns.factory import SimplePollFactory

@pytest.fixture
def cli_controller(tmpdir):
    """Crea un controlador CLI con servicios temporales."""
    storage_path = str(tmpdir)
    encuesta_repo = EncuestaRepository(storage_path, "json")
    user_repo = UsuarioRepository(storage_path, "json")
    nft_repo = NFTRepository(storage_path, "json")
    poll_service = PollService(encuesta_repo, poll_factory=SimplePollFactory())
    user_service = UserService(user_repo)
    nft_service = NFTService(nft_repo, user_repo)
    chatbot_service = ChatbotService()
    return CLIController(poll_service, user_service, nft_service, chatbot_service)

def test_register_user(cli_controller, capsys):
    """Prueba registrar un usuario a través del CLI."""
    with patch('builtins.input', side_effect=["1", "user1", "password123", "3"]):  # Salir después de registrar
        cli_controller.run()
    captured = capsys.readouterr()
    assert "Usuario user1 registrado exitosamente." in captured.out
    assert "¡Adiós!" in captured.out

def test_login_user(cli_controller, capsys):
    """Prueba iniciar sesión a través del CLI."""
    cli_controller.user_service.register("user1", "password123")
    with patch('builtins.input', side_effect=["2", "user1", "password123", "8"]):  # Salir después de iniciar sesión
        cli_controller.run()
    captured = capsys.readouterr()
    assert "Inicio de sesión exitoso." in captured.out
    assert "¡Adiós!" in captured.out

def test_create_poll(cli_controller, capsys):
    """Prueba crear una encuesta a través del CLI."""
    cli_controller.user_service.register("user1", "password123")
    with patch('builtins.input', side_effect=["2", "user1", "password123", "1", "Pregunta", "Opción 1,Opción 2", "60", "simple", "8"]):  # Salir después de crear
        cli_controller.run()
    captured = capsys.readouterr()
    assert "Inicio de sesión exitoso." in captured.out
    assert "Encuesta creada exitosamente." in captured.out
    assert "¡Adiós!" in captured.out

def test_vote(cli_controller, capsys):
    """Prueba votar en una encuesta a través del CLI."""
    cli_controller.user_service.register("user1", "password123")
    poll = cli_controller.poll_service.create_poll("Pregunta", ["Opción 1", "Opción 2"], 60, poll_type="simple")
    with patch('builtins.input', side_effect=["2", "user1", "password123", "2", poll.poll_id, "Opción 1", "8"]):  # Salir después de votar
        cli_controller.run()
    captured = capsys.readouterr()
    assert "Inicio de sesión exitoso." in captured.out
    assert "Voto registrado exitosamente." in captured.out
    assert "¡Adiós!" in captured.out