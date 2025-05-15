# LivePollStream

https://github.com/Serdan1/LivePollStream.git


# LivePollStream

LivePollStream es una plataforma de votaciones en vivo diseñada para streamers, que permite a los usuarios crear encuestas, votar, obtener tokens NFT simulados como recompensa, transferir esos tokens a otros usuarios y visualizar los resultados en tiempo real. Además, incluye un chatbot simple para interactuar con los usuarios.

## Características principales

- **Creación de encuestas**: Los usuarios pueden crear encuestas con opciones personalizadas y diferentes tipos (simple, múltiple, ponderada).
- **Votación**: Los usuarios autenticados pueden votar en encuestas activas.
- **Tokens NFT simulados**: Cada voto genera un token NFT que se asigna al usuario como recompensa.
- **Transferencia de tokens**: Los usuarios pueden transferir sus tokens NFT a otros usuarios registrados.
- **Resultados en tiempo real**: Visualiza los resultados de las encuestas en porcentajes mediante una tabla dinámica.
- **Chatbot interactivo**: Un chatbot simple responde a preguntas básicas de los usuarios.
- **Interfaz web con Gradio**: Una interfaz intuitiva para interactuar con todas las funcionalidades.

## Requisitos previos

- **Python 3.8+**
- **Pip** (gestor de paquetes de Python)
- **Git** (opcional, para clonar el repositorio)

## Instalación

1. **Clona el repositorio** (o descarga el código fuente):
   ```bash
   git clone https://github.com/<tu-usuario>/LivePollStream.git
   cd LivePollStream

2. **Instala las dependencias:**
   
pip install -r requirements.txt


## Uso

1. **Inicia la aplicación:**

python main.py


2. **Registra un usuario**

En la sección "Registrar Usuario", introduce un nombre de usuario (por ejemplo, user1) y una contraseña (por ejemplo, password123).

Pulsa "Registrar". Deberías ver un mensaje de confirmación.


3. **Inicia sesión**

En la sección "Iniciar Sesión", introduce las credenciales del usuario registrado.

Pulsa "Iniciar Sesión". Recibirás un mensaje con un token de sesión.


4. **Crea una encuesta**

En la sección "Crear Encuesta", introduce una pregunta (por ejemplo, "¿Rojo o Azul?"), las opciones (por ejemplo, rojo,azul), la duración en segundos (por ejemplo, 60), y el tipo de encuesta (por ejemplo, simple).

Pulsa "Crear Encuesta". La encuesta aparecerá en el dropdown "Seleccionar Encuesta".


5. **Vota en una encuesta**

Selecciona una encuesta en "Seleccionar Encuesta".

Elige una opción en "Opción" (por ejemplo, rojo).

Pulsa "Votar". Recibirás un mensaje de confirmación, y un token NFT se generará y aparecerá en "Tus Tokens NFT".


6. **Visualiza los resultados""

En la sección "Resultados de la Encuesta",


7. **Transfiere un token**

Registra otro usuario (por ejemplo, user2).

En la sección "Tus Tokens NFT", copia el Token ID de un token.

Introduce el Token ID en "ID del Token a Transferir" y el nombre del nuevo propietario (por ejemplo, user2) en "Nuevo Propietario".

Pulsa "Transferir Token". El token debería transferirse a user2.


8. **Interactúa con el chatbot**

En la sección "Chatbot", escribe una pregunta (por ejemplo, "Hola").

Pulsa "Enviar Pregunta". El chatbot debería responder (por ejemplo, user1, ¡Hola! ¿En qué puedo ayudarte?).


## Diagrama de flujo del sistema LivePollSteam
graph TD
    subgraph "Usuario"
        U[Usuario]
    end

    subgraph "Interfaz (GradioUI)"
        G[GradioUI]
        G_UI[Interfaz Web]
        G_CreatePoll[Crear Encuesta]
        G_Vote[Votar]
        G_Transfer[Transferir Token]
        G_Chat[Chatbot]
        G_Results[Mostrar Resultados]
    end

    subgraph "Servicios"
        S_Poll[PollService]
        S_NFT[NFTService]
        S_Chatbot[ChatbotService]
    end

    subgraph "Repositorios (Almacenamiento)"
        R_Encuesta[EncuestaRepository<br>polls.json, votes.json]
        R_NFT[NFTRepository<br>nfts.json]
        R_Usuario[UsuarioRepository<br>users.json]
    end

    %% Flujo de interacción del usuario
    U -->|Accede| G_UI
    G_UI -->|Registra/Inicio Sesión| G
    G -->|Verifica| R_Usuario

    %% Crear encuesta
    G_UI -->|Crear Encuesta| G_CreatePoll
    G_CreatePoll -->|create_poll| S_Poll
    S_Poll -->|Guarda Encuesta| R_Encuesta
    S_Poll -->|Devuelve poll_id| G_CreatePoll
    G_CreatePoll -->|Actualiza poll_list| G_UI

    %% Votar
    G_UI -->|Vota| G_Vote
    G_Vote -->|vote| S_Poll
    S_Poll -->|Verifica Voto| R_Encuesta
    S_Poll -->|Guarda Voto| R_Encuesta
    S_Poll -->|mint_token| S_NFT
    S_NFT -->|Guarda Token| R_NFT
    S_NFT -->|Actualiza Tokens del Usuario| R_Usuario
    S_NFT -->|Devuelve Token| S_Poll
    S_Poll -->|Devuelve Resultado| G_Vote
    G_Vote -->|Actualiza token_list y results_table| G_UI

    %% Ver resultados
    G_UI -->|Selecciona Encuesta| G_Results
    G_Results -->|get_partial_results| S_Poll
    S_Poll -->|Obtiene Votos| R_Encuesta
    S_Poll -->|Calcula Porcentajes| G_Results
    G_Results -->|Actualiza results_table| G_UI

    %% Transferir token
    G_UI -->|Transfiere Token| G_Transfer
    G_Transfer -->|transfer_token| S_NFT
    S_NFT -->|Verifica Token| R_NFT
    S_NFT -->|Verifica Nuevo Propietario| R_Usuario
    S_NFT -->|Actualiza Propietario| R_NFT
    S_NFT -->|Actualiza Lista de Tokens| R_Usuario
    S_NFT -->|Devuelve Resultado| G_Transfer
    G_Transfer -->|Actualiza token_list| G_UI

    %% Interactuar con el chatbot
    G_UI -->|Envia Pregunta| G_Chat
    G_Chat -->|respond| S_Chatbot
    S_Chatbot -->|Genera Respuesta| G_Chat
    G_Chat -->|Muestra Respuesta| G_UI


   
