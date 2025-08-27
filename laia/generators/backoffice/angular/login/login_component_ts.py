import os


def modify_login_component_ts(projectName: str):
    routing_path = "backoffice/src/app/pages/login/login.component.ts"
    if not os.path.exists(routing_path):
        return

    content = f"""import {{ Component }} from '@angular/core';
import {{ FormBuilder, FormGroup, Validators }} from '@angular/forms';
import {{ AuthService }} from '../../services/auth.service';
import {{ Router }} from '@angular/router';

@Component({{
  selector: 'app-login',
  standalone: false,
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
}})
export class LoginComponent {{

  title = '{projectName}';
  loginForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {{
    this.loginForm = this.fb.group({{
      username: ['', Validators.required],
      password: ['', Validators.required]
    }});
  }}

  onSubmit(): void {{
    if (this.loginForm.valid) {{
      const {{ username, password }} = this.loginForm.value;
      this.authService.login(username, password).subscribe({{
        next: () => {{
          this.router.navigate(['/']);
        }},
        error: (error) => {{
          console.log(error);
        }}
      }})
    }} else {{
      console.log('Formulario inválido');
      this.loginForm.markAllAsTouched();
    }}
  }}

}}
"""
    with open(routing_path, "w") as f:
        f.write(content)