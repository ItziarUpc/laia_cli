def modify_app_component_ts():
    app_component_ts = "backoffice/src/app/app.component.ts"
    with open(app_component_ts, "w") as f:
        f.write(f"""import {{ Component }} from '@angular/core';
import {{ Router }} from '@angular/router';
import {{ AuthService }} from './services/auth.service';

@Component({{
  selector: 'app-root',
  templateUrl: './app.component.html',
  standalone: false,
  styleUrls: ['./app.component.scss']
}})
export class AppComponent {{
  title = 'RouteInjector';

  constructor(
    private router: Router,
    public authService: AuthService
  ) {{}}
                
  isLogin(): boolean {{
    return this.router.url === '/login';
  }}
}}
""")