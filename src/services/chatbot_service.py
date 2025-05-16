from transformers import pipeline

class ChatbotService:
    def __init__(self):
        print("ChatbotService: Inicializando chatbot con modelo datificate/gpt2-small-spanish")
        # Cargar el modelo de generación de texto en español
        self.chatbot = pipeline("text-generation", model="datificate/gpt2-small-spanish")

    def respond(self, message, username):
        print(f"ChatbotService: respond - Procesando mensaje de {username}: '{message}'")
        if not message or not isinstance(message, str):
            print("ChatbotService: respond - Mensaje inválido, devolviendo respuesta genérica")
            return f"{username}, por favor escribe un mensaje válido."
        
        # Generar la respuesta con el modelo
        try:
            # Agregar el nombre del usuario al prompt para personalizar la respuesta
            prompt = f"{username}, {message}"
            response = self.chatbot(prompt, max_length=100, do_sample=True, num_return_sequences=1)[0]['generated_text']
            # Limpiar la respuesta para que sea más legible
            response = response.strip()
            # Si la respuesta incluye el prompt inicial, lo eliminamos
            if response.startswith(prompt):
                response = response[len(prompt):].strip()
            print(f"ChatbotService: respond - Respuesta generada: {response}")
            return f"{username}, {response}"
        except Exception as e:
            print(f"ChatbotService: respond - Error al generar respuesta: {e}")
            return f"{username}, lo siento, ocurrió un error al procesar tu mensaje."