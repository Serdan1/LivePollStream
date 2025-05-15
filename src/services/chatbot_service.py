from transformers import pipeline
from src.services.poll_service import PollService
from src.config import MODELO_HUGGINGFACE
from datetime import datetime

class ChatbotService:
    def __init__(self, model_name, poll_service=None):
        """Inicializa el chatbot con un modelo de Hugging Face."""
        self.chatbot = pipeline("conversational", model=model_name)
        self.poll_service = poll_service

    def respond(self, message, username=None):
        """Responde a un mensaje del usuario."""
        # Verificar si la pregunta es sobre encuestas
        if self.poll_service and any(keyword in message.lower() for keyword in ["quién va ganando", "cuánto falta", "resultados"]):
            return self._handle_poll_query(message)
        # Usar el modelo de Hugging Face para responder preguntas generales
        response = self.chatbot(message)
        return response[-1]["generated_text"]

    def _handle_poll_query(self, message):
        """Maneja preguntas relacionadas con encuestas."""
        polls = self.poll_service.encuesta_repository.get_all_polls()
        active_polls = [poll for poll in polls if poll.is_active()]
        if not active_polls:
            return "No hay encuestas activas en este momento."
        # Tomar la primera encuesta activa para simplificar
        poll = active_polls[0]
        if "quién va ganando" in message.lower() or "resultados" in message.lower():
            results = self.poll_service.get_partial_results(poll.poll_id)
            leading_option = max(results["counts"], key=results["counts"].get, default=None)
            if leading_option:
                return (f"En la encuesta '{poll.question}', la opción que va ganando es '{leading_option}' "
                        f"con {results['counts'][leading_option]} votos ({results['percentages'][leading_option]:.1f}%).")
            return "Aún no hay votos en esta encuesta."
        elif "cuánto falta" in message.lower():
            remaining_time = poll.duration_seconds - (datetime.now() - poll.timestamp_start).total_seconds()
            return (f"Para la encuesta '{poll.question}', faltan {max(0, int(remaining_time))} segundos "
                    "para que termine.")
        return "No entendí tu pregunta sobre la encuesta. ¿Puedes reformularla?"