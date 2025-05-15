from src.models.token_nft import TokenNFT
from src.repositories.nft_repository import NFTRepository
from src.repositories.usuario_repository import UsuarioRepository

class NFTService:
    def __init__(self, nft_repository, usuario_repository):
        self.nft_repository = nft_repository
        self.usuario_repository = usuario_repository

    def mint_token(self, username, poll_id, option):
        """Genera un nuevo token NFT al votar."""
        token = TokenNFT(poll_id, option, username)
        self.nft_repository.save_nft(token)
        user = self.usuario_repository.get_user(username)
        if user:
            user.add_token(token.token_id)
            self.usuario_repository.save_user(user)
        return token

    def transfer_token(self, token_id, current_owner, new_owner):
        """Transfiere un token NFT a otro usuario."""
        token = self.nft_repository.get_nft(token_id)
        if not token:
            raise ValueError("Token NFT no encontrado.")
        if token.owner != current_owner:
            raise ValueError("El usuario no es el propietario del token.")
        user_exists = self.usuario_repository.get_user(new_owner)
        if not user_exists:
            raise ValueError("El nuevo propietario no existe.")
        token.owner = new_owner
        self.nft_repository.transfer_nft(token_id, new_owner)
        # Actualizar las listas de tokens de los usuarios
        current_user = self.usuario_repository.get_user(current_owner)
        new_user = self.usuario_repository.get_user(new_owner)
        if current_user:
            current_user.remove_token(token_id)
            self.usuario_repository.save_user(current_user)
        if new_user:
            new_user.add_token(token_id)
            self.usuario_repository.save_user(new_user)

    def get_user_tokens(self, username):
        """Obtiene todos los tokens NFT de un usuario."""
        return self.nft_repository.get_nfts_by_owner(username)