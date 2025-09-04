import json
import os

from laia.generators.backoffice.backoffice_generator import create_backoffice_project
from laia.generators.files_generator import copy_template, create_directory, create_file

FUSEKI_BLOCK = """\
  jena-fuseki:
    image: stain/jena-fuseki
    container_name: jena-fuseki
    platform: linux/amd64
    ports:
      - "3030:3030"
    environment:
      - ADMIN_PASSWORD=admin
    volumes:
      - jena_data:/fuseki
"""

def ensure_fuseki_in_compose(compose_path: str):
    """Añade el servicio jena-fuseki correctamente en services y el volumen jena_data en el bloque global."""
    if not os.path.exists(compose_path):
        return

    with open(compose_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Ya está → nada que hacer
    if any("jena-fuseki:" in line for line in lines):
        return

    new_lines = []
    inserted_service = False
    found_global_volumes = False
    inserted_volume = False

    for i, line in enumerate(lines):
        # Detectamos el bloque global de volumes (sin indentación)
        if line.strip().startswith("volumes:") and not line.startswith(" "):
            # Insertamos el servicio justo antes del bloque global
            if not inserted_service:
                new_lines.append(FUSEKI_BLOCK)
                inserted_service = True
            found_global_volumes = True

        new_lines.append(line)

    # Si no hemos insertado el servicio (porque no había bloque global de volumes todavía)
    if not inserted_service:
        new_lines.append(FUSEKI_BLOCK)

    # Añadimos el volumen global jena_data
    if found_global_volumes:
        if not any(line.strip().startswith("jena_data:") for line in new_lines):
            new_lines.append("  jena_data:\n")
    else:
        new_lines.append("\nvolumes:\n  jena_data:\n")

    with open(compose_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)


def remove_fuseki_from_compose(compose_path: str):
    """Elimina el servicio jena-fuseki y el volumen global jena_data del docker-compose."""
    if not os.path.exists(compose_path):
        return

    with open(compose_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    skip = False

    for line in lines:
        # Detectar inicio del servicio jena-fuseki
        if line.startswith("  jena-fuseki:"):
            skip = True
            continue

        # Si estamos dentro del bloque jena-fuseki, seguimos saltando
        if skip:
            # El bloque termina si encontramos otra definición de servicio (2 espacios) o bloque global
            if (line.startswith("  ") and not line.startswith("    ")) or not line.startswith(" "):
                skip = False
                new_lines.append(line)
            # Si no, seguimos saltando (líneas internas de jena-fuseki)
            continue

        # Saltar la definición del volumen global jena_data
        if line.strip().startswith("jena_data:"):
            continue

        new_lines.append(line)

    with open(compose_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)



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

    if use_ontology:
        ensure_fuseki_in_compose(os.path.join(TEMPLATES_DIR, "docker-compose.yaml"))
    else:
        remove_fuseki_from_compose(os.path.join(TEMPLATES_DIR, "docker-compose.yaml"))

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

    #create_backoffice_project(backoffice, project_name)

    print("\nProject created successfully.")