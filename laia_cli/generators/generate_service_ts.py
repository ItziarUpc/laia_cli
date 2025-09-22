import os


def generate_ts_service(model_name: str):
    camel = model_name.lower()
    pascal = model_name[0].upper() + model_name[1:]

    service_code = f"""import {{ Injectable }} from '@angular/core';
import {{ CommunicationService }} from './communication.service';
import {{ Observable }} from 'rxjs';
import {{ {pascal} }} from '../interfaces/{camel}';

@Injectable({{
  providedIn: 'root',
}})
export class {pascal}Service {{
  private base = '/{camel}';

  constructor(private api: CommunicationService) {{}}

  getAll(skip: number, limit: number, filters: any = {{}}, orders: any = {{}}): Observable<any> {{
    return this.api.post<{pascal}[]>(`${{this.base}}s/?skip=${{skip}}&limit=${{limit}}`, {{ filters, orders }});
  }}

  getById(id: string): Observable<{pascal}> {{
    return this.api.get<{pascal}>(`${{this.base}}/${{id}}`);
  }}

  create(data: {pascal}): Observable<{pascal}> {{
    return this.api.post<{pascal}>(`${{this.base}}`, data);
  }}

  update(id: string, data: {pascal}): Observable<{pascal}> {{
    return this.api.put<{pascal}>(`${{this.base}}/${{id}}`, data);
  }}

  delete(id: string): Observable<any> {{
    return this.api.delete<any>(`${{this.base}}/${{id}}`);
  }}
}}
"""
    
    service_path = f"backoffice/src/app/services/{camel}.service.ts"

    os.makedirs(os.path.dirname(service_path), exist_ok=True)

    with open(service_path, "w") as f:
        f.write(service_code)