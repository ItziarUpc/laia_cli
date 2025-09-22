import os
import yaml
from pathlib import Path

from laia_cli.generators.kebab_case_converter import to_kebab_case


def modify_model_component_files(yaml_path: str, component_base_path: str):
    if not os.path.exists(yaml_path):
        print(f"⚠️  No existe el YAML: {yaml_path}")
        return

    with open(yaml_path, "r") as f:
        schema = yaml.safe_load(f)

    model_name, definition = next(iter(schema.items()))
    default_fields = definition.get("x-frontend-defaultFields", [])

    if not default_fields:
        print(f"⚠️  No se encontraron 'x-frontend-defaultFields' en {yaml_path}")
        return

    kebab_model = to_kebab_case(model_name)
    model_component_path = f"backoffice/src/app/pages/{component_base_path}/{kebab_model}.component"
    ts_path = f"{model_component_path}.ts"
    html_path = f"{model_component_path}.html"
    scss_path = f"{model_component_path}.scss"

    os.makedirs(os.path.dirname(ts_path), exist_ok=True)

    # === TS FILE ===
    headers_line = f"  headers: string[] = {default_fields};"
    map_fields = ",\n        ".join([f"{field}: item.{field}" for field in default_fields])
    map_block = f"""this.items = response['items'].map((item: any) => ({{
        {map_fields}
      }}));"""

    ts_content = f"""import {{ Component, OnInit }} from '@angular/core';
import {{ PageEvent }} from '@angular/material/paginator';
import {{ {model_name}Service }} from '../../../services/{kebab_model}.service';
import {{ {model_name} }} from '../../../interfaces/{kebab_model}';

@Component({{
  selector: 'app-{kebab_model}',
  standalone: false,
  templateUrl: './{kebab_model}.component.html',
  styleUrl: './{kebab_model}.component.scss'
}})
export class {model_name}Component implements OnInit {{

  searchQuery = '';
  items: {model_name}[] = [];
{headers_line}

  total = 0;
  pageSize = 10;
  currentPage = 0;

  constructor(private service: {model_name}Service) {{}}

  ngOnInit() {{
    this.fetchData(this.currentPage, this.pageSize);
  }}

  fetchData(skip: number, limit: number) {{
    this.service.getAll(skip, limit).subscribe(response => {{
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
        f.write(ts_content)

    # === HTML FILE ===
    html_content = f"""<div class="page">
  <h1>{model_name}</h1>
  <mat-card class="example-card" appearance="outlined">
    <mat-card-header>
      <mat-card-title-group>
        <mat-icon routerLink="/{component_base_path}/new-{kebab_model}">add</mat-icon>
        <mat-card-title>{model_name}s</mat-card-title>
      </mat-card-title-group>
    </mat-card-header>
    <mat-card-content>
      <mat-form-field appearance="outline" class="full-width">
        <mat-label>Search...</mat-label>
        <input matInput type="text" [(ngModel)]="searchQuery">
        <mat-icon matSuffix>search</mat-icon>
      </mat-form-field>
      <app-table [headers]="headers" [data]="items"></app-table>
    </mat-card-content>
    <mat-paginator
      [length]="total"
      [pageSize]="pageSize"
      [pageSizeOptions]="[10, 25, 50]"
      (page)="onPageChange($event)">
    </mat-paginator>
  </mat-card>
</div>
"""
    with open(html_path, "w") as f:
        f.write(html_content)

    # === SCSS FILE ===
    scss_content = """.full-width {
  width: 100%;
}

mat-card-header {
  margin-bottom: 20px;
}

mat-paginator {
  margin: 20px;
}

mat-icon {
  &:hover {
    cursor: pointer;
    background-color: #ebebeb;
    border-radius: 10px;
  }
}
"""
    with open(scss_path, "w") as f:
        f.write(scss_content)

    print(f"✅ Componente {model_name} modificado correctamente")