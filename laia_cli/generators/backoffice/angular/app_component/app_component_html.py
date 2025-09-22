def modify_app_component_html():
    with open("backoffice/src/app/app.component.html", "w") as f:
        f.write("""
<mat-toolbar *ngIf="!isLogin()">
    <img src="/favicon.ico" />
    <span>{{ title }}</span>
    <span class="example-spacer"></span>
    <button mat-icon-button [routerLink]="['/login']" *ngIf="!this.authService.isLoggedIn()">
      <mat-icon>login</mat-icon>
    </button>
    <button mat-icon-button (click)="this.authService.logout()" *ngIf="this.authService.isLoggedIn()">
      <mat-icon>logout</mat-icon>
    </button>
</mat-toolbar>
<mat-sidenav-container class="example-container" *ngIf="!isLogin()">
    <mat-sidenav mode="side" opened>
      <mat-nav-list>
        <a mat-list-item [routerLink]="'/'" routerLinkActive="active-link" [routerLinkActiveOptions]="{ exact: true }" class="nav-item">
          <span class="nav-content">
            <mat-icon>home</mat-icon>
            <span class="no-mobile">Home</span>
          </span>
        </a>
        <a mat-list-item [routerLink]="'/auth'" routerLinkActive="active-link" [routerLinkActiveOptions]="{ exact: true }" class="nav-item">
          <span class="nav-content">
            <mat-icon>people</mat-icon>
            <span class="no-mobile">Auth</span>
          </span>
        </a>
        <a mat-list-item [routerLink]="'/schemas'" routerLinkActive="active-link" [routerLinkActiveOptions]="{ exact: true }" class="nav-item">
          <span class="nav-content">
            <mat-icon>account_tree</mat-icon>
            <span class="no-mobile">Schemas</span>
          </span>
        </a>
        <a mat-list-item [routerLink]="'/models'" routerLinkActive="active-link" [routerLinkActiveOptions]="{ exact: true }" class="nav-item">
          <span class="nav-content">
            <mat-icon>storage</mat-icon>
            <span class="no-mobile">Models</span>
          </span>
        </a>
        <a mat-list-item [routerLink]="'/storage'" routerLinkActive="active-link" [routerLinkActiveOptions]="{ exact: true }" class="nav-item">
          <span class="nav-content">
            <mat-icon>cloud_upload</mat-icon>
            <span class="no-mobile">Storage</span>
          </span>
        </a>
        <a mat-list-item [routerLink]="'/settings'" routerLinkActive="active-link" [routerLinkActiveOptions]="{ exact: true }" class="nav-item">
          <span class="nav-content">
            <mat-icon>settings</mat-icon>
            <span class="no-mobile">Settings</span>
          </span>
        </a>
      </mat-nav-list>
    </mat-sidenav>
  
    <mat-sidenav-content>
      <div class="main-content">
        <router-outlet></router-outlet>
      </div>
    </mat-sidenav-content>
</mat-sidenav-container>
                
<router-outlet *ngIf="isLogin()"></router-outlet>
""")