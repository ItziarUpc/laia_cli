import asyncio
import subprocess
import os

from laia_cli.commands.run_laia_flutter import run_laia_flutter
from laia_cli.generators.backoffice.angular.models.model_component_files import modify_model_component_files
from laia_cli.generators.backoffice.angular.models.models_component_ts import modify_models_component_ts
from laia_cli.generators.backoffice.angular.route_to_app_routing import add_new_route
from laia_cli.generators.generate_service_ts import generate_ts_service
from laia_cli.generators.generate_ts_interface import generate_all_interfaces_from_schemas
from laia_cli.generators.kebab_case_converter import to_kebab_case

def run_command(command, cwd=None):
    try:
        subprocess.run(command, shell=True, check=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error while running: {command}")
        print(f"{e}")
        exit(1)

def start_project(args):
    if args.backend:
        print("🚀 Starting backend...")
        # Step 1: Install requirements
        if os.path.exists("requirements.txt"):
            run_command("pip install -r requirements.txt")
        else:
            print("⚠️  requirements.txt not found, skipping pip install.")

        # Step 2: Docker Compose up
        if os.path.exists("docker-compose.yaml"):
            print("\nStarting Docker containers...")
            run_command("docker compose up -d")
        else:
            print("⚠️  docker-compose.yaml not found, skipping Docker step.")

        # Step 3: Run main.py
        main_file = "backend/main.py"
        if os.path.exists(main_file):
            print("\n🚀 Launching application...")
            run_command(f"python {main_file}")
        else:
            print("⚠️  backendpp/main.py not found, cannot start the application.")

    if args.frontend:
        openapi_path = os.path.join(os.getcwd(), "backend", "openapi.yaml")
        asyncio.run(run_laia_flutter(openapi_path, "backend", "frontend"))

    if args.backoffice:
        print("🚀 Starting backoffice...")
        modify_models_component_ts()
        generate_all_interfaces_from_schemas("backend/openapi/schemas", "backoffice/src/app/interfaces")

        schemas_dir = "backend/openapi/schemas"
        pages_dir = "backoffice/src/app/pages/models"

        for filename in os.listdir(schemas_dir):
            if not (filename.endswith(".yaml") or filename.endswith(".yml")):
                continue

            model_name = os.path.splitext(filename)[0]
            if model_name == "User":
                continue

            kebab_name = to_kebab_case(model_name)
            model_folder = os.path.join(pages_dir, kebab_name)

            if not os.path.exists(model_folder):
                print(f"🆕 Generando componentes para modelo: {model_name} → {kebab_name}")
                try:
                    subprocess.run(
                        ["ng", "generate", "component", f"pages/models/{kebab_name}"],
                        cwd="backoffice",
                        check=True
                    )
                    add_new_route(
                        path=f"models/{kebab_name}",
                        component=f"{model_name}Component",
                        import_path=f"./pages/models/{kebab_name}/{kebab_name}.component",
                        guard=True
                    )
                    generate_ts_service(model_name)
                    schema_path = os.path.join(schemas_dir, filename)
                    modify_model_component_files(
                        yaml_path=schema_path,
                        component_base_path=f"models/{kebab_name}"
                    )
                    subprocess.run(
                        ["ng", "generate", "component", f"pages/models/{kebab_name}/new-{kebab_name}"],
                        cwd="backoffice",
                        check=True
                    )
                    add_new_route(
                        path=f"models/{kebab_name}/new-{kebab_name}",
                        component=f"New{model_name}Component",
                        import_path=f"./pages/models/{kebab_name}/new-{kebab_name}/new-{kebab_name}.component",
                        guard=True
                    )
                except subprocess.CalledProcessError as e:
                    print(f"❌ Error generando componentes para {model_name}: {e}")

        backoffice_path = "backoffice"
        env = os.environ.copy()
        env["NG_CLI_ANALYTICS"] = "ci"  # <- Previene el error 'setRawMode EIO'

        if os.path.exists(os.path.join(backoffice_path, "angular.json")):
            subprocess.run(["ng", "serve", "--open"], cwd=backoffice_path, env=env)
        elif os.path.exists(os.path.join(backoffice_path, "package.json")):
            subprocess.run(["npm", "start"], cwd=backoffice_path, env=env)
        else:
            print("⚠️ No backoffice project found to start.")

    if not (args.backend or args.frontend or args.backoffice):
        print("⚠️  No target specified. Use --backend, --frontend, or --backoffice.")