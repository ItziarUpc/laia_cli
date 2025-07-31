import yaml
import os

def modify_new_user_component_html(yaml_path: str):
    html_path = "backoffice/src/app/pages/auth/new-user/new-user.component.html"
    with open(yaml_path, "r") as f:
        schema = yaml.safe_load(f)

    model_name, definition = next(iter(schema.items()))
    properties = definition.get("properties", {})
    required_fields = definition.get("required", [])

    form_fields = []

    for prop, config in properties.items():
        if not config.get("x_frontend_editable", False):
            continue

        placeholder = config.get("x_frontend_placeholder", "")
        label = config.get("x_frontend_fieldName", prop.capitalize())
        is_required = "required" if prop in required_fields else ""

        form_fields.append(f"""
<mat-form-field appearance="outline" class="full-width">
  <mat-label>{label}</mat-label>
  <input matInput placeholder="{placeholder}" [(ngModel)]="user.{prop}" name="{prop}" {is_required}>
</mat-form-field>
""")

    html_content = f"""
<div class="page">
  <h1>Create New {model_name}</h1>
  <form (ngSubmit)="createUser()">
    {''.join(form_fields)}
    <button mat-raised-button color="primary" type="submit">Create</button>
  </form>
</div>
"""

    with open(html_path, "w") as f:
        f.write(html_content)

    print(f"✅ HTML generado en {html_path}")