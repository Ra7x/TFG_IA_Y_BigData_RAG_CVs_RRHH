import os
import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
from dotenv import load_dotenv

load_dotenv()

# Configuración centralizada
DB_PATH = os.getenv("DB_PATH")
OLLAMA_URL = "http://100.126.71.20:11434/api/embeddings"

def get_collection():
    ollama_ef = OllamaEmbeddingFunction(
        model_name="nomic-embed-text",
        url=OLLAMA_URL,
    )
    client = chromadb.PersistentClient(path=DB_PATH)
    return client.get_or_create_collection(name="cv_collection", embedding_function=ollama_ef)

collection = get_collection()
