import subprocess
import os

def run_command(command, cwd=None):
    try:
        print(f"\n💻 Running: {command}")
        subprocess.run(command, shell=True, check=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error while running: {command}")
        print(f"📄 {e}")
        exit(1)

def start_project():
    print("\n🟢 Starting LAIA project...")

    # Step 1: Install requirements
    if os.path.exists("requirements.txt"):
        print("\n🐍 Installing Python dependencies...")
        run_command("pip install -r requirements.txt")
    else:
        print("⚠️  requirements.txt not found, skipping pip install.")

    # Step 2: Docker Compose up
    if os.path.exists("docker-compose.yaml"):
        print("\n🐳 Starting Docker containers...")
        run_command("docker compose up -d")
    else:
        print("⚠️  docker-compose.yaml not found, skipping Docker step.")

    # Step 3: Run main.py
    main_file = "app/main.py"
    if os.path.exists(main_file):
        print("\n🚀 Launching application...")
        run_command(f"python {main_file}")
    else:
        print("⚠️  app/main.py not found, cannot start the application.")