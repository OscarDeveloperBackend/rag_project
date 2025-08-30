import pytest
from app.controllers import qa_controller

def test_get_most_similar_chunk():
    # Pregunta de ejemplo
    question = "Lisa Müller"  

    # Llamar la función
    result = qa_controller.get_most_similar_chunk(question, min_similarity=0.4)

    # Mostrar en terminal lo que devuelve
    print("Resultado de get_most_similar_chunk:", result)

    # Comprobar que la estructura es correcta
    assert "similarity" in result or "message" in result

    if "similarity" in result:
        assert isinstance(result["similarity"], float)
        assert "chunk" in result
        assert isinstance(result["chunk"], str)
    else:
        # Aceptar cualquiera de los mensajes posibles
        assert result["message"] in [
            "No hay datos en la base",
            "No se encontró un chunk suficientemente cercano"
        ]
