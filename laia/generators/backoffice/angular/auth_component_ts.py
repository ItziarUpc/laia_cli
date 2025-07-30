import os
import yaml

def modify_auth_component_ts(yaml_path: str):
    ts_path = "backoffice/src/app/pages/auth/auth.component.ts"
    if not os.path.exists(ts_path):
        print(f"⚠️  No existe {ts_path}")
        return

    with open(yaml_path, "r") as f:
        schema = yaml.safe_load(f)

    # Asumimos que el nombre del modelo es la clave raíz
    model_name, definition = next(iter(schema.items()))
    default_fields = definition.get("x-frontend-defaultFields", [])

    if not default_fields:
        print(f"⚠️  No se encontraron 'x-frontend-defaultFields' en {yaml_path}")
        return

    # Generar línea headers
    headers_line = f"  headers: string[] = {default_fields};"

    # Generar mapping dinámico para user
    map_fields = ",\n        ".join([f"{field}: user.{field}" for field in default_fields])
    map_block = f"""this.users = response['items'].map((user: {{ name: any; surnames: any; email: any; }}) => ({{
        {map_fields}
      }}));"""

    # Crear contenido del componente con sustituciones
    content = f"""import {{ Component, OnInit }} from '@angular/core';
import {{ UserService }} from '../../services/user.service';
import {{ User }} from '../../interfaces/user';
import {{ PageEvent }} from '@angular/material/paginator';

@Component({{
  selector: 'app-auth',
  standalone: false,
  templateUrl: './auth.component.html',
  styleUrl: './auth.component.scss'
}})
export class AuthComponent implements OnInit {{
  
  searchQuery = '';
  users: User[] = [];
{headers_line}

  total = 0;
  pageSize = 10;
  currentPage = 0;

  constructor( 
    private userService: UserService
  ) {{}}

  ngOnInit() {{
    this.fetchData(this.currentPage, this.pageSize);
  }}

  fetchData(skip: number, limit: number) {{
    this.userService.getAll(0, 10).subscribe(response => {{
      {map_block}
      this.total = response['max_pages'];
    }});
  }}

  onPageChange(event: PageEvent) {{
    this.currentPage = event.pageIndex;
    this.pageSize = event.pageSize;
    const skip = this.currentPage * this.pageSize;
    this.fetchData(skip, this.pageSize);
  }}

}}
"""

    with open(ts_path, "w") as f:
        f.write(content)
    print(f"✅ auth.component.ts actualizado con campos: {default_fields}")
