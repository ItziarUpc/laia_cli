from laiagenlib.Infrastructure.Openapi.LaiaFastApi import LaiaFastApi
from laiagenlib.Infrastructure.LaiaBaseModel.MongoModelRepository import MongoModelRepository
from laiagenlib.Infrastructure.Openapi.FastAPIOpenapiRepository import FastAPIOpenapiRepository
from pymongo import MongoClient
from laiagenlib.Domain.LaiaBaseModel.LaiaBaseModel import LaiaBaseModel
import os
import uvicorn
import asyncio
import time
import requests
import yaml
import json
import threading
from dotenv import load_dotenv

print("🔁 Cargando entorno...", flush=True)
load_dotenv()

print("🔧 Cargando configuración desde variables de entorno...", flush=True)
mongo_client_url = os.getenv("MONGO_CLIENT_URL", "mongodb://localhost:27017")
mongo_database_name = os.getenv("MONGO_DATABASE_NAME", "test")
openapi_file_name = "openapi.yaml"
backend_folder_name = "backend"
backend_jwt_secret_key = os.getenv("BACKEND_JWT_SECRET_KEY", "mysecret")
backend_port = int(os.getenv("BACKEND_PORT", 8005))

print(f"✅ Conectando a MongoDB en {mongo_client_url}...", flush=True)
client = MongoClient(mongo_client_url)
db = client[mongo_database_name]
print("✅ Conectado a la base de datos.", flush=True)

print("📦 Cargando OpenAPI desde partes...", flush=True)
base_path = os.path.join("app", "openapi")
base_file = os.path.join(base_path, "base.yaml")
schemas_dir = os.path.join(base_path, "schemas")
paths_dir = os.path.join(base_path, "paths")
output_file = os.path.join("app", "openapi.yaml")

with open(base_file, "r") as f:
    openapi_doc = yaml.safe_load(f)

openapi_doc.setdefault("components", {})
openapi_doc["components"].setdefault("schemas", {})
openapi_doc.setdefault("paths", {})

print("📄 Procesando schemas...", flush=True)
for filename in os.listdir(schemas_dir):
    if filename.endswith((".yaml", ".yml")):
        filepath = os.path.join(schemas_dir, filename)
        print(f"🔹 Leyendo schema: {filepath}", flush=True)
        with open(filepath, "r") as f:
            schema = yaml.safe_load(f)
            if isinstance(schema, dict):
                openapi_doc["components"]["schemas"].update(schema)

print("📄 Procesando paths...", flush=True)
for filename in os.listdir(paths_dir):
    if filename.endswith((".yaml", ".yml")):
        filepath = os.path.join(paths_dir, filename)
        print(f"🔸 Leyendo path: {filepath}", flush=True)
        with open(filepath, "r") as f:
            path_def = yaml.safe_load(f)
            if isinstance(path_def, dict):
                openapi_doc["paths"].update(path_def)

print(f"💾 Guardando OpenAPI en {output_file}...", flush=True)
with open(output_file, "w") as f:
    yaml.dump(openapi_doc, f, sort_keys=False)

print(f"✅ OpenAPI generated with {len(openapi_doc['components']['schemas'])} schemas and {len(openapi_doc['paths'])} routes.", flush=True)

openapi_path = os.path.join(os.getcwd(), "app", openapi_file_name)

async def main():
    print("🚀 Iniciando instancia LaiaFastApi...", flush=True)
    app_instance = await LaiaFastApi(
        openapi_path,
        backend_folder_name,
        db,
        MongoModelRepository,
        FastAPIOpenapiRepository,
        backend_jwt_secret_key
    )
    print("✅ LaiaFastApi inicializada.", flush=True)

    app = app_instance.api

    print("➕ Añadiendo rutas extra...", flush=True)
    from backend.routes import ExtraRoutes
    app.include_router(ExtraRoutes(app_instance.repository_instance))
    print("✅ Rutas extra incluidas.", flush=True)

    print(f"🌍 Lanzando servidor en puerto {backend_port}...", flush=True)
    config = uvicorn.Config(app, host="0.0.0.0", port=backend_port)
    server = uvicorn.Server(config)
    await server.serve()

def run_server():
    print("🧵 Iniciando hilo del servidor...", flush=True)
    asyncio.run(main())

MAX_RETRIES = 30
RETRY_INTERVAL = 1

if __name__ == "__main__":
    print("🧠 Entrando en bloque principal (__main__)...", flush=True)

    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    print("🟢 Hilo del servidor lanzado.", flush=True)

    time.sleep(10)

    import importlib.util
    import sys

    models_path = os.path.join("app", "backend", "models.py")
    if os.path.exists(models_path):
        spec = importlib.util.spec_from_file_location("models", models_path)
        models = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(models)
        sys.modules["models"] = models

        # Aquí forzamos rebuild de todos los modelos del módulo generado
        for attr in dir(models):
            model_class = getattr(models, attr)
            if hasattr(model_class, "model_rebuild"):
                try:
                    model_class.model_rebuild()
                except Exception:
                    pass  # puede que algunos no lo necesiten


        time.sleep(10)
    else:
        print(f"❌ models.py not found at {models_path}")

    try:
        response = requests.get(f"http://localhost:{backend_port}/openapi.json")
        if response.status_code == 200:
            openapi_yaml = yaml.dump(json.loads(response.text), default_flow_style=False)
            with open(openapi_path, "wb") as f: 
                f.write(openapi_yaml.encode("utf-8"))
            print("✅ OpenAPI YAML file saved.")
        else:
            print(f"❌ Failed to retrieve OpenAPI YAML file: {response.status_code}")
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")

    print("💤 Servidor lanzado, esperando interrupción...", flush=True)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Apagando servidor...", flush=True)
        os._exit(0)