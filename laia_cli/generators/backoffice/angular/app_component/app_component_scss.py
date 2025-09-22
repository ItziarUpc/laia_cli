def modify_app_component_scss():
    with open("backoffice/src/app/app.component.scss", "w") as f:
        f.write(""".example-spacer {
  flex: 1 1 auto;
}

img {
  max-width: 40px;
  margin-right: 30px;
}

.example-container {
  height: 100vh;
}

mat-sidenav {
  width: 250px;
  background: #E0E0E0;
  color: white;
  border-right: 2px solid #979797;
}

mat-toolbar {
  position: sticky;
  top: 0;
  z-index: 2;
  background: #E0E0E0;
  border-bottom: 2px solid #979797;
}

.main-content {
  padding: 16px;
}

.mat-drawer {
  border-top-right-radius: 0;
}
                
.nav-item .nav-content {
  display: flex;
  align-items: center;

  mat-icon {
    margin-right: 8px;
    font-size: 20px;
  }

  span {
    line-height: 1;
  }
}
                
mat-sidenav {
  @media (max-width: 768px) {
    width: 8vh;
  }
}
                
.nav-item {
  color: #b3b1b1;

  .mat-icon {
    color: #b3b1b1;
  }

  span {
    color: #b3b1b1;
  }

  &.active-link {
    color: #000;

    .mat-icon {
      color: #000;
    }

    span {
      color: #000;
    }
  }
}
""")