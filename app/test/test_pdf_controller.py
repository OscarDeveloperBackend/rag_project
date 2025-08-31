import os
import io
import pytest
from app.controllers import pdf_controller  # Importamos el controlador a testear
from app.db.mongo import db # Conexion a MongoDB
from app.config import settings # Variables de entorno


# Fixture de pytest para devolver la ruta del PDF de prueba
@pytest.fixture
def test_pdf_path():

    # Devuelve la ruta del archivo "test.pdf" dentro de la carpeta "data"
    return os.path.join(os.path.dirname(__file__), "data", "test.pdf")


def test_handle_upload_pdf(test_pdf_path, monkeypatch):
    # Abrir el PDF de prueba en modo binario
    with open(test_pdf_path, "rb") as f:
        file_bytes = f.read()

    # Crear un objeto tipo UploadFile simulado
    class FakeUploadFile:
        def __init__(self, filename, bytes_data):
            self.filename = filename
            self.file = io.BytesIO(bytes_data)

    upload_file = FakeUploadFile("test.pdf", file_bytes)

    # Usar colección de prueba
    test_collection_name = "test_collection"
    test_collection = db[test_collection_name]

    # Limpiar coleccion de prueba antes de test
    test_collection.delete_many({})

    # Reemplazar temporalmente settings.COLLECTION_NAME por la de prueba
    monkeypatch.setattr(settings, "COLLECTION_NAME", test_collection_name)

    # Ejecutar handle_upload (ahora apunta a test_collection)
    result = pdf_controller.handle_upload(upload_file, clear=True)

    # Mostrar resultado en terminal
    print("Resultado de handle_upload:", result)

    # Comprobar que se insertaron documentos
    assert "inserted" in result
    assert result["inserted"] > 0

    # Comprobar que la colección contiene los mismos documentos
    docs_in_db = list(test_collection.find({}))
    assert len(docs_in_db) == result["inserted"]

# Funcion auxiliar para limpiar la colección de prueba manualmente.
def clear_test_collection():
    db["test_collection"].delete_many({})
