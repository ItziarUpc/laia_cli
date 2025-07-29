import subprocess
import shutil
from laia.generators.backoffice.angular.app_component_html import modify_app_component_html
from laia.generators.backoffice.angular.app_component_module import modify_app_component_module
from laia.generators.backoffice.angular.app_component_scss import modify_app_component_scss
from laia.generators.backoffice.angular.app_component_ts import modify_app_component_ts
from laia.generators.backoffice.angular.auth_guard import add_auth_guard
from laia.generators.backoffice.angular.auth_service import add_auth_service
from laia.generators.backoffice.angular.comm_service import add_comm_service
from laia.generators.backoffice.angular.global_page_style import modify_global_page_style
from laia.generators.backoffice.angular.home_component_html import modify_home_component_html
from laia.generators.backoffice.angular.home_component_scss import modify_home_component_scss
from laia.generators.backoffice.angular.home_component_ts import modify_home_component_ts
from laia.generators.backoffice.angular.intercept_service import add_intercept_service
from laia.generators.backoffice.angular.route_to_app_routing import add_route_to_app_routing
from laia.generators.files_generator import create_directory

def generate_angular_project(project_name: str):
    # Verificar si Angular CLI está instalado
    if shutil.which("ng") is None:
        print("🔧 Angular CLI (ng) is not installed. Installing it globally with npm...")
        try:
            subprocess.run(["npm", "install", "-g", "@angular/cli@19"], check=True)
        except subprocess.CalledProcessError:
            print("❌ Failed to install Angular CLI. Please install it manually with:")
            print("   npm install -g @angular/cli")
            return

    print("🚀 Creating Angular backoffice project...")

    subprocess.run([
        "ng", "new", "backoffice", "--routing", "--style=scss",
        "--no-standalone", "--strict", "--skip-tests", "--defaults"
    ], check=True)

    subprocess.run(
        ["npx", "-p", "@angular/cli", "ng", "add", "@angular/material", "--skip-confirmation"],
        cwd="backoffice",
        check=True,
        input=b'azure-blue\nn\n',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Crear carpetas
    create_directory("backoffice/src/app/pages")
    create_directory("backoffice/src/app/components")
    create_directory("backoffice/src/app/services")

    modify_global_page_style()
    modify_app_component_module()
    modify_app_component_ts()
    modify_app_component_html()
    modify_app_component_scss()

    subprocess.run(
      ["ng", "generate", "component", "pages/home"],
      cwd="backoffice",
      check=True
    )

    subprocess.run(
      ["ng", "generate", "component", "pages/login"],
      cwd="backoffice",
      check=True
    )

    subprocess.run(
      ["ng", "generate", "component", "pages/auth"],
      cwd="backoffice",
      check=True
    )

    subprocess.run(
      ["ng", "generate", "component", "pages/models"],
      cwd="backoffice",
      check=True
    )

    subprocess.run(
      ["ng", "generate", "component", "pages/storage"],
      cwd="backoffice",
      check=True
    )

    subprocess.run(
      ["ng", "generate", "component", "pages/settings"],
      cwd="backoffice",
      check=True
    )
    

    add_route_to_app_routing()

    modify_home_component_ts(project_name)
    modify_home_component_scss()
    modify_home_component_html()

    add_comm_service()
    add_intercept_service()
    add_auth_service()
    add_auth_guard()


    print("✅ Angular backoffice created successfully.")