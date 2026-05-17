from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os
import requests
import re
from app.db.chroma import collection

router = APIRouter()
JSON_DIR = os.getenv("JSON_DIR")

class QueryRequest(BaseModel):
    prompt: str
    n_results: int = 3

JOB_TITLE_KEYWORDS = {

    'manager', 'director', 'lead', 'chief', 'head', 'responsable', 'gerente', 'coordinador',
    'supervisor', 'administrator', 'administrador', 'consultant', 'consultor', 'officer',
    
    # Tecnología y Diseño
    'engineer', 'developer', 'technician', 'analyst', 'architect', 'designer', 'webmaster',
    'programador', 'ingeniero', 'analista', 'diseñador', 'soporte', 'it', 'qa', 'tester',
    
    # Hostelería y Alimentación (Sector Chef)
    'chef', 'cook', 'cocinero', 'waiter', 'camarero', 'bartender', 'barman', 'hostess',
    'baker', 'pastry', 'maitre', 'repostero', 'catering', 'gastronomy', 'executive',
    
    # Salud y Bienestar
    'doctor', 'nurse', 'enfermero', 'therapist', 'terapeuta', 'psychologist', 'psicólogo',
    'dentist', 'pharmacist', 'veterinary', 'médico', 'auxiliar', 'fisioterapeuta',
    
    # Industria y Oficios
    'mechanic', 'operator', 'operario', 'mantenimiento', 'electrician', 'electricista',
    'welder', 'soldador', 'driver', 'conductor', 'logistics', 'warehouse', 'mozo',
    
    # Educación y Formación
    'instructor', 'trainer', 'teacher', 'profesor', 'educador', 'mentor', 'coach',
    
    # Ventas y Atención al Cliente
    'representative', 'agent', 'agente', 'sales', 'ventas', 'account', 'comercial',
    'associate', 'asociado', 'clerk', 'receptionist', 'recepcionista', 'customer',
    
    # Ciencia e Investigación
    'scientist', 'researcher', 'investigador', 'biologist', 'chemist', 'científico'
}

SKILLS_KEYWORDS = {
    'tecnologia': {
        'frontend', 'backend', 'fullstack', 'react', 'angular', 'vue', 'javascript', 'js', 
        'typescript', 'css', 'html', 'python', 'java', 'c#', 'php', 'node', 'sql', 'nosql', 
        'aws', 'docker', 'kubernetes', 'git', 'api', 'rest'
    },
    'hosteleria': {
        'reposteria', 'pasteleria', 'pan', 'croissants', 'baguettes', 'masa madre', 'horno', 
        'postres', 'vinos', 'cocteleria', 'servicio de mesa', 'manipulacion de alimentos',
        'cocina mediterranea', 'sushi', 'grill', 'chef de partie'
    },
    'administracion_ventas': {
        'excel', 'sap', 'crm', 'contabilidad', 'facturacion', 'nominas', 'ventas frias', 
        'negociacion', 'atencion al cliente', 'marketing', 'seo', 'sem', 'redes sociales'
    },
    'industria_oficios': {
        'soldadura', 'cnc', 'mecanica', 'electricidad', 'fontaneria', 'logistica', 
        'carretilla', 'puente grua', 'prevencion de riesgos', 'mantenimiento preventivo'
    }
}

def is_likely_job_title(text):
    """Detecto si un texto probablemente sea un puesto de trabajo"""
    if not text:
        return False
    
    # Limpio el texto para una comparación más robusta
    lower_text = text.lower().strip()
    
    # 1. Comprobación directa: ¿Alguna de nuestras palabras clave está en el texto?
    if any(keyword in lower_text for keyword in JOB_TITLE_KEYWORDS):
        return True
        
    # 2. Heurística extra: Si el texto es muy largo y no tiene espacios, 
    # o si contiene números de años, suele ser un puesto o fecha, no un nombre.
    if len(lower_text) > 50 or any(char.isdigit() for char in lower_text):
        return True
        
    return False

def extract_location_from_company(company_str):
    if not company_str or company_str.lower() == 'company name':
        return None
    parts = company_str.split(',', 1)
    if len(parts) > 1:
        return parts[1].strip()
    return None

def detectar_skills_clave(prompt):
    prompt_lower = prompt.lower()
    skills_detectadas = []
    for sector, lista in SKILLS_KEYWORDS.items():
        for skill in lista:
            if skill in prompt_lower:
                skills_detectadas.append(skill)
    return skills_detectadas

def extraer_n_resultados(prompt):
    """Detecta si el usuario pide un número específico de resultados"""
    prompt_lower = prompt.lower()
    numeros_texto = {"uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5, "diez": 10}
    
    # Buscar dígitos
    match = re.search(r'\b(\d+)\b', prompt_lower)
    if match:
        return int(match.group(1))
    
    # Buscar palabras
    for palabra, valor in numeros_texto.items():
        if palabra in prompt_lower:
            return valor
    return None

def normalize_candidate_data(cv_data):
    full_name = cv_data.get('full_name', '').strip()
    work_history = cv_data.get('work_history', [])
    first_job_title = work_history[0].get('job_title', '') if work_history else ''
    first_company = work_history[0].get('company', '') if work_history else ''
    
    if not full_name or full_name in ['Candidate Name', 'Not Specified', '']:
        display_name = first_job_title or 'Candidato'
    elif is_likely_job_title(full_name):
        display_name = first_job_title or full_name
    else:
        display_name = full_name
    
    location = cv_data.get('location')
    if not location:
        location = extract_location_from_company(first_company)
    
    return {
        'full_name': display_name,
        'location': location or 'Ubicación no especificada',
        'english_level': cv_data.get('english_level', 'No especificado'),
        'tech_stack': cv_data.get('tech_stack', []),
        'matchmaking_summary': cv_data.get('matchmaking_summary', ''),
        'summary': cv_data.get('summary', 'Sin resumen disponible.'),
        'work_history': work_history,
        'education': cv_data.get('education', []),
        'certifications': cv_data.get('certifications', [])
    }

def generar_respuesta_ia(prompt_usuario, candidatos):
    skills = detectar_skills_clave(prompt_usuario)
    mencion_skills = f" Pon especial atención a las habilidades: {', '.join(skills)}." if skills else ""
    contexto = ""

    # Solo usamos el TOP 3 para el razonamiento de la IA
    for c in candidatos[:3]:
        nombre = c['data'].get('full_name')
        resumen = c['data'].get('matchmaking_summary') or "Perfil técnico calificado."
        score = c['score']
        contexto += f"- {nombre} (Match: {score}%): {resumen}\n"

    prompt_final = f"""
    
    Eres un experto en Selección de Personal (Headhunter) y bilingüe, lo que quiere decir que eres capaz de entender y cominicarte en el idioma necesario . El cliente dice: "{prompt_usuario}"
    
    Habilidades destacadas en la consulta: {', '.join(skills) if skills else 'Ninguna detectada'}.{mencion_skills}

    Perfiles encontrados en la base de datos:
    {contexto}
    
    Instrucción: Responde al cliente de forma natural y profesional en el idioma necesario. 
    Explica brevemente por qué estos candidatos son relevantes. 
    Si el usuario pidió un número específico de candidatos, confirma que se los estás mostrando.
    Máximo 2 párrafos cortos.
    """

    try:
        response = requests.post(
            "http://100.126.71.20:11434/api/generate", 
            json={
                "model": "deepseek-coder-v2:16b", 
                "prompt": prompt_final,
                "stream": False,
                "options": {
                    "num_predict": 350,
                    "temperature": 0.5
                }
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json().get('response', "Aquí tienes los perfiles seleccionados:")
    except Exception as e:
        print(f"Error en Ollama: {e}")
        return "He encontrado estos candidatos que coinciden con tu búsqueda:"

@router.post("/search")
async def search_cvs(request: QueryRequest):
    if not JSON_DIR or not os.path.isdir(JSON_DIR):
        raise HTTPException(status_code=500, detail="Error de configuración: JSON_DIR no válido")

    try:
        # Lógica dinámica de cantidad de resultados
        n_dinamico = extraer_n_resultados(request.prompt)
        num_final = n_dinamico if n_dinamico else request.n_results

        results = collection.query(
            query_texts=[request.prompt],
            n_results=num_final
        )

        final_results = []
        for i in range(len(results['ids'][0])):
            cv_id = results['ids'][0][i]
            distancia = results['distances'][0][i]
            path_json = os.path.join(JSON_DIR, f"{cv_id}.json")

            if os.path.exists(path_json):
                with open(path_json, "r", encoding="utf-8") as f:
                    full_cv_data = json.load(f)
                normalized_data = normalize_candidate_data(full_cv_data)
                final_results.append({
                    "id": cv_id,
                    "score": round((1 - distancia) * 100, 2),
                    "data": normalized_data
                })

        if final_results:
            texto_ia = generar_respuesta_ia(request.prompt, final_results)
        else:
            texto_ia = "No he encontrado perfiles que coincidan con tu búsqueda."

        print(f"Consulta: {request.prompt}")
        print(f"Resultados encontrados: {len(final_results)}")
        print(f"Respuesta de la IA: {texto_ia}")
        print(f"Detalles de los candidatos: {final_results}")

        return {
            "answer": texto_ia, 
            "matches": final_results
        }
    
    except Exception as e:
        print(f"Error crítico: {e}")
        raise HTTPException(status_code=500, detail=str(e))