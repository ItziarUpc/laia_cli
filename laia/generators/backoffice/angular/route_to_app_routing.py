import os
import re


def add_route_to_app_routing():
    routing_path = "backoffice/src/app/app-routing.module.ts"
    if not os.path.exists(routing_path):
        return  # No routing module

    content = """import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { AuthComponent } from './pages/auth/auth.component';
import { ModelsComponent } from './pages/models/models.component';
import { StorageComponent } from './pages/storage/storage.component';
import { SettingsComponent } from './pages/settings/settings.component';
import { AuthGuard } from './services/auth.guard';
import { LoginComponent } from './pages/login/login.component';
import { SchemasComponent } from './pages/schemas/schemas.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'login', component: LoginComponent },
  { path: 'auth', component: AuthComponent, canActivate: [AuthGuard] },
  { path: 'schemas', component: SchemasComponent, canActivate: [AuthGuard] },
  { path: 'models', component: ModelsComponent, canActivate: [AuthGuard] },
  { path: 'storage', component: StorageComponent, canActivate: [AuthGuard] },
  { path: 'settings', component: SettingsComponent, canActivate: [AuthGuard] },
  { path: '**', redirectTo: 'login', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
"""
    with open(routing_path, "w") as f:
        f.write(content)

def add_new_route(path: str, component: str, import_path: str, guard: bool = True):
    routing_path = "backoffice/src/app/app-routing.module.ts"
    if not os.path.exists(routing_path):
        print("⚠️ No se encontró app-routing.module.ts")
        return

    with open(routing_path, "r") as f:
        content = f.read()

    # 1. Agregar import si no existe
    import_statement = f"import {{ {component} }} from '{import_path}';"
    if import_statement not in content:
        # Insertar el import antes de 'const routes'
        content = content.replace("const routes:", f"{import_statement}\n\nconst routes:")

    # 2. Verificar si la ruta ya existe
    route_line = f"path: '{path}'"
    if route_line in content:
        print(f"ℹ️ Ruta '/{path}' ya existe.")
        return

    # 3. Construir la ruta
    route_entry = f" {{ path: '{path}', component: {component}"
    if guard:
        route_entry += ", canActivate: [AuthGuard]"
    route_entry += " },"

    # 4. Insertar la ruta antes de la línea con '**'
    pattern = re.compile(r"(\{ path: '\*\*'.*?})", re.DOTALL)
    match = pattern.search(content)
    if match:
        full_match = match.group(1)
        content = content.replace(full_match, f"{route_entry}\n  {full_match}")

    # 5. Guardar cambios
    with open(routing_path, "w") as f:
        f.write(content)

    print(f"✅ Ruta '/{path}' → {component} añadida correctamente.")