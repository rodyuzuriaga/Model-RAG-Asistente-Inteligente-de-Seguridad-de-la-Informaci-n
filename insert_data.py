import json
import pymongo
from pymongo import MongoClient

# Conectar a MongoDB
client = MongoClient("mongodb+srv://rodyuzuriaga:jG8KeOea6LoeLbgi@cluster0.kz9c1wg.mongodb.net/")
db = client["security_db"]
collection_risk_records = db["risk_records"]
collection_technova_personnel = db["technova_personnel"]

# Cargar datos del JSON
with open('techNova_risk_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Limpiar colecciones existentes
collection_risk_records.delete_many({"company": "TechNova S.A."})
collection_technova_personnel.delete_many({"company": "TechNova S.A."})

# Insertar datos de riesgo
risk_records = data["data"]
inserted_risks = collection_risk_records.insert_many(risk_records)

# Insertar responsables
personnel_records = data["responsables"]
inserted_personnel = collection_technova_personnel.insert_many(personnel_records)

print("✅ Datos insertados exitosamente en MongoDB")
print(f"📊 {len(inserted_risks.inserted_ids)} registros de riesgo insertados")
print(f"👥 {len(inserted_personnel.inserted_ids)} responsables TechNova insertados")

# Verificar inserción
total_risks = collection_risk_records.count_documents({"company": "TechNova S.A."})
total_personnel = collection_technova_personnel.count_documents({"company": "TechNova S.A."})

print(f"🔍 Verificación: {total_risks} riesgos y {total_personnel} responsables en BD")