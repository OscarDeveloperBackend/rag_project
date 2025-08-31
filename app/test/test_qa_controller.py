import pytest
from app.controllers import qa_controller  # Importamos el controlador a testear

def test_get_most_similar_chunk():
    # Definimos una pregunta de ejemplo para probar la función
    question = "Lisa Müller"  

    # Llamamos a la funcion get_most_similar_chunk con la pregunta
    result = qa_controller.get_most_similar_chunk(question, min_similarity=0.4)

    # Mostrar en terminal lo que devuelve
    print("Resultado de get_most_similar_chunk:", result)

    # Verificar que el resultado tenga la estructura esperada
    # Puede ser 'similarity' y 'chunk' si encontró un chunk relevante
    # o 'message' si no se encontró ningún chunk
    assert "similarity" in result or "message" in result

    if "similarity" in result:
        # Si hay similitud, comprobamos que es un float
        assert isinstance(result["similarity"], float)
        assert "chunk" in result
        assert isinstance(result["chunk"], str)
    else:
        # Si no hay chunk, aceptamos cualquiera de los mensajes posibles
        assert result["message"] in [
            "No hay datos en la base",
            "No se encontró un chunk suficientemente cercano"
        ]
