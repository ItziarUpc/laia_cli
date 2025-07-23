import json
import os

from laia.generators.files_generator import copy_template, create_directory, create_file

def init_project():
    print("\n🛠️ Initializing project...")

    print("\n📛 What is the name of your project?")
    project_name = input("Project name: ").strip() or "routeinjector"

    create_directory("app")
    create_directory("app/backend")
    create_directory("app/openapi")
    create_directory("app/openapi/paths")
    create_directory("app/openapi/schemas")

    TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")

    copy_template(os.path.join(TEMPLATES_DIR, "main.py"), "app/main.py")
    copy_template(os.path.join(TEMPLATES_DIR, "base.yaml"), "app/openapi/base.yaml")
    copy_template(os.path.join(TEMPLATES_DIR, "User.yaml"), "app/openapi/schemas/User.yaml")
    copy_template(os.path.join(TEMPLATES_DIR, "routes.py"), "app/backend/routes.py")
    copy_template(os.path.join(TEMPLATES_DIR, "models.py"), "app/backend/models.py")
    copy_template(os.path.join(TEMPLATES_DIR, "requirements.txt"), "requirements.txt")
    copy_template(os.path.join(TEMPLATES_DIR, ".env"), ".env")
    copy_template(os.path.join(TEMPLATES_DIR, "docker-compose.yaml"), "docker-compose.yaml")

    # Configuración del proyecto
    config = {
        "project_name": project_name,
    }
    create_file("laia.json", json.dumps(config, indent=4))

    print("\n✅ Project created successfully.")