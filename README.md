# RAG System - PDF Semantic Search API

Este proyecto implementa un sistema **RAG (Retrieval-Augmented Generation)** usando **FastAPI** para subir PDFs, extraer texto, vectorizarlo y responder preguntas de manera semántica usando embeddings y un LLM.

---

## Funcionalidades principales

1. **Subida de PDFs**
   - Extrae texto de archivos PDF.
   - Divide el contenido en entradas según patrón (numeradas).
   - Genera embeddings con **Sentence Transformers**.
   - Guarda la información en **MongoDB**.

2. **Búsqueda semántica y Q&A**
   - Permite realizar preguntas sobre los PDFs cargados.
   - Encuentra el chunk más similar a la pregunta.
   - Genera una respuesta usando un modelo LLM (OpenRouter).

3. **Tests automatizados**
   - Testea la subida de PDFs y la búsqueda semántica.
   - Verifica la integridad de la base de datos de prueba.

---

## Estructura del proyecto

```
rag_proyecto/
│
├─ app/
│ ├─ controllers/
│ │ ├─ pdf_controller.py
│ │ └─ qa_controller.py
│ ├─ db/
│ │ ├─ mongo.py
│ │ 
│ ├─ llm/
│ │ └─ llm_controller.py
│ ├─ routes/
│ │ ├─ pdf_routes.py
│ │ └─ qa_routes.py
│ │ 
│ └─ main.py
│ └─ config.py 
│ │ 
│ ├─ test/
│    ├─ test_pdf_controller.py
│    └─ test_qa_controller.py
│
├─ docker-compose.yml
├─ requirements.txt
├─ .env.example
└─ README.md
```

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/OscarDeveloperBackend/rag_project.git

cd carpeta
```

2. Ejecutar contenedor con el mongodb 

```
docker-compose up -d 

# Para verificar si se levantó el contenedor
docker ps
```
3. Completar las variables con tus credenciales:

```
MONGO_USER=tu_usuario
MONGO_PASS=tu_password
MONGO_URL=mongodb://user:pass@localhost:27017
DB_NAME=rag_db
COLLECTION_NAME=coleccion_rag
OPEN_ROUTER=tu_api_key_openrouter
```


4. Crear y activar un entorno virtual:

```
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / MacOS
source venv/bin/activate
```

5. Instalar dependencias

```
pip install -r requirements.txt
```


6. Ejecutar el servidor de FastApi
```
uvicorn app.main:app --reload

# API disponible en: http://127.0.0.1:8000

# Documentacion (Swagger UI): http://127.0.0.1:8000/docs
```

## Endpoints disponibles

### POST /pdf/upload

Espera un archivo pdf y en caso desesa limpiar la colección antes de insertar.


### POST /qa/ask

Espera una pregunta, para luego procesarla y generar una respuesta utilizando el modelo LLM.

## Tests automatizados

Testea la subida de PDFs y la búsqueda semántica.

```
# Para probar la cargada de un pdf en data para prueba
PYTHONPATH=. pytest test/test_pdf_controller.py -v --disable-warnings
o

# Para probar la consulta al handler y traerme el resultado mas cercano
PYTHONPATH=. pytest test/test_qa_controller.py -v --disable-warnings

```
