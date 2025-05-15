from src.services.poll_service import PollService
from src.services.user_service import UserService
from src.services.nft_service import NFTService
from src.config import Config

class CLIController:
    def __init__(self, config: Config):
        self.poll_service = PollService(config.encuesta_repository)
        self.user_service = UserService(config.usuario_repository)
        self.nft_service = NFTService(config.nft_repository)
        self.config = config

    def run(self):
        while True:
            print("\nComandos: crear_encuesta, votar, cerrar_encuesta, mis_tokens, transferir_token, salir")
            cmd = input("> ").split()
            try:
                if not cmd:
                    continue
                if cmd[0] == "crear_encuesta":
                    pregunta = input("Pregunta: ")
                    opciones = input("Opciones (separadas por coma): ").split(",")
                    duracion = int(input("Duración (segundos): "))
                    encuesta = self.poll_service.create_poll(pregunta, opciones, duracion)
                    print(f"Encuesta creada: {encuesta.id}")
                elif cmd[0] == "votar":
                    poll_id = cmd[1]
                    username = cmd[2]
                    opcion = cmd[3]
                    self.poll_service.vote(poll_id, username, opcion)
                    print("Voto registrado")
                elif cmd[0] == "cerrar_encuesta":
                    poll_id = cmd[1]
                    self.poll_service.close_poll(poll_id)
                    print("Encuesta cerrada")
                elif cmd[0] == "mis_tokens":
                    username = cmd[1]
                    tokens = self.nft_service.get_user_tokens(username)
                    for token in tokens:
                        print(f"Token {token.token_id}: {token.opcion}")
                elif cmd[0] == "transferir_token":
                    token_id = cmd[1]
                    new_owner = cmd[2]
                    self.nft_service.transfer_token(token_id, new_owner)
                    print("Token transferido")
                elif cmd[0] == "salir":
                    break
            except Exception as e:
                print(f"Error: {e}")