import requests
import json
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import aggregation

# Configuración de GitHub
REPO = "Serdan1/LivePollStream"  # Repositorio público
BRANCH = "firebase-integration"  # Rama específica
JSON_PATH = "data"  # Carpeta con los JSON
TOKEN = ""  # No necesario para repositorio público

# Configuración de Firebase
CRED_PATH = "firebase-adminsdk.json" 
PROJECT_ID = "livepollstream"  # ID del proyecto

# Inicializar Firebase
try:
    cred = credentials.Certificate(CRED_PATH)
    firebase_admin.initialize_app(cred, {"projectId": PROJECT_ID})
    db = firestore.client()
    print("Conectado a Firebase Firestore")
except Exception as e:
    print(f"Error al conectar a Firebase: {e}")
    exit(1)

# Configurar headers para la API de GitHub
headers = {"Accept": "application/vnd.github.v3+json"}
if TOKEN:
    headers["Authorization"] = f"token {TOKEN}"

# Verificar acceso al repositorio
repo_url = f"https://api.github.com/repos/{REPO}"
print(f"Verificando repositorio: {repo_url}")
try:
    repo_response = requests.get(repo_url, headers=headers)
    repo_response.raise_for_status()
    print("Repositorio encontrado")
except requests.exceptions.RequestException as e:
    print(f"Error al acceder al repositorio: {e}")
    exit(1)

# Verificar rama
branch_url = f"https://api.github.com/repos/{REPO}/branches/{BRANCH}"
print(f"Verificando rama: {branch_url}")
try:
    branch_response = requests.get(branch_url, headers=headers)
    branch_response.raise_for_status()
    print("Rama encontrada")
except requests.exceptions.RequestException as e:
    print(f"Error al acceder a la rama: {e}")
    exit(1)

# Obtener lista de archivos JSON
url = f"https://api.github.com/repos/{REPO}/contents/{JSON_PATH}?ref={BRANCH}"
print(f"Accediendo a: {url}")
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    files = response.json()
    print(f"Archivos encontrados: {[f['name'] for f in files if isinstance(f, dict)]}")
except requests.exceptions.RequestException as e:
    print(f"Error accediendo a GitHub: {e}")
    try:
        if response.status_code == 404:
            print("Causas posibles:")
            print(f"- Verifica que el repositorio existe: https://github.com/{REPO}")
            print(f"- Verifica que la rama existe: https://github.com/{REPO}/tree/{BRANCH}")
            print(f"- Verifica que la carpeta data/ existe: https://github.com/{REPO}/tree/{BRANCH}/{JSON_PATH}")
    except NameError:
        print("Error de conexión o respuesta.")
    exit(1)

# Procesar cada archivo JSON
json_files = {
    "nfts.json": "nfts",
    "polls.json": "polls",
    "users.json": "users",
    "votes.json": "votes"
}

for file_info in files:
    if isinstance(file_info, dict) and file_info["name"] in json_files:
        file_url = file_info["download_url"]
        collection_name = json_files[file_info["name"]]
        try:
            file_response = requests.get(file_url)
            file_response.raise_for_status()
            data = json.loads(file_response.text)
            if isinstance(data, dict):
                data = [data]
            # Importar a Firestore
            collection_ref = db.collection(collection_name)
            for doc in data:
                # Usar un campo como ID (id, poll_id, user_id, vote_id, nft_id) o un hash
                doc_id = doc.get("id", doc.get("poll_id", doc.get("user_id", doc.get("vote_id", doc.get("nft_id", str(hash(str(doc))))))))
                collection_ref.document(str(doc_id)).set(doc)
            print(f"Importado {file_info['name']} a la colección {collection_name}")
        except requests.exceptions.RequestException as e:
            print(f"Error descargando {file_info['name']}: {e}")
        except json.JSONDecodeError:
            print(f"Error: {file_info['name']} no es un JSON válido")
        except Exception as e:
            print(f"Error insertando {file_info['name']} en Firestore: {e}")

# Contar documentos en una colección
collection_ref = db.collection("polls")
docs = collection_ref.get()
print(f"Total de documentos en polls: {len(docs)}")

# Estadísticas básicas
# 1. Promedio de votos en polls
try:
    collection_ref = db.collection("polls")
    query = collection_ref
    agg_query = aggregation.AggregationQuery(query).avg("votes", alias="promedio_votos")
    result = agg_query.get()
    for res in result:
        print(f"Promedio de votos en polls: {res[0]['promedio_votos']}")
except Exception as e:
    print(f"Error al calcular promedio de votos: {e}")

# 2. Usuarios por edad
try:
    ages = {}
    for doc in db.collection("users").stream():
        age = doc.to_dict().get("age")
        if age is not None:
            ages[age] = ages.get(age, 0) + 1
    for age, count in ages.items():
        print(f"Edad: {age}, Conteo: {count}")
except Exception as e:
    print(f"Error al calcular usuarios por edad: {e}")

print("Importación y estadísticas completadas.")
firebase_admin.delete_app(firebase_admin.get_app())