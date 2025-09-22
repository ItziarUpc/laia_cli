import os


def modify_home_component_scss():
    routing_path = "backoffice/src/app/pages/home/home.component.scss"
    if not os.path.exists(routing_path):
        return

    content = """.cards {
    display: flex;
    flex-wrap: wrap;
    gap: 30px;
    justify-content: center;
}  

mat-card {
    width: 300px;
    flex: 1 1 300px;
    transition: transform 0.3s ease-in-out;

    &:hover {
        cursor: pointer;
        transform: scale(1.05);
    }
}

mat-card-title-group {
    margin-bottom: 20px;
}

.home-card {
    max-width: 450px;
}
"""
    with open(routing_path, "w") as f:
        f.write(content)