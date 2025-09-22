import os


def modify_models_component_scss():
    routing_path = "backoffice/src/app/pages/models/models.component.scss"
    if not os.path.exists(routing_path):
        return

    content = """mat-card {
  transition: transform 0.3s ease-in-out;

  &:hover {
    cursor: pointer;
    transform: scale(1.02);
  }
}

.no-data {
  text-align: center;
  padding: 1rem;
  color: #888;
  font-style: italic;
}

.cards {
  gap: 20px;
  display: flex;
  flex-direction: column;
}

mat-card-header {
  margin-bottom: 0px;
}
"""
    with open(routing_path, "w") as f:
        f.write(content)