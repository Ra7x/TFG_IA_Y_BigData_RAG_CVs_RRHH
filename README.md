# TFG: Sistema de Matchmaking Inteligente para RRHH

## 🎯 Descripción General

Sistema de inteligencia artificial aplicado a Recursos Humanos que utiliza **embeddings vectoriales** y **búsqueda semántica** para realizar matching automático entre perfiles de candidatos y requisitos de puesto. La plataforma transforma datos curriculares no estructurados en representaciones vectoriales, permitiendo consultas en lenguaje natural para encontrar candidatos afines de manera eficiente.

**Estado del Proyecto:** Trabajo de Fin de Grado (TFG) - 2026

---

## 📋 Tabla de Contenidos

- [Características Principales](#características-principales)
- [Arquitectura del Sistema](#arquitectura-del-sistema)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
  - [Backend](#backend)
  - [Frontend](#frontend)
- [Configuración](#configuración)
- [Cómo Ejecutar](#cómo-ejecutar)
- [Flujo de Datos](#flujo-de-datos)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [API REST](#api-rest)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Licencia](#licencia)

---

## ✨ Características Principales

- **🤖 Embeddings Vectoriales**: Integración con Ollama para generar representaciones semánticas de currículos
- **🔍 Búsqueda Semántica**: Consultas en lenguaje natural sin necesidad de palabras clave exactas
- **💾 Base de Datos Vectorial**: ChromaDB como almacenamiento persistente de embeddings
- **🎨 Interfaz Web Moderna**: React + Tailwind CSS con chat interactivo
- **⚡ API RESTful**: FastAPI con endpoints documentados automáticamente
- **🔐 CORS Habilitado**: Comunicación segura Frontend-Backend
- **📊 Normalización de Datos**: Mapeo inteligente de campos CV para presentación consistente
- **♿ Interfaz Conversacional**: Chat amigable para búsqueda de candidatos

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React)                         │
│  - Chat Interface (MessageBubble)                               │
│  - Candidate Results Cards (CandidateResults)                   │
│  - Input Component (ChatInput)                                  │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP/REST
                         │ axios
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    API REST (FastAPI)                            │
│  - POST /api/v1/search                                          │
│  - Normalización de datos                                       │
│  - Control de acceso                                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│               VECTOR SEARCH (Chroma DB)                         │
│  - Query semántica con embeddings                               │
│  - Almacenamiento persistente                                   │
│  - Similitud de coseno                                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│           EMBEDDINGS (Ollama - nomic-embed-text)               │
│  - Generación de vectores semánticos                           │
│  - Dimensionalidad: 768                                        │
│  - Modelo: nomic-embed-text (CPU optimizado)                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 Requisitos Previos

### Sistema
- **Python**: 3.9 o superior
- **Node.js**: 16.x o superior (para Frontend)
- **npm**: 8.x o superior

### Servicios Externos
- **Ollama**: Servidor de embeddings activo en `http://100.126.71.20:11434`
  - Modelo instalado: `nomic-embed-text`
  - Uso: Generación de vectores semánticos para CVs

### Recursos
- **Memoria RAM**: Mínimo 4GB
- **Espacio en Disco**: 2GB (para base de datos vectorial + datos JSON)

---

## 🚀 Instalación

### Backend

#### 1. Clonar y navegar al directorio
```bash
cd Backend
```

#### 2. Crear entorno virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

**Dependencias principales:**
- `fastapi` - Framework web asincrónico
- `chromadb` - Base de datos vectorial
- `pydantic` - Validación de datos
- `python-dotenv` - Gestión de variables de entorno
- `pymupdf4llm` - Procesamiento de PDFs
- `instructor` - Validación de esquemas
- `openai` - Integraciones de IA (opcional)

#### 4. Configurar archivo `.env`
```bash
# Backend/.env
JSON_DIR="C:/Users/Ra7x/Desktop/Big Data e IA/TFG/Backend/data/JSON"
DB_PATH="./vector_db"
```

**Variables:**
- `JSON_DIR`: Ruta a los archivos JSON de currículos procesados
- `DB_PATH`: Ruta para almacenar la base de datos de ChromaDB

---

### Frontend

#### 1. Navegar al directorio
```bash
cd Frontend/rrhh_chatbot
```

#### 2. Instalar dependencias
```bash
npm install
```

**Dependencias principales:**
- `react@^19` - Librería UI
- `axios@^1.16` - Cliente HTTP
- `tailwindcss@^3.4` - Framework CSS
- `vite@^8` - Build tool

#### 3. Configurar servidor API
Editar `src/services/api.js`:
```javascript
const api = axios.create({
    baseURL: 'http://100.90.201.104:8000/api/v1',  // Ajusta según tu entorno
});
```

---

## ⚙️ Configuración

### Backend

#### Estructura de directorios requerida
```
Backend/
├── data/
│   ├── JSON/          # Currículos procesados (*.json)
│   ├── Curriculums/   # CVs originales (PDF/DOCX)
│   └── Markdowns/     # CVs convertidos a MD
├── vector_db/         # Base de datos ChromaDB (creada automáticamente)
├── app/
│   ├── main.py
│   ├── api/
│   │   └── search.py
│   └── db/
│       └── chroma.py
└── scripts/
    ├── index_db.py          # Script para indexar CVs
    └── json_generator.py    # Script para generar JSONs
```

#### Generar/indexar datos
```bash
# Indexar CVs en la base de datos vectorial
python scripts/index_db.py
```

Este script:
1. Lee todos los JSONs en `data/JSON/`
2. Genera embeddings usando Ollama
3. Almacena vectores en ChromaDB
4. Crea índices de búsqueda semántica

---

## ▶️ Cómo Ejecutar

### Terminal 1: Backend
```bash
cd Backend
source venv/bin/activate  # o venv\Scripts\activate en Windows
python -m app.main
```

**Salida esperada:**
```
INFO:     Application startup complete
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Acceso:**
- API REST: `http://localhost:8000`
- Documentación Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Terminal 2: Frontend
```bash
cd Frontend/rrhh_chatbot
npm run dev
```

**Salida esperada:**
```
VITE v8.0.11  ready in 234 ms

➜  Local:   http://localhost:5173/
➜  press h to show help
```

### Terminal 3: Ollama (si está en tu máquina)
```bash
ollama serve
```

---

## 🔄 Flujo de Datos

### 1️⃣ Fase de Preparación (Offline)

```
┌──────────────────────────┐
│ Currículos (PDF/DOCX)    │
│ data/Curriculums/        │
└──────────────┬───────────┘
               │
               ▼
┌──────────────────────────────────────┐
│ json_generator.py                    │
│ - Parse CV                           │
│ - Extrae: nombre, skills, exp, edu   │
│ - Genera resumen IA                  │
└──────────────┬──────────────────────┘
               │
               ▼
┌──────────────────────────┐
│ CVs JSON Procesados      │
│ data/JSON/               │
│ (ej: 10001727.json)      │
└──────────────┬───────────┘
               │
               ▼
┌──────────────────────────────────────┐
│ index_db.py (scripts/index_db.py)    │
│ - Lee cada JSON                      │
│ - Extrae texto para embeddings       │
│ - Normaliza metadatos                │
└──────────────┬──────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│ Ollama Embeddings                    │
│ http://100.126.71.20:11434           │
│ modelo: nomic-embed-text             │
│ Salida: vector de 768 dimensiones    │
└──────────────┬──────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│ ChromaDB Vector Store                │
│ vector_db/chroma.sqlite3             │
│ Colección: cv_collection             │
│ - Vectores indexados                 │
│ - Metadatos almacenados              │
└──────────────────────────────────────┘
```

### 2️⃣ Fase de Consulta (Interactivo)

```
┌────────────────────────────┐
│ Usuario escribe consulta   │
│ "Busco senior developer"   │
└────────────────┬───────────┘
                 │
                 ▼
    ┌─────────────────────────┐
    │ Frontend (React)        │
    │ ChatWindow              │
    └────────────┬────────────┘
                 │ axios.post()
                 ▼
┌─────────────────────────────────────┐
│ POST /api/v1/search                 │
│ payload: {                          │
│   "prompt": "Busco senior developer"│
│   "n_results": 3                    │
│ }                                   │
└────────────────┬────────────────────┘
                 │
                 ▼
    ┌─────────────────────────────┐
    │ FastAPI search endpoint     │
    │ app/api/search.py           │
    └────────────────┬────────────┘
                     │
                     ▼
    ┌─────────────────────────────────┐
    │ Ollama: Generar embedding       │
    │ input: "Busco senior developer" │
    │ output: vector[768]             │
    └────────────────┬────────────────┘
                     │
                     ▼
    ┌─────────────────────────────────┐
    │ ChromaDB: Query semántica       │
    │ - Similitud de coseno           │
    │ - Top 3 resultados              │
    │ - Calcula: distance             │
    └────────────────┬────────────────┘
                     │
                     ▼
    ┌─────────────────────────────────┐
    │ Lectura JSON complementarios    │
    │ data/JSON/{cv_id}.json          │
    │ - Datos completos del CV        │
    │ - Información normalizada       │
    └────────────────┬────────────────┘
                     │
                     ▼
    ┌─────────────────────────────────┐
    │ Normalización de datos          │
    │ - Nombre (inteligente)          │
    │ - Ubicación (from company)      │
    │ - Score: (1 - distance) * 100   │
    └────────────────┬────────────────┘
                     │
                     ▼
    ┌─────────────────────────────────┐
    │ Response JSON                   │
    │ {                               │
    │   "matches": [                  │
    │     {                           │
    │       "id": "10001727",         │
    │       "score": 85.32,           │
    │       "data": { ... }           │
    │     },                          │
    │     ...                         │
    │   ]                             │
    │ }                               │
    └────────────────┬────────────────┘
                     │
                     ▼
    ┌─────────────────────────────────┐
    │ Frontend renderiza tarjetas     │
    │ CandidateResults.jsx            │
    │ - Nombre del candidato          │
    │ - Ubicación                     │
    │ - Score de coincidencia         │
    │ - Skills destacadas             │
    │ - Chip de CV interactivo        │
    └─────────────────────────────────┘
```

### 3️⃣ Estructura de Datos JSON

**Ejemplo: `data/JSON/10001727.json`**
```json
{
  "full_name": "Sous Chef / Candidato",
  "location": null,
  "english_level": "Not specified",
  "tech_stack": [],
  "summary": null,
  "matchmaking_summary": "El candidato tiene experiencia en cocina profesional...",
  "work_history": [
    {
      "job_title": "Sous Chef",
      "company": "Company Name",
      "period": "Jul 2010 to Present",
      "description": ["Assist cooks...", "Worked sauté..."],
      "technologies": []
    }
  ],
  "education": [
    {
      "degree": "Master's",
      "institution": "Stratford University",
      "year": 2015
    }
  ],
  "certifications": [
    {
      "name": "CPR-AED Certified",
      "year": null
    }
  ]
}
```

---

## 📁 Estructura del Proyecto

```
TFG/
├── README.md                          # Este archivo
│
├── Backend/                           # API y procesamiento
│   ├── .env                           # Variables de entorno
│   ├── requirements.txt               # Dependencias Python
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # Aplicación FastAPI
│   │   ├── api/
│   │   │   └── search.py              # Endpoint de búsqueda semántica
│   │   └── db/
│   │       └── chroma.py              # Conexión a ChromaDB
│   ├── data/
│   │   ├── Curriculums/               # CVs originales (PDF/DOCX)
│   │   ├── JSON/                      # CVs procesados
│   │   └── Markdowns/                 # Versiones Markdown
│   ├── vector_db/                     # Base de datos vectorial
│   │   └── chroma.sqlite3
│   └── scripts/
│       ├── index_db.py                # Indexar CVs en ChromaDB
│       ├── json_generator.py          # Generar JSONs desde PDFs
│       ├── markdown_generator.py      # Convertir CVs a Markdown
│       └── model.py                   # Modelos de datos
│
├── Frontend/
│   └── rrhh_chatbot/                  # Aplicación React
│       ├── package.json
│       ├── vite.config.js
│       ├── tailwind.config.js
│       ├── index.html
│       ├── src/
│       │   ├── main.jsx
│       │   ├── App.jsx
│       │   ├── App.css
│       │   ├── index.css
│       │   ├── components/
│       │   │   ├── chat/
│       │   │   │   ├── ChatWindow.jsx    # Contenedor del chat
│       │   │   │   ├── MessageBubble.jsx # Burbujas de mensaje
│       │   │   │   └── ChatInput.jsx     # Input de usuario
│       │   │   └── results/
│       │   │       └── CandidateResults.jsx  # Tarjetas de candidatos
│       │   └── services/
│       │       └── api.js               # Cliente API (axios)
│       ├── public/
│       └── dist/                        # Build generado
│
└── vector_db/                          # Base de datos vectorial (raíz del proyecto)
    └── chroma.sqlite3
```

---

## 🔌 API REST

### Endpoint Principal

#### `POST /api/v1/search`

Realiza búsqueda semántica de candidatos.

**Request:**
```json
{
  "prompt": "Busco ingeniero fullstack con experiencia en React",
  "n_results": 3
}
```

**Response:**
```json
{
  "matches": [
    {
      "id": "10001727",
      "score": 87.45,
      "data": {
        "full_name": "Senior Software Engineer",
        "location": "Madrid, España",
        "english_level": "Fluent",
        "tech_stack": ["React", "Node.js", "PostgreSQL", "Docker"],
        "matchmaking_summary": "Candidato con experiencia en desarrollo full-stack...",
        "work_history": [...],
        "education": [...],
        "certifications": [...]
      }
    },
    ...
  ]
}
```

**Parámetros:**
- `prompt` (string, requerido): Consulta en lenguaje natural
- `n_results` (int, opcional): Número de resultados (default: 3)

**Códigos de respuesta:**
- `200 OK`: Búsqueda exitosa
- `400 Bad Request`: JSON inválido
- `500 Internal Server Error`: Error del servidor

**Ejemplo con cURL:**
```bash
curl -X POST http://localhost:8000/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Desarrollador Python con experiencia en machine learning",
    "n_results": 5
  }'
```

---

## 🛠️ Tecnologías Utilizadas

### Backend
| Tecnología | Versión | Propósito |
|-----------|---------|----------|
| Python | 3.9+ | Lenguaje principal |
| FastAPI | 0.x | Framework web asincrónico |
| ChromaDB | Latest | Base de datos vectorial |
| Ollama | Local | Generador de embeddings |
| Pydantic | Latest | Validación de esquemas |
| python-dotenv | Latest | Gestión de env variables |

### Frontend
| Tecnología | Versión | Propósito |
|-----------|---------|----------|
| React | 19.2.5 | Framework UI |
| Axios | 1.16.0 | Cliente HTTP |
| Tailwind CSS | 3.4.17 | Framework CSS utilitario |
| Vite | 8.0.10 | Build tool |
| ESLint | 10.x | Linting |

### Infraestructura
| Servicio | Rol |
|---------|-----|
| Ollama | Servicio de embeddings |
| ChromaDB | Almacenamiento vectorial |
| FastAPI | API REST |
| Vite Dev Server | Servidor desarrollo frontend |

---

## 🔐 Seguridad

### CORS
El backend permite acceso desde cualquier origen en desarrollo:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
⚠️ **En producción**, especificar orígenes permitidos:
```python
allow_origins=["https://dominio.com"]
```

### Variables de Entorno
Nunca commitear `.env`:
```bash
# Backend/.gitignore
.env
*.pyc
__pycache__/
venv/
```

---

## 📊 Monitoreo y Logs

### Backend
Los logs de búsqueda se imprimen en consola:
```
CV ID: 10001727, Nombre: Sous Chef, Score: 85.32
CV ID: 10089434, Nombre: IT Technician, Score: 78.91
```

### Frontend
Activar Developer Tools del navegador (F12) para ver requests/responses:
- Network tab: Inspeccionar requests a `/api/v1/search`
- Console: Logs de aplicación

---

## 🐛 Troubleshooting

### Error: "JSON_DIR no es válido"
```
❌ JSON_DIR no es válido o no existe: C:\...
```
**Solución:**
```bash
# Verificar que existe data/JSON/
ls Backend/data/JSON/

# Si no existe, crear estructura:
mkdir -p Backend/data/JSON
```

### Error: "No connection to Ollama"
```
❌ Connection refused to http://100.126.71.20:11434
```
**Solución:**
1. Verificar que Ollama está corriendo
2. Cambiar IP en `app/db/chroma.py` si está en otra máquina
3. Verificar modelo instalado: `ollama list`

### Error: "CORS error"
```
❌ Access to XMLHttpRequest blocked by CORS policy
```
**Solución:**
- Frontend y Backend en desarrollo local: `*` (permite todo)
- En producción: Configurar orígenes específicos en FastAPI

### ChromaDB Database locked
```
❌ database is locked
```
**Solución:**
1. Asegurar que solo una instancia de FastAPI está activa
2. Eliminar `vector_db/chroma.sqlite3-shm` si existe
3. Reiniciar la aplicación

---

## 📈 Posibles Mejoras Futuras

- [ ] Autenticación y autorización (JWT)
- [ ] Filtros avanzados (experiencia, tecnologías, ubicación)
- [ ] Caché de búsquedas frecuentes
- [ ] Modelo de embedding fine-tuned para dominio RRHH
- [ ] Análisis de feedback de usuarios
- [ ] Exportación de resultados (PDF, Excel)
- [ ] Dashboard de analytics
- [ ] Sistema de recomendaciones persistente
- [ ] Soporte para múltiples idiomas en búsqueda
- [ ] Integración con ATS (Applicant Tracking System)

---

## 📄 Licencia

Este proyecto es parte de un Trabajo de Fin de Grado (TFG) de la especialización de Big Data e Inteligencia artificial.  
Todos los derechos reservados © 2026.

---

## 👨‍💻 Autor

**Raúl Moreno Serrano**  
Trabajo de Fin de Grado - Algoritmos de IA aplicados a RRHH

---

## 📞 Contacto y Soporte

Para preguntas o problemas:
1. Revisar la sección [Troubleshooting](#troubleshooting)
2. Consultar los logs del backend y frontend
3. Verificar documentación de dependencias

---

**Última actualización:** Mayo 2026  
**Estado del Servidor:** Desarrollo activo
