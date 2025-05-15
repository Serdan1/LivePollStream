from src.repositories.encuesta_repository import EncuestaRepository
from src.repositories.usuario_repository import UsuarioRepository
from src.repositories.nft_repository import NFTRepository

class Config:
    def __init__(self):
        self.db_path = "livepollstream.sqlite"
        self.port = 7860
        self.chatbot_model = "facebook/blenderbot-400M-distill"
        self.encuesta_repository = EncuestaRepository(self.db_path)
        self.usuario_repository = UsuarioRepository(self.db_path)
        self.nft_repository = NFTRepository(self.db_path)