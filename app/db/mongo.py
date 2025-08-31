from pymongo import MongoClient # - importamos el cliente de MongoDB
from app.config import settings # - importamos las variables del .env cargadas en settings

# Creamos el cliente de Mongo usando la URL definida en el .env
client = MongoClient(settings.MONGO_URL)

# Seleccionamos la base de datos por nombre (DB_NAME del .env)
db = client[settings.DB_NAME]

#test de conexon
def test_connection():
    try:
        client.admin.command("ping")
        print("Conectado a MongoDB:", db.name)

        collections = db.list_collection_names()
        print("Colecciones en la DB:", collections)
    except Exception as e:
        print("Error de conexion:", e)

# Si ejecutamos este archivo directamente, probamos la conexion
if __name__ == "__main__":
    test_connection()
