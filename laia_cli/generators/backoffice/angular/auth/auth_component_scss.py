import os


def modify_auth_component_scss():
    routing_path = "backoffice/src/app/pages/auth/auth.component.scss"
    if not os.path.exists(routing_path):
        return

    content = """.full-width {
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
    with open(routing_path, "w") as f:
        f.write(content)