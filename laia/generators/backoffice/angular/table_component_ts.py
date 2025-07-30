import os


def modify_table_component_ts():
  ts_path = "backoffice/src/app/components/table/table.component.ts"
  if not os.path.exists(ts_path):
      return

  with open(ts_path, "r") as f:
      lines = f.readlines()

  new_lines = []
  added = False

  for line in lines:
    if line.strip().startswith("import { Component") and "Input" not in line:
        new_lines.append("import { Component, Input } from '@angular/core';\n")
        continue

    new_lines.append(line)

    if not added and "export class TableComponent" in line:
        new_lines.append("  @Input() headers: string[] = [];\n")
        new_lines.append("  @Input() fields: string[] = [];\n")
        new_lines.append("  @Input() data: any[] = [];\n")
        added = True

  with open(ts_path, "w") as f:
      f.writelines(new_lines)