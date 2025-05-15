import gradio as gr
from src.services.poll_service import PollService
from src.services.user_service import UserService
from src.services.nft_service import NFTService
from src.services.chatbot_service import ChatbotService

class GradioUI:
    def __init__(self, poll_service, user_service, nft_service, chatbot_service, port):
        self.poll_service = poll_service
        self.user_service = user_service
        self.nft_service = nft_service
        self.chatbot_service = chatbot_service
        self.port = port

    def launch(self):
        """Inicia la interfaz web con Gradio."""
        with gr.Blocks() as app:
            gr.Markdown("# Plataforma de Votaciones en Vivo para Streamers")

            # Sección de autenticación
            gr.Markdown("## Autenticación")
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Iniciar Sesión")
                    login_username = gr.Textbox(label="Usuario")
                    login_password = gr.Textbox(label="Contraseña", type="password")
                    login_button = gr.Button("Iniciar Sesión")
                    login_output = gr.Textbox(label="Resultado")
                with gr.Column():
                    gr.Markdown("### Registrar Usuario")
                    register_username = gr.Textbox(label="Usuario")
                    register_password = gr.Textbox(label="Contraseña", type="password")
                    register_button = gr.Button("Registrar")
                    register_output = gr.Textbox(label="Resultado")

            # Sección de encuestas
            gr.Markdown("## Encuestas")
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Crear Encuesta")
                    question_input = gr.Textbox(label="Pregunta")
                    options_input = gr.Textbox(label="Opciones (separadas por comas)")
                    duration_input = gr.Number(label="Duración (segundos)", value=60)
                    poll_type_input = gr.Dropdown(label="Tipo de Encuesta", choices=["simple", "multiple", "weighted"], value="simple")
                    create_poll_button = gr.Button("Crear Encuesta")
                    create_poll_output = gr.Textbox(label="Resultado")
                with gr.Column():
                    gr.Markdown("### Votar en Encuesta")
                    poll_list = gr.Dropdown(label="Seleccionar Encuesta", choices=self._get_active_polls())
                    option_input = gr.Dropdown(label="Opción", choices=[])
                    weight_input = gr.Number(label="Peso del Voto (solo para encuestas ponderadas)", value=1)
                    vote_button = gr.Button("Votar")
                    vote_output = gr.Textbox(label="Resultado del Voto")

            # Sección de chatbot
            gr.Markdown("## Chatbot")
            chatbot_input = gr.Textbox(label="Pregunta")
            chatbot_output = gr.Textbox(label="Respuesta")
            chatbot_button = gr.Button("Enviar Pregunta")

            # Sección de tokens
            gr.Markdown("## Tus Tokens NFT")
            token_list = gr.Dataframe(label="Tus Tokens", headers=["Token ID", "Encuesta", "Opción"])
            transfer_token_id = gr.Textbox(label="ID del Token a Transferir")
            transfer_new_owner = gr.Textbox(label="Nuevo Propietario")
            transfer_button = gr.Button("Transferir Token")
            transfer_output = gr.Textbox(label="Resultado de la Transferencia")

            # Funcionalidad
            def register(username, password):
                try:
                    user = self.user_service.register(username, password)
                    return f"Usuario {username} registrado exitosamente."
                except ValueError as e:
                    return f"Error: {e}"

            def login(username, password):
                try:
                    session_token = self.user_service.login(username, password)
                    return f"Sesión iniciada con éxito. Token: {session_token}"
                except ValueError as e:
                    return f"Error: {e}"

            def create_poll(question, options, duration, poll_type, login_output, username):
                print(f"Gradio: create_poll - Creando encuesta: question={question}, options={options}, duration={duration}, poll_type={poll_type}, username={username}")
                if not login_output or not login_output.startswith("Sesión iniciada"):
                    print("Gradio: create_poll - Sesión no iniciada")
                    return "Debes iniciar sesión primero."
                try:
                    session_token = login_output.split("Token: ")[1]
                    print(f"Gradio: create_poll - Verificando sesión para {username} con token {session_token}")
                    self.user_service.verify_session(username, session_token)
                    options_list = [opt.strip() for opt in options.split(",")]
                    poll = self.poll_service.create_poll(question, options_list, int(duration), poll_type)
                    print(f"Gradio: create_poll - Encuesta creada: {poll.__dict__}")
                    return f"Encuesta creada exitosamente. ID: {poll.poll_id}"
                except (ValueError, IndexError) as e:
                    print(f"Gradio: create_poll - Error: {e}")
                    return f"Error: {e}"

            def update_options(poll_id):
                print(f"Gradio: update_options - Actualizando opciones para poll_id={poll_id}")
                poll = self.poll_service.encuesta_repository.get_poll(poll_id)
                if poll:
                    print(f"Gradio: update_options - Encuesta encontrada, opciones: {poll.options}")
                    return gr.update(choices=poll.options)
                else:
                    print(f"Gradio: update_options - Encuesta no encontrada: {poll_id}")
                    return gr.update(choices=[])

            def vote(poll_id, username, option, weight, login_output):
                print(f"Gradio: vote - Iniciando votación: poll_id={poll_id}, username={username}, option={option}, weight={weight}, login_output={login_output}")
                if not login_output or not login_output.startswith("Sesión iniciada"):
                    print("Gradio: vote - Sesión no iniciada")
                    return "Debes iniciar sesión primero."
                try:
                    session_token = login_output.split("Token: ")[1]
                    print(f"Gradio: vote - Verificando sesión para {username} con token {session_token}")
                    self.user_service.verify_session(username, session_token)
                    print(f"Gradio: vote - Sesión verificada, intentando votar")
                    self.poll_service.vote(poll_id, username, option, weight)
                    print(f"Gradio: vote - Voto registrado exitosamente para {username} en {poll_id}")
                    return f"Voto registrado para {username} en la encuesta {poll_id}."
                except (ValueError, IndexError) as e:
                    print(f"Gradio: vote - Error: {e}")
                    return f"Error: {e}"

            def chat(message, username, login_output):
                if not login_output or not login_output.startswith("Sesión iniciada"):
                    return "Debes iniciar sesión primero."
                try:
                    session_token = login_output.split("Token: ")[1]
                    self.user_service.verify_session(username, session_token)
                    return self.chatbot_service.respond(message, username)
                except (ValueError, IndexError) as e:
                    return f"Error: {e}"

            def view_tokens(username, login_output):
                print(f"Gradio: view_tokens - Username: {username}, Login Output: {login_output}")
                if not login_output or not login_output.startswith("Sesión iniciada"):
                    print("Gradio: view_tokens - Sesión no iniciada, devolviendo lista vacía")
                    return []
                try:
                    session_token = login_output.split("Token: ")[1]
                    print(f"Gradio: view_tokens - Verificando sesión para {username} con token {session_token}")
                    if self.user_service.verify_session(username, session_token):
                        print(f"Gradio: view_tokens - Sesión válida, recuperando tokens para {username}")
                        tokens = self.nft_service.get_user_tokens(username)
                        print(f"Gradio: view_tokens - Tokens recuperados: {[token.__dict__ for token in tokens]}")
                        return [[token.token_id, token.poll_id, token.option] for token in tokens]
                    else:
                        print("Gradio: view_tokens - Sesión inválida, devolviendo lista vacía")
                        return []
                except (ValueError, IndexError) as e:
                    print(f"Gradio: view_tokens - Error: {e}, devolviendo lista vacía")
                    return []

            def transfer(token_id, new_owner, username, login_output):
                print(f"Gradio: Intentando transferir token {token_id} de {username} a {new_owner}")
                if not login_output or not login_output.startswith("Sesión iniciada"):
                    return "Debes iniciar sesión primero.", []
                try:
                    session_token = login_output.split("Token: ")[1]
                    self.user_service.verify_session(username, session_token)
                    self.nft_service.transfer_token(token_id, username, new_owner)
                    tokens = self.nft_service.get_user_tokens(username)
                    return f"Token {token_id} transferido a {new_owner}.", [[token.token_id, token.poll_id, token.option] for token in tokens]
                except (ValueError, IndexError) as e:
                    print(f"Gradio: Error en transferencia: {e}")
                    return f"Error: {e}", []

            register_button.click(register, inputs=[register_username, register_password], outputs=register_output)
            login_button.click(login, inputs=[login_username, login_password], outputs=login_output)
            create_poll_button.click(create_poll, inputs=[question_input, options_input, duration_input, poll_type_input, login_output, login_username], outputs=create_poll_output)
            poll_list.change(update_options, inputs=poll_list, outputs=option_input)
            vote_button.click(vote, inputs=[poll_list, login_username, option_input, weight_input, login_output], outputs=vote_output)
            chatbot_button.click(chat, inputs=[chatbot_input, login_username, login_output], outputs=chatbot_output)
            login_username.change(view_tokens, inputs=[login_username, login_output], outputs=token_list)
            transfer_button.click(transfer, inputs=[transfer_token_id, transfer_new_owner, login_username, login_output], outputs=[transfer_output, token_list])

        app.launch(server_port=self.port)

    def _get_active_polls(self):
        """Devuelve una lista de IDs de encuestas activas."""
        print("Gradio: _get_active_polls - Obteniendo encuestas activas")
        polls = self.poll_service.encuesta_repository.get_all_polls()
        active_polls = [poll.poll_id for poll in polls if poll.is_active()]
        print(f"Gradio: _get_active_polls - Encuestas activas: {active_polls}")
        return active_polls