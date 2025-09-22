def add_auth_service():
    app_component_ts = "backoffice/src/app/services/auth.service.ts"
    with open(app_component_ts, "w") as f:
        f.write("""import { Injectable } from '@angular/core';
import { CommunicationService } from './communication.service';
import { Observable, BehaviorSubject } from 'rxjs';
import { tap } from 'rxjs/operators';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private currentUserSubject = new BehaviorSubject<any>(this.getUserFromLocalStorage());
  public currentUser$ = this.currentUserSubject.asObservable();

  constructor(
    private api: CommunicationService,
    private router: Router
  ) {}

  login(email: string, password: string): Observable<any> {
    return this.api.post('/auth/login/user/', { email, password }).pipe(
      tap((response: any) => {
        this.setSession(response);
        this.currentUserSubject.next(response.user);
      })
    );
  }

  register(username: string, email: string, password: string): Observable<any> {
    return this.api.post('/auth/register/user/', { email, password });
  }

  refreshToken(): Observable<any> {
    const refresh_token = localStorage.getItem('refresh_token');
    return this.api.post('/auth/refresh/user/', { refresh_token }).pipe(
      tap((response: any) => {
        localStorage.setItem('access_token', response.access_token);
        localStorage.setItem('refresh_token', response.refresh_token);
      })
    );
  }

  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    this.currentUserSubject.next(null);
    this.router.navigate(['/login']);
  }

  isLoggedIn(): boolean {
    return !!localStorage.getItem('access_token');
  }

  getAccessToken(): string | null {
    return localStorage.getItem('access_token');
  }

  private setSession(authResult: any): void {
    localStorage.setItem('access_token', authResult.access_token);
    localStorage.setItem('refresh_token', authResult.refresh_token);
    localStorage.setItem('user', JSON.stringify(authResult.user));
  }

  private getUserFromLocalStorage(): any {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }

  sendValidationEmail(email: string, username: string): Observable<any> {
    return this.api.post('/auth/send-validation-email', null, {
      params: { email, username },
    });
  }

  validateUser(token: string): Observable<any> {
    return this.api.get(`/auth/validate?token=${token}`);
  }
}
""") 