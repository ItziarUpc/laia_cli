import subprocess

from laia_cli.generators.backoffice.angular.angular_generator import generate_angular_project


def create_backoffice_project(tech: str, project_name: str):
    print(f"\nCreating {tech.capitalize()} backoffice project...")

    if tech == "React":
      subprocess.run(["npx", "create-react-app", "backoffice"])
    elif tech == "Angular":
      generate_angular_project(project_name)
    elif tech == "Vue":
      subprocess.run(["npm", "init", "vue@latest", "backoffice"])
    else:
      print("❌ Unknown backoffice technology.")