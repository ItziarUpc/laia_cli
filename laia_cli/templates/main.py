from laiagenlib.Infrastructure.Openapi.LaiaFastApi import LaiaFastApi
from laiagenlib.Infrastructure.Openapi.LaiaFlutter import LaiaFlutter
from laiagenlib.Infrastructure.LaiaBaseModel.MongoModelRepository import MongoModelRepository
from laiagenlib.Infrastructure.Openapi.FastAPIOpenapiRepository import FastAPIOpenapiRepository
from pymongo import MongoClient
from laiagenlib.Domain.LaiaBaseModel.LaiaBaseModel import LaiaBaseModel
from laia_ontology_sync import start_background_watcher
import os
import uvicorn
import asyncio
import time
import requests
import yaml
import json
import threading
from dotenv import load_dotenv
import shutil

load_dotenv()

mongo_client_url = os.getenv("MONGO_CLIENT_URL", "mongodb://localhost:27017")
mongo_database_name = os.getenv("MONGO_DATABASE_NAME", "test")
openapi_file_name = "openapi.yaml"
backend_folder_name = "backend"
frontend_folder_name = "frontend"
backend_jwt_secret_key = os.getenv("BACKEND_JWT_SECRET_KEY", "mysecret")
backend_jwt_refresh_secret_key = os.getenv("BACKEND_JWT_REFRESH_SECRET_KEY", "mysecretrefresh")
backend_port = int(os.getenv("BACKEND_PORT", 8005))
fuseki_base_url = os.getenv("FUSEKI_BASE_URL", "http://localhost:3030")
fuseki_user= os.getenv("FUSEKI_USER", "admin")
fuseki_pwd= os.getenv("FUSEKI_PWD", "admin")
base_uri_prefix = os.getenv("BASE_URI_PREFIX", "http://localhost:8005")

client = MongoClient(mongo_client_url)
db = client[mongo_database_name]

base_path = os.path.join("backend", "openapi")
base_file = os.path.join(base_path, "base.yaml")
schemas_dir = os.path.join(base_path, "schemas")
paths_dir = os.path.join(base_path, "paths")
output_file = os.path.join("backend", "openapi.yaml")

with open(base_file, "r") as f:
    openapi_doc = yaml.safe_load(f)

openapi_doc.setdefault("components", {})
openapi_doc["components"].setdefault("schemas", {})
openapi_doc.setdefault("paths", {})

for filename in os.listdir(schemas_dir):
    if filename.endswith((".yaml", ".yml")):
        filepath = os.path.join(schemas_dir, filename)
        with open(filepath, "r") as f:
            schema = yaml.safe_load(f)
            if isinstance(schema, dict):
                openapi_doc["components"]["schemas"].update(schema)

for filename in os.listdir(paths_dir):
    if filename.endswith((".yaml", ".yml")):
        filepath = os.path.join(paths_dir, filename)
        with open(filepath, "r") as f:
            path_def = yaml.safe_load(f)
            if isinstance(path_def, dict):
                openapi_doc["paths"].update(path_def)

with open(output_file, "w") as f:
    yaml.dump(openapi_doc, f, sort_keys=False)

openapi_path = os.path.join(os.getcwd(), "backend", openapi_file_name)

laia_config_path = os.path.join(os.getcwd(), "laia.json")
with open(laia_config_path, "r", encoding="utf-8") as f:
    laia_config = json.load(f)

async def main():
    app_instance = await LaiaFastApi(
        openapi_path,
        backend_folder_name,
        db,
        MongoModelRepository,
        FastAPIOpenapiRepository,
        laia_config.get("use_ontology", False),
        laia_config.get("use_access_rights", True),
        backend_jwt_secret_key,
        backend_jwt_refresh_secret_key
    )

    app = app_instance.api

    from backend.routes import ExtraRoutes
    app.include_router(ExtraRoutes(app_instance.repository_instance))

    config = uvicorn.Config(app, host="0.0.0.0", port=backend_port)
    server = uvicorn.Server(config)

    await server.serve()

async def run_laia_flutter_later():
    await asyncio.sleep(5)

    flutter_bin = os.path.expandvars("$HOME/flutter/bin/flutter")

    flutter_path = shutil.which("flutter")

    if flutter_path is None and os.path.exists(flutter_bin):
        flutter_dir = os.path.dirname(flutter_bin)
        os.environ["PATH"] += os.pathsep + flutter_dir
        flutter_path = shutil.which("flutter")

    if flutter_path is None:
        print("❌ Flutter no está instalado ni disponible en $HOME/flutter/bin/flutter")

    await LaiaFlutter(openapi_path, backend_folder_name, frontend_folder_name)

def run_server():
    asyncio.run(main())

MAX_RETRIES = 30
RETRY_INTERVAL = 1

if __name__ == "__main__":

    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    ontology_enabled = laia_config.get("use_ontology", False)

    if ontology_enabled:
        start_background_watcher(
            mongo_url=f"{mongo_client_url}/?replicaSet=rs0",
            db_name=mongo_database_name,
            models={}, 
            fuseki_base=fuseki_base_url,
            user=fuseki_user,
            pwd=fuseki_pwd,
            base_uri_prefix=base_uri_prefix,
            watch_whole_db=True,
        )

    print("Loading...")
    time.sleep(10)

    import importlib.util
    import sys

    models_path = os.path.join("backend", "backend", "models.py")
    if os.path.exists(models_path):
        spec = importlib.util.spec_from_file_location("models", models_path)
        models = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(models)
        sys.modules["models"] = models

        for attr in dir(models):
            model_class = getattr(models, attr)
            if hasattr(model_class, "model_rebuild"):
                try:
                    model_class.model_rebuild()
                except Exception:
                    pass  


        time.sleep(10)
    else:
        print(f"❌ models.py not found at {models_path}")

    try:
        response = requests.get(f"http://localhost:{backend_port}/openapi.json")
        if response.status_code == 200:
            openapi_yaml = yaml.dump(json.loads(response.text), default_flow_style=False)
            with open(openapi_path, "wb") as f: 
                f.write(openapi_yaml.encode("utf-8"))
            print("OpenAPI YAML file saved.")
        else:
            print(f"❌ Failed to retrieve OpenAPI YAML file: {response.status_code}")
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")

    print("Server launched, waiting for interruption...", flush=True)
    #asyncio.create_task(run_laia_flutter_later())
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping server...", flush=True)
        os._exit(0)