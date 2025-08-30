from pymongo import MongoClient
from app.config import settings

client = MongoClient(settings.MONGO_URL)
db = client[settings.DB_NAME]

def test_connection():
    try:
        client.admin.command("ping")
        print("✅ Conectado a MongoDB:", db.name)

        collections = db.list_collection_names()
        print("📂 Colecciones en la DB:", collections)
    except Exception as e:
        print("❌ Error de conexión:", e)

if __name__ == "__main__":
    test_connection()
