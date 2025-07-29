import os


def modify_home_component_ts(project_name: str):
    ts_path = "backoffice/src/app/pages/home/home.component.ts"
    if not os.path.exists(ts_path):
        return

    with open(ts_path, "r") as f:
        lines = f.readlines()

    new_lines = []
    added = False

    for line in lines:
        new_lines.append(line)
        if not added and "export class HomeComponent" in line:
            new_lines.append(f"  projectName = '{project_name}';\n")
            added = True

    with open(ts_path, "w") as f:
        f.writelines(new_lines)