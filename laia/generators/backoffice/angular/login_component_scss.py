import os


def modify_login_component_scss():
    routing_path = "backoffice/src/app/pages/login/login.component.scss"
    if not os.path.exists(routing_path):
        return

    content = """html, body {
  height: 100%;
  margin: 0;
}

.page {
  background-color: #E0E0E0;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login {
  background-color: white;
  width: 90%;
  max-width: 400px;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.login img {
  width: 48px;
  height: 48px;
  margin-bottom: 1rem;
}

.login h3 {
  margin-bottom: 2rem;
}

.full-width {
  width: 100%;
  margin-bottom: 1rem;
}

.home-button {
  position: absolute;
  width: 100%;
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
  top: 0;
}
"""
    with open(routing_path, "w") as f:
        f.write(content)