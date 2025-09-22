import os
import yaml

from laia_cli.generators.files_generator import create_file

def generate_schema():
    print("\n📦 Generating new OpenAPI schema...")

    schema_name = input("Schema name (e.g. User): ").strip()
    if not schema_name:
        print("❌ Schema name is required.")
        return

    use_auth = input("Require auth? [y/N]: ").strip().lower() == "y"

    print("➕ Define properties (press Enter without name to finish)")
    properties = {}

    while True:
        prop_name = input("  Property name: ").strip()
        if not prop_name:
            break

        prop_type = input("    Type (string, integer, boolean, etc.): ").strip()
        description = input("    Description: ").strip()

        properties[prop_name] = {
            "type": prop_type,
            "description": description
        }

    # Generar el contenido YAML
    schema = {
        schema_name: {
            "type": "object",
            "properties": properties
        }
    }

    if use_auth:
        schema[schema_name]["x-auth"] = True

    # Crear archivo en backend/openapi/schemas
    output_dir = os.path.join("backend", "openapi", "schemas")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{schema_name}.yaml")

    with open(output_path, "w") as f:
        yaml.dump(schema, f, sort_keys=False)

    print(f"\n✅ Schema {schema_name} created at {output_path}")