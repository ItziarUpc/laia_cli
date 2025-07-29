import os


def modify_home_component_html():
    routing_path = "backoffice/src/app/pages/home/home.component.html"
    if not os.path.exists(routing_path):
        return

    content = """<div class="page">
    <h1>{{ projectName }}</h1>
    <div class="cards">
        <mat-card class="home-card" appearance="outlined" [routerLink]="['/auth']">
          <mat-card-header>
            <mat-card-title-group>
              <mat-icon>people</mat-icon>
              <mat-card-title>Auth</mat-card-title>
            </mat-card-title-group>
          </mat-card-header>
          <mat-card-content>
            Manage users, logins, and account validations using secure JWT and email.
          </mat-card-content>
        </mat-card>
        <mat-card class="home-card" appearance="outlined" [routerLink]="['/schemas']">
          <mat-card-header>
            <mat-card-title-group>
              <mat-icon>account_tree</mat-icon>
              <mat-card-title>Schemas</mat-card-title>
            </mat-card-title-group>
          </mat-card-header>
          <mat-card-content>
            Define and organize the data schemas that structure your models and their relationships.
          </mat-card-content>
        </mat-card>
        <mat-card class="home-card" appearance="outlined" [routerLink]="['/models']">
            <mat-card-header>
              <mat-card-title-group>
                <mat-icon>storage</mat-icon>
                <mat-card-title>Models</mat-card-title>
              </mat-card-title-group>
            </mat-card-header>
            <mat-card-content>
              View and manage stored data in your collections or tables with ease.
            </mat-card-content>
        </mat-card>
        <mat-card class="home-card" appearance="outlined" [routerLink]="['/storage']">
            <mat-card-header>
              <mat-card-title-group>
                <mat-icon>cloud_upload</mat-icon>
                <mat-card-title>Storage</mat-card-title>
              </mat-card-title-group>
            </mat-card-header>
            <mat-card-content>
              Upload, manage, and access files securely with cloud storage support.
            </mat-card-content>
        </mat-card>
        <mat-card class="home-card" appearance="outlined">
          <mat-card-header>
            <mat-card-title-group>
              <mat-icon>smartphone</mat-icon>
              <mat-card-title>Frontend</mat-card-title>
            </mat-card-title-group>
          </mat-card-header>
          <mat-card-content>
            View and manage automatically generated user interfaces based on your models and configurations.
          </mat-card-content>
        </mat-card>
    </div>
</div>
"""
    with open(routing_path, "w") as f:
        f.write(content)