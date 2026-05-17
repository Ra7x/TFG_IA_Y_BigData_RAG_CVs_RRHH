import pymupdf4llm
import pathlib
import os
import dotenv

# Cargar variables de entorno desde el archivo .env
dotenv.load_dotenv()
INPUT_DIR = os.getenv('INPUT_DIR') 
OUTPUT_DIR = os.getenv('MARKDOWN_DIR')

def crear_carpeta_markdowns(directorio_salida):
    if not os.path.exists(directorio_salida):
        os.makedirs(directorio_salida)
        print(f"✅ Carpeta '{directorio_salida}' creada.")

def convertir_cvs_a_markdown(directorio_entrada, directorio_salida):
    # Listar archivos PDF
    archivos_pdf = list(pathlib.Path(directorio_entrada).glob("*.pdf"))
    
    if not archivos_pdf:
        print("❌ No se encontraron archivos PDF en la carpeta de entrada.")
        return

    print(f"🚀 Procesando {len(archivos_pdf)} archivos...")

    for pdf_path in archivos_pdf:
        try:
            # Conversion a Markdow
            md_text = pymupdf4llm.to_markdown(str(pdf_path))
            
            # Definir nombre de salida (.md)
            nombre_salida = pdf_path.stem + ".md"
            ruta_salida = os.path.join(directorio_salida, nombre_salida)
            
            # Guardar el archivo
            with open(ruta_salida, "w", encoding="utf-8") as f:
                f.write(md_text)
            
            print(f"Convertido: {pdf_path.name} -> {nombre_salida}")
            
        except Exception as e:
            print(f"Error al convertir {pdf_path.name}: {e}")

if __name__ == "__main__":
    crear_carpeta_markdowns(INPUT_DIR)
    convertir_cvs_a_markdown(INPUT_DIR, OUTPUT_DIR)