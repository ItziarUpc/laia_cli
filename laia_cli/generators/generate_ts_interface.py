import os
import yaml

def convert_openapi_type(openapi_type: str, format: str = None) -> str:
    type_map = {
        "string": "string",
        "integer": "number",
        "number": "number",
        "boolean": "boolean",
        "array": "any[]",
        "object": "any",
    }
    if openapi_type == "string" and format == "date-time":
        return "Date"
    return type_map.get(openapi_type, "any")

def generate_ts_interface_from_yaml(yaml_path: str, output_dir: str):
    with open(yaml_path, "r") as f:
        content = yaml.safe_load(f)

    if not isinstance(content, dict):
        print(f"⚠️  {yaml_path} is not a valid schema file.")
        return

    for model_name, schema in content.items():
        if "type" not in schema or schema["type"] != "object":
            continue

        extends = "LaiaUser" if schema.get("x-auth") else "LaiaBaseModel"
        import_path = "laiaUser" if extends == "LaiaUser" else "laiaBaseModel"

        ts_lines = [f'import {{ {extends} }} from "./{import_path}";', ""]
        ts_lines.append(f"export interface {model_name} extends {extends} {{")

        properties = schema.get("properties", {})
        required_fields = schema.get("required", [])

        for prop, details in properties.items():
            ts_type = convert_openapi_type(details.get("type", "any"), details.get("format"))
            optional = "" if prop in required_fields else "?"
            ts_lines.append(f"  {prop}{optional}: {ts_type};")

        ts_lines.append("}")

        os.makedirs(output_dir, exist_ok=True)
        filename = f"{output_dir}/{model_name[0].lower() + model_name[1:]}.ts"
        with open(filename, "w") as f:
            f.write("\n".join(ts_lines))
        print(f"✅ Interface written to {filename}")

def generate_base_interfaces(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    base_model = """export interface LaiaBaseModel {
  id: string;
  owner?: string; // ObjectId
}
"""
    laia_user = """export interface LaiaUser {
  email: string;
  password: string;
  roles: string[];
}
"""
    with open(os.path.join(output_dir, "laiaBaseModel.ts"), "w") as f:
        f.write(base_model)

    with open(os.path.join(output_dir, "laiaUser.ts"), "w") as f:
        f.write(laia_user)

    print("✅ Base interfaces (LaiaBaseModel, LaiaUser) generated.")

def generate_all_interfaces_from_schemas(schemas_dir: str, output_dir: str):
    generate_base_interfaces(output_dir)

    for filename in os.listdir(schemas_dir):
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            model_name = os.path.splitext(filename)[0]
            output_ts = os.path.join(output_dir, f"{model_name[0].lower() + model_name[1:]}.ts")

            if not os.path.exists(output_ts):
                yaml_path = os.path.join(schemas_dir, filename)
                generate_ts_interface_from_yaml(yaml_path, output_dir)
            else:
                print(f"🔁 Interface {output_ts} ya existe, se omite.")

