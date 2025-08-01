import os

def modify_models_component_ts():
    routing_path = "backoffice/src/app/pages/models/models.component.ts"
    schemas_dir = "backend/openapi/schemas"

    if not os.path.exists(routing_path) or not os.path.isdir(schemas_dir):
        return

    # Obtener todos los nombres de archivo sin extensión .yaml o .yml
    model_files = [
        os.path.splitext(f)[0]
        for f in os.listdir(schemas_dir)
        if (f.endswith(".yaml") or f.endswith(".yml")) and os.path.splitext(f)[0] != "User"
    ]

    # Crear contenido del array como string
    models_array_str = ", ".join([f"'{name}'" for name in model_files])

    # Código TypeScript con los modelos ya cargados
    content = f"""import {{ Component }} from '@angular/core';

@Component({{
  selector: 'app-models',
  standalone: false,
  templateUrl: './models.component.html',
  styleUrl: './models.component.scss',
}})
export class ModelsComponent {{

  models: string[] = [{models_array_str}];

  constructor() {{}}

  ngOnInit(): void {{}}
}}
"""

    with open(routing_path, "w") as f:
        f.write(content)

    print(f"✅ ModelsComponent actualizado con: {model_files}")
