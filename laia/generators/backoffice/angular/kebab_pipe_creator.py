def create_kebab_pipe():
    with open("backoffice/src/app/pipes/kebab-case.pipe.ts", "w") as f:
        f.write("""
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'kebabCase', standalone: false })
export class KebabCasePipe implements PipeTransform {
  transform(value: string): string {
    return value
      .replace(/([a-z])([A-Z])/g, '$1-$2')
      .replace(/\s+/g, '-')
      .toLowerCase();
  }
}
""")