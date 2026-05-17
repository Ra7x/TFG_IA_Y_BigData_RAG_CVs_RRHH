import os, dotenv
from openai import OpenAI

dotenv.load_dotenv()
# Asegúrate de que esta variable apunta a la carpeta de tus .md generados
INPUT_DIR = os.getenv('MARKDOWN_DIR') 

client = OpenAI(base_url="http://100.126.71.20:11434/v1", api_key="ollama")

def analizar_y_generar_pydantic(carpeta_md):
    contenidos = ""
    archivos = [f for f in os.listdir(carpeta_md) if f.endswith('.md')]
    
    if not archivos:
        print(f"❌ No se encontraron archivos .md en {carpeta_md}")
        return

    # Tomamos una muestra representativa (20 es mucho para un prompt si los CVs son largos)
    # Si ves que falla por contexto, baja a 10.
    for archivo in archivos[:10]: 
        ruta_completa = os.path.join(carpeta_md, archivo)
        try:
            with open(ruta_completa, "r", encoding="utf-8-sig") as f:
                # Añadimos un separador claro
                contenidos += f"\n\n--- INICIO CV: {archivo} ---\n" 
                contenidos += f.read()
                contenidos += f"\n--- FIN CV: {archivo} ---\n"
        except Exception as e:
            print(f"⚠️ Error leyendo {archivo}: {e}")
            continue

    prompt = f"""
    Eres un Arquitecto de Datos Senior especializado en RRHH y NLP. 
    A continuación te proporciono {len(archivos[:10])} currículums extraídos en Markdown.
    
    TAREA:
    1. Analiza los patrones comunes de información.
    2. Diseña un modelo de datos en Python usando la librería Pydantic.
    3. El modelo debe ser 'generalista' pero permitir filtros potentes (Matchmaking).
    
    REQUISITOS DEL MODELO:
    - Campo 'seniority': Basado en años y rol (Junior, Mid, Senior, Lead).
    - Campo 'stack_principal' (List[str]) y 'tecnologias_secundarias' (List[str]).
    - Campo 'soft_skills' (List[str]).
    - Campo 'idiomas': Una lista de objetos con 'idioma' y 'nivel_mcer' (A1-C2).
    - Campo 'experiencia_total_años' (float): Cálculo numérico para filtros 'mayor que'.
    - Campo 'proyectos_destacados': Lista de objetos con 'nombre', 'descripcion' y 'tecnologias'.
    - Campo 'analisis_estabilidad': Un string que evalúe si el candidato cambia mucho de empresa.

    POR FAVOR, devuelve ÚNICAMENTE el código Python de la clase Pydantic llamada 'CandidatoEstructurado'. 
    Usa Field() para añadir descripciones a los campos.

    CVs PARA ANALIZAR:
    {contenidos}
    """

    print(f"📡 Analizando {len(archivos[:100])} CVs con DeepSeek-Coder-V2...")
    
    try:
        response = client.chat.completions.create(
            model="deepseek-coder-v2:16b",
            messages=[
                {"role": "system", "content": "Actúa como un experto en ingeniería de datos y Pydantic."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2 # Baja temperatura para mayor consistencia estructural
        )
        
        output = response.choices[0].message.content
        
        # Guardamos la propuesta en un archivo para que lo revises
        with open("modelo_propuesto.py", "w", encoding="utf-8") as f:
            f.write(output)
            
        print("\n✅ Análisis completado. Revisa 'modelo_propuesto.py'")
        print("-" * 30)
        print(output)
        
    except Exception as e:
        print(f"❌ Error en la comunicación: {e}")

if __name__ == "__main__":
    if INPUT_DIR:
        analizar_y_generar_pydantic(INPUT_DIR)
    else:
        print("❌ Error: MARKDOWN_DIR no está definido en el .env")