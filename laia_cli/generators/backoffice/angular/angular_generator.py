import importlib
from pathlib import Path
import subprocess
import shutil
import sys
import inspect
from pydantic import BaseModel
from laia_cli.generators.backoffice.angular.app_component.app_component_html import modify_app_component_html
from laia_cli.generators.backoffice.angular.app_component.app_component_module import modify_app_component_module
from laia_cli.generators.backoffice.angular.app_component.app_component_scss import modify_app_component_scss
from laia_cli.generators.backoffice.angular.app_component.app_component_ts import modify_app_component_ts
from laia_cli.generators.backoffice.angular.auth.auth_component_html import modify_auth_component_html
from laia_cli.generators.backoffice.angular.auth.auth_component_scss import modify_auth_component_scss
from laia_cli.generators.backoffice.angular.auth.auth_component_ts import modify_auth_component_ts
from laia_cli.generators.backoffice.angular.auth.new_user_html import modify_new_user_component_html
from laia_cli.generators.backoffice.angular.auth.new_user_scss import modify_new_user_component_scss
from laia_cli.generators.backoffice.angular.auth.new_user_ts import modify_new_user_component_ts
from laia_cli.generators.backoffice.angular.kebab_pipe_creator import create_kebab_pipe
from laia_cli.generators.backoffice.angular.services.auth_guard import add_auth_guard
from laia_cli.generators.backoffice.angular.services.auth_service import add_auth_service
from laia_cli.generators.backoffice.angular.services.comm_service import add_comm_service
from laia_cli.generators.backoffice.angular.app_component.global_page_style import modify_global_page_style
from laia_cli.generators.backoffice.angular.home.home_component_html import modify_home_component_html
from laia_cli.generators.backoffice.angular.home.home_component_scss import modify_home_component_scss
from laia_cli.generators.backoffice.angular.home.home_component_ts import modify_home_component_ts
from laia_cli.generators.backoffice.angular.services.intercept_service import add_intercept_service
from laia_cli.generators.backoffice.angular.login.login_component_html import modify_login_component_html
from laia_cli.generators.backoffice.angular.login.login_component_scss import modify_login_component_scss
from laia_cli.generators.backoffice.angular.login.login_component_ts import modify_login_component_ts
from laia_cli.generators.backoffice.angular.models.models_component_html import modify_models_component_html
from laia_cli.generators.backoffice.angular.models.models_component_scss import modify_models_component_scss
from laia_cli.generators.backoffice.angular.models.models_component_ts import modify_models_component_ts
from laia_cli.generators.backoffice.angular.route_to_app_routing import add_new_route, add_route_to_app_routing
from laia_cli.generators.backoffice.angular.table.table_component_html import modify_table_component_html
from laia_cli.generators.backoffice.angular.table.table_component_scss import modify_table_component_scss
from laia_cli.generators.backoffice.angular.table.table_component_ts import modify_table_component_ts
from laia_cli.generators.files_generator import create_directory
from laia_cli.generators.generate_service_ts import generate_ts_service
from laia_cli.generators.generate_ts_interface import generate_all_interfaces_from_schemas

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
  create_directory("backoffice/src/app/pipes")

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
    ["ng", "generate", "component", "pages/schemas"],
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
  
  create_kebab_pipe()

  add_route_to_app_routing()

  modify_home_component_ts(project_name)
  modify_home_component_scss()
  modify_home_component_html()

  add_comm_service()
  add_intercept_service()
  add_auth_service()
  add_auth_guard()

  subprocess.run(
    ["ng", "generate", "component", "/components/table"],
    cwd="backoffice",
    check=True
  )

  modify_table_component_ts()
  modify_table_component_html()
  modify_table_component_scss()

  modify_login_component_html()
  modify_login_component_scss()
  modify_login_component_ts(project_name)

  generate_all_interfaces_from_schemas("backend/openapi/schemas", "backoffice/src/app/interfaces")

  generate_ts_service("User")

  modify_auth_component_ts("backend/openapi/schemas/User.yaml")
  modify_auth_component_html()
  modify_auth_component_scss()

  subprocess.run(
    ["ng", "generate", "component", "/pages/auth/new-user"],
    cwd="backoffice",
    check=True
  )

  modify_new_user_component_html("backend/openapi/schemas/User.yaml")
  modify_new_user_component_ts()
  modify_new_user_component_scss()

  add_new_route(
    path="auth/new-user",
    component="NewUserComponent",
    import_path="./pages/auth/new-user/new-user.component",
    guard=True
  )

  modify_models_component_html()
  modify_models_component_scss()
  modify_models_component_ts()

  print("✅ Angular backoffice created successfully.")