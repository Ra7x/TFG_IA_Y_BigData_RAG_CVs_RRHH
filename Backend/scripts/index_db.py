import os
import json
import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
from pathlib import Path
import dotenv

dotenv.load_dotenv()

# Configuración (Ajusta la IP si es necesario)
JSON_DIR = os.getenv("JSON_DIR")
DB_PATH = os.getenv("DB_PATH")

ollama_ef = OllamaEmbeddingFunction(
    model_name="nomic-embed-text",
    url="http://100.126.71.20:11434/api/embeddings",
)

client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(
    name="cv_collection",
    embedding_function=ollama_ef
)

def indexar():
    archivos = list(Path(JSON_DIR).glob("*.json"))
    
    for ruta in archivos:
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # --- SELECCIÓN DE TEXTO PARA EL VECTOR ---
            # Si el matchmaking_summary falló, usamos el job_title y tech_stack
            texto_para_vector = f"""
            Nombre: {data.get('full_name')}
            Rol: {data.get('matchmaking_summary')}
            Tecnologías: {', '.join(data.get('tech_stack', []))}
            Experiencia: {str(data.get('work_history'))}
            """

            collection.add(
                ids=[ruta.stem],
                documents=[texto_para_vector], # Ahora el vector tiene muchísima más info para comparar
                metadatas=[metadatos]
            )

            # --- PREPARACIÓN DE METADATOS (Solo tipos simples) ---
            metadatos = {
                "full_name": str(data.get("full_name", "Unknown")),
                "location": str(data.get("location") or "Not Specified"),
                "english_level": str(data.get("english_level", "Not specified")),
                # Convertimos la lista de skills a un solo string para que Chroma lo acepte
                "skills": ", ".join(data.get("tech_stack", []))[:500] # Limitamos largo
            }

            # Insertar
            collection.add(
                ids=[ruta.stem],
                documents=[texto_para_vector],
                metadatas=[metadatos]
            )
            print(f"✅ Indexado correctamente: {ruta.stem}")

        except Exception as e:
            print(f"❌ Error en {ruta.name}: {e}")

if __name__ == "__main__":
    indexar()