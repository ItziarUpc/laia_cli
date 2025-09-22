import os


def modify_table_component_html():
    routing_path = "backoffice/src/app/components/table/table.component.html"
    if not os.path.exists(routing_path):
        return

    content = """<table class="table" *ngIf="data && data.length > 0; else noData">
    <thead>
      <tr>
        <th *ngFor="let header of headers">{{ header }}</th>
      </tr>
    </thead>
    <tbody>
      @if (fields.length == 0) {
        <tr *ngFor="let row of data">
          <td *ngFor="let header of headers">{{ row[header] }}</td>
        </tr>
      }
      @else {
        <tr *ngFor="let row of data">
          <td *ngFor="let field of fields">{{ row[field] }}</td>
        </tr>
      }
    </tbody>
</table>

<ng-template #noData>
    <div class="no-data">There is no data yet ...</div>
</ng-template>
"""
    with open(routing_path, "w") as f:
        f.write(content)