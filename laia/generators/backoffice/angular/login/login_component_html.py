import os


def modify_login_component_html():
    routing_path = "backoffice/src/app/pages/login/login.component.html"
    if not os.path.exists(routing_path):
        return

    content = """<div class="page">
  <div class="home-button">
    <button mat-icon-button [routerLink]="['/']">
      <mat-icon>home</mat-icon>
    </button>
  </div>

  <div class="login">

    <img src="/favicon.ico" alt="logo" />
    <h3>{{ title }}</h3>

    <form [formGroup]="loginForm" (ngSubmit)="onSubmit()">
      <mat-form-field appearance="fill" class="full-width">
        <mat-label>Email</mat-label>
        <input matInput formControlName="username" type="text" />
        <mat-error *ngIf="loginForm.get('username')?.hasError('required')">
          This field is required
        </mat-error>
      </mat-form-field>

      <mat-form-field appearance="fill" class="full-width">
        <mat-label>Password</mat-label>
        <input matInput formControlName="password" type="password" />
        <mat-error *ngIf="loginForm.get('password')?.hasError('required')">
          This field is required
        </mat-error>
      </mat-form-field>

      <button mat-raised-button color="primary" class="full-width" type="submit">
        Sign in
      </button>
    </form>
  </div>
</div>
"""
    with open(routing_path, "w") as f:
        f.write(content)