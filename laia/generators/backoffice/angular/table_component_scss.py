import os


def modify_table_component_scss():
    routing_path = "backoffice/src/app/components/table/table.component.scss"
    if not os.path.exists(routing_path):
        return

    content = """.table {
  width: 100%;
  border-collapse: collapse;

  th, td {
    padding: 0.75rem;
    border: 1px solid #ccc;
    text-align: left;
  }

  thead {
    background-color: #f0f0f0;
  }
}

.no-data {
  text-align: center;
  padding: 1rem;
  color: #888;
  font-style: italic;
}
"""
    with open(routing_path, "w") as f:
        f.write(content)