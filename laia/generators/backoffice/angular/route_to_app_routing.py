import os


def add_route_to_app_routing():
    routing_path = "backoffice/src/app/app-routing.module.ts"
    if not os.path.exists(routing_path):
        return  # No routing module

    content = """import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { AuthComponent } from './pages/auth/auth.component';
import { ModelsComponent } from './pages/models/models.component';
import { StorageComponent } from './pages/storage/storage.component';
import { SettingsComponent } from './pages/settings/settings.component';
import { AuthGuard } from './services/auth.guard';
import { LoginComponent } from './pages/login/login.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'login', component: LoginComponent },
  { path: 'auth', component: AuthComponent, canActivate: [AuthGuard] },
  { path: 'models', component: ModelsComponent, canActivate: [AuthGuard] },
  { path: 'storage', component: StorageComponent, canActivate: [AuthGuard] },
  { path: 'settings', component: SettingsComponent, canActivate: [AuthGuard] },
  { path: '**', redirectTo: 'login', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
"""
    with open(routing_path, "w") as f:
        f.write(content)