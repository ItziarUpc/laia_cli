def modify_new_user_component_scss():
    scss_path = "backoffice/src/app/pages/auth/new-user/new-user.component.scss"
    content = """.form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-width: 500px;
  margin: auto;
}

button {
  align-self: flex-start;
}
"""
    with open(scss_path, "w") as f:
        f.write(content)
    print(f"✅ SCSS generado en {scss_path}")
