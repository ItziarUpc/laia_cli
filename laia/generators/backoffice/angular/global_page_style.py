import os


def modify_global_page_style():
    path = "backoffice/src/styles.scss"
    if not os.path.exists(path):
        return

    with open(path, "r") as f:
        content = f.read()

    additions = []

    if ".page" not in content:
        additions.append("\n.page {\n    padding: 20px;\n}")

    if ".no-mobile" not in content:
        additions.append(
            "\n.no-mobile {\n"
            "    @media (max-width: 768px) {\n"
            "        display: none;\n"
            "    }\n"
            "}"
        )

    if ".full-width" not in content:
        additions.append("\n.full-width {\n    width: 100%;\n}")

    if "mat-card-header" not in content:
        additions.append("\nmat-card-header {\n    margin-bottom: 20px;\n}")

    if additions:
        with open(path, "a") as f:
            f.write("\n".join(additions) + "\n")