import json
import os
import re

from laia_cli.generators.backoffice.backoffice_generator import create_backoffice_project
from laia_cli.generators.files_generator import copy_template, create_directory, create_file

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

MONGO_RS_COMMAND_LINE = '    command: ["--replSet", "rs0", "--bind_ip_all"]\n'
INIT_REPLICA_VOLUME_LINE = '      - ./init-replica.js:/docker-entrypoint-initdb.d/init-replica.js:ro\n'

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

def ensure_mongo_replicaset_in_compose(compose_path: str):
    """
    Dentro del bloque '  mongo:' inserta:
      - command: ["--replSet", "rs0", "--bind_ip_all"]
      - en volumes: el bind del init-replica.js
    Crea 'volumes:' del servicio si no existe.
    """
    if not os.path.exists(compose_path):
        return

    with open(compose_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1) localizar bloque del servicio mongo
    m = re.search(r"(?ms)^  mongo:\n(?: {4}.+\n)+", content)
    if not m:
        # no hay bloque mongo, no tocamos
        return

    block = m.group(0)

    # 2) asegurar command line
    if "    command:" not in block:
        block = block.replace("  mongo:\n", "  mongo:\n" + MONGO_RS_COMMAND_LINE, 1)

    # 3) asegurar el volumen del init-replica.js dentro de volumes del servicio
    if "    volumes:" in block:
        # ya hay volumes: añadir el bind si no existe
        if INIT_REPLICA_VOLUME_LINE.strip() not in block:
            block = re.sub(
                r"(?ms)(^    volumes:\n)",
                r"\1" + INIT_REPLICA_VOLUME_LINE,
                block
            )
    else:
        # crear volumes con la línea del init-replica (no tocamos mongo_data: si estaba fuera)
        insert_after = "    ports:\n"
        if insert_after in block:
            # intenta añadir después del bloque de ports o environment si existen
            block = block.replace(insert_after, insert_after)  # noop, seguimos
        # añadimos un bloque mínimo de volumes en el servicio
        # (si ya hay mongo_data en el servicio, el usuario lo conservará; si está fuera, no pasa nada)
        block = re.sub(r"(?m)^(  mongo:\n)", r"\1    volumes:\n" + INIT_REPLICA_VOLUME_LINE, block)

    # 4) escribir de vuelta el compose con el bloque reemplazado
    new_content = content[:m.start()] + block + content[m.end():]
    with open(compose_path, "w", encoding="utf-8") as f:
        f.write(new_content)

def remove_mongo_replicaset_from_compose(compose_path: str):
    """
    Elimina del servicio mongo:
      - la línea 'command: ["--replSet", "rs0", "--bind_ip_all"]'
      - el bind del init-replica.js dentro de 'volumes:'
    Si 'volumes:' del servicio queda vacío, lo quita.
    """
    if not os.path.exists(compose_path):
        return
    with open(compose_path, "r", encoding="utf-8") as f:
        content = f.read()

    m = re.search(r"(?ms)^  mongo:\n(?: {4}.+\n)+", content)
    if not m:
        return

    block = m.group(0)

    # quitar command line
    block = block.replace(MONGO_RS_COMMAND_LINE, "")

    # quitar línea de volumen del init script
    if INIT_REPLICA_VOLUME_LINE in block:
        block = block.replace(INIT_REPLICA_VOLUME_LINE, "")

        # si 'volumes:' quedó sin ítems, eliminar la sección
        # detecta '    volumes:\n' seguido NO de '      -'
        block = re.sub(r"(?ms)^    volumes:\n(?!( {6}|      )-).*\n?", "", block)

    new_content = content[:m.start()] + block + content[m.end():]
    with open(compose_path, "w", encoding="utf-8") as f:
        f.write(new_content)


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
        copy_template(os.path.join(TEMPLATES_DIR, "init-replica.js"), "init-replica.js")
        ensure_mongo_replicaset_in_compose(os.path.join(TEMPLATES_DIR, "docker-compose.yaml"))
    else:
        remove_fuseki_from_compose(os.path.join(TEMPLATES_DIR, "docker-compose.yaml"))
        remove_mongo_replicaset_from_compose(os.path.join(TEMPLATES_DIR, "docker-compose.yaml"))

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