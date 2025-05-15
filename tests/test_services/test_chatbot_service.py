import pytest
from src.services.chatbot_service import ChatbotService

@pytest.fixture
def chatbot_service():
    """Crea un servicio de chatbot."""
    return ChatbotService()  # Ahora debería funcionar con el model_name predeterminado

def test_respond(chatbot_service):
    """Prueba que el chatbot responda a un mensaje."""
    response = chatbot_service.respond("Hola, ¿cómo estás?", "user1")
    assert isinstance(response, str)
    assert len(response) > 0

def test_respond_empty_message(chatbot_service):
    """Prueba que el chatbot maneje un mensaje vacío."""
    response = chatbot_service.respond("", "user1")
    assert isinstance(response, str)
    assert len(response) > 0

def test_respond_different_users(chatbot_service):
    """Prueba que el chatbot responda a diferentes usuarios."""
    response1 = chatbot_service.respond("Hola", "user1")
    response2 = chatbot_service.respond("Hola", "user2")
    assert isinstance(response1, str)
    assert isinstance(response2, str)
    assert len(response1) > 0
    assert len(response2) > 0