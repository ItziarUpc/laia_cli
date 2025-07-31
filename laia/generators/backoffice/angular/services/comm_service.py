def add_comm_service():
    app_component_ts = "backoffice/src/app/services/communication.service.ts"
    with open(app_component_ts, "w") as f:
        f.write("""import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class CommunicationService {
  private baseUrl = 'http://localhost:8005';

  constructor(private http: HttpClient) {}

  get<T>(url: string): Observable<T> {
    return this.http.get<T>(`${this.baseUrl}${url}`);
  }

  post<T>(url: string, data: any, options?: {
    headers?: HttpHeaders;
    params?: HttpParams | { [param: string]: string | string[] };
  }): Observable<T> {
    return this.http.post<T>(`${this.baseUrl}${url}`, data, options);
  }

  put<T>(url: string, data: any): Observable<T> {
    return this.http.put<T>(`${this.baseUrl}${url}`, data);
  }

  delete<T>(url: string): Observable<T> {
    return this.http.delete<T>(`${this.baseUrl}${url}`);
  }
}
""")