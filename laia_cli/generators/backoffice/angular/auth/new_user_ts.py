def modify_new_user_component_ts():
    ts_path = "backoffice/src/app/pages/auth/new-user/new-user.component.ts"
    content = """import { Component } from '@angular/core';
import { UserService } from '../../../services/user.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-new-user',
  standalone: false,
  templateUrl: './new-user.component.html',
  styleUrl: './new-user.component.scss'
})
export class NewUserComponent {

  user: any = {};

  constructor(
    private userService: UserService,
    private router: Router
  ) {}

  createUser(): void {
    this.userService.create(this.user).subscribe(() => {
      this.router.navigate(['/auth']);
    });
  }

}
"""
    with open(ts_path, "w") as f:
        f.write(content)
    print(f"✅ TS generado en {ts_path}")