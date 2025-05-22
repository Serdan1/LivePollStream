import requests
import json
import pymongo
from pymongo import MongoClient

# Configuración de GitHub
REPO = "Serdan1/LivePollStream"
BRANCH = "mongodb-integration"
JSON_PATH = "data"
TOKEN = ""  # Repositorio público

# Configuración de MongoDB Atlas
MONGO_URI = "mongodb+srv://danserrano1:e8Bg4LXI0hPxNbso@livepollstream.wv5rwu3.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "livepoll"

# Conectar a MongoDB Atlas
try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    print("Conectado a MongoDB Atlas")
except pymongo.errors.ConnectionError as e:
    print(f"Error al conectar a MongoDB: {e}")
    exit(1)

# Lista de archivos JSON y sus colecciones
json_files = {
    "nfts.json": "nfts",
    "polls.json": "polls",
    "users.json": "users",
    "votes.json": "votes"
}

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
print(f"Intentando acceder a: {url}")
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    files = response.json()
    print(f"Archivos encontrados: {[f['name'] for f in files if isinstance(f, dict)]}")
except requests.exceptions.RequestException as e:
    print(f"Error al acceder a GitHub: {e}")
    try:
        if response.status_code == 404:
            print("Posibles causas:")
            print(f"- Verifica que el repositorio existe: https://github.com/{REPO}")
            print(f"- Verifica que la rama existe: https://github.com/{REPO}/tree/{BRANCH}")
            print(f"- Verifica que la carpeta data/ existe: https://github.com/{REPO}/tree/{BRANCH}/{JSON_PATH}")
    except NameError:
        print("Error de conexión o respuesta no disponible.")
    exit(1)

# Procesar cada archivo JSON
for file_info in files:
    if isinstance(file_info, dict) and file_info["name"] in json_files:
        file_url = file_info["download_url"]
        collection_name = json_files[file_info["name"]]
        collection = db[collection_name]
        try:
            file_response = requests.get(file_url)
            file_response.raise_for_status()
            data = json.loads(file_response.text)
            if isinstance(data, dict):
                data = [data]
            collection.insert_many(data)
            print(f"Importado {file_info['name']} a la colección {collection_name}")
        except requests.exceptions.RequestException as e:
            print(f"Error al descargar {file_info['name']}: {e}")
        except json.JSONDecodeError:
            print(f"Error: {file_info['name']} no es un JSON válido")
        except pymongo.errors.PyMongoError as e:
            print(f"Error al insertar {file_info['name']} en MongoDB: {e}")

print("Importación completada.")
client.close()