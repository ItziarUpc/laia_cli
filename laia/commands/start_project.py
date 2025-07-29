import subprocess
import os

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
        print("🚀 Starting frontend...")
        # Lógica para arrancar el frontend

    if args.backoffice:
        print("🚀 Starting backoffice...")
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