import json
import os

from laia.generators.backoffice.backoffice_generator import create_backoffice_project
from laia.generators.files_generator import copy_template, create_directory, create_file

def init_project():
    print("\nInitializing project...")

    print("\nWhat is the name of your project?")
    project_name = input("Project name: ").strip() or "routeinjector"

    print("\nDo you want to use ontology in your project? [y/N]")
    use_ontology = input("Use ontology: ").strip().lower() == "y"

    print("\nDo you want to use access rights in your project? [y/N]")
    use_access_rights = input("Use access rights: ").strip().lower() == "y"

    # Database
    print("\nWhich database do you want to use?")
    print("Options: [1] MongoDB, [2] PostgreSQL")
    db_option = input("Select database (1 or 2): ").strip()
    database = "MongoDB" if db_option == "1" else "PostgreSQL"

    # Frontend framework
    print("\nWhich frontend framework do you want to use?")
    print("Options: [1] Flutter, [2] Ionic Angular")
    frontend_option = input("Select frontend (1 or 2): ").strip()
    frontend = {
        "1": "Flutter",
        "2": "Ionic Angular"
    }.get(frontend_option, "Flutter")  # Default to Flutter

    # Backoffice framework
    print("\nWhich backoffice framework do you want to use?")
    print("Options: [1] Angular, [2] React, [3] Vue")
    backoffice_option = input("Select backoffice (1, 2 or 3): ").strip()
    backoffice = {
        "1": "Angular",
        "2": "React",
        "3": "Vue"
    }.get(backoffice_option, "Angular")  # Default to Angular

    create_directory("backend")
    create_directory("frontend")
    create_directory("backoffice")
    create_directory("backend/backend")
    create_directory("backend/openapi")
    create_directory("backend/openapi/paths")
    create_directory("backend/openapi/schemas")

    TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")

    copy_template(os.path.join(TEMPLATES_DIR, "main.py"), "backend/main.py")
    copy_template(os.path.join(TEMPLATES_DIR, "base.yaml"), "backend/openapi/base.yaml")
    copy_template(os.path.join(TEMPLATES_DIR, "User.yaml"), "backend/openapi/schemas/User.yaml")
    copy_template(os.path.join(TEMPLATES_DIR, "routes.py"), "backend/backend/routes.py")
    copy_template(os.path.join(TEMPLATES_DIR, "models.py"), "backend/backend/models.py")
    copy_template(os.path.join(TEMPLATES_DIR, "requirements.txt"), "requirements.txt")
    copy_template(os.path.join(TEMPLATES_DIR, ".env"), ".env")
    copy_template(os.path.join(TEMPLATES_DIR, "docker-compose.yaml"), "docker-compose.yaml")

    # Configuración del proyecto
    config = {
        "project_name": project_name,
        "use_ontology": use_ontology,
        "database": database,
        "frontend": frontend,
        "backoffice": backoffice,
        "use_access_rights": use_access_rights
    }
    create_file("laia.json", json.dumps(config, indent=4))

    create_backoffice_project(backoffice, project_name)

    print("\nProject created successfully.")