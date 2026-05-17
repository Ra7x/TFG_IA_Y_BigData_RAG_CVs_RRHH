import os
import instructor
from openai import OpenAI
# Asumiendo que Structured_CV está en tu archivo model.py
from model import Structured_CV 
from pathlib import Path

# --- CONFIGURACIÓN ---
client = instructor.from_openai(
    OpenAI(base_url="http://100.126.71.20:11434/v1", api_key="ollama"),
    mode=instructor.Mode.JSON,
)

def procesar_markdown_a_json(ruta_md, carpeta_destino):
    try:
        with open(ruta_md, "r", encoding="utf-8") as f:
            contenido = f.read()

        # Consolidamos las instrucciones en un solo bloque para el sistema
        instrucciones_sistema = (
            "Eres un experto en reclutamiento técnico y sistema de extracción de datos de RRHH.\n"
            "Tu tarea es normalizar CVs a JSON siguiendo estrictamente el esquema solicitado.\n\n"
            "REGLAS CRÍTICAS:\n"
            "1. NO inventes campos. Usa solo los definidos en el esquema Pydantic.\n"
            "2. El campo 'matchmaking_summary' es OBLIGATORIO; redacta un párrafo analizando al candidato para búsqueda semántica.\n"
            "3. Si un dato no existe, usa [] para listas o null para campos simples.\n"
            "4. Mapea 'Awards', 'Affiliations' o licencias a la lista de 'certifications'.\n"
            "5. Infiere datos lógicos: si tiene certificaciones en inglés, deduce el 'english_level'."
        )

        datos_extraidos = client.chat.completions.create(
            model="deepseek-coder-v2:16b",
            response_model=Structured_CV,
            messages=[
                {"role": "system", "content": instrucciones_sistema},
                {"role": "user", "content": contenido}
            ]
        )

        ruta_guardado = os.path.join(carpeta_destino, Path(ruta_md).stem + ".json")
        os.makedirs(os.path.dirname(ruta_guardado), exist_ok=True)

        with open(ruta_guardado, "w", encoding="utf-8") as f:
            f.write(datos_extraidos.model_dump_json(indent=4))
        
        print(f"Procesado exitosamente: {Path(ruta_md).name} -> {Path(ruta_guardado).name}")

    except Exception as e:
        print(f"Error procesando {ruta_md}: {e}")


if __name__ == "__main__":
    # TODO: tengo que cambiar estas rutas por variables de entorno
    input_folder = "./data/Markdowns"
    output_folder = "./data/JSON"


    # Obtener todos los archivos .md
    archivos_md = [f for f in os.listdir(input_folder) if f.endswith(".md")]

    if not archivos_md:
        print("⚠️ No se encontraron archivos .md en la carpeta de entrada.")
    else:
        print(f"Iniciando procesamiento de {len(archivos_md)} archivos...")
        for archivo in archivos_md:
            ruta_completa = os.path.join(input_folder, archivo)
            procesar_markdown_a_json(ruta_completa, output_folder)
        
        print("\nProceso finalizado.")