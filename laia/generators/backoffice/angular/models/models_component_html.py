import os


def modify_models_component_html():
    routing_path = "backoffice/src/app/pages/models/models.component.html"
    if not os.path.exists(routing_path):
        return

    content = """<div class="page">
  <h1>Models</h1>

  <div *ngIf="models.length === 0" class="no-data">
    There is no data yet ...
  </div>

  <div class="cards" *ngIf="models.length > 0">
    <mat-card
      class="example-card"
      appearance="outlined"
      *ngFor="let model of models"
      [routerLink]="['/models', model | kebabCase]"
    >
      <mat-card-header>
        <mat-card-title-group>
          <mat-icon>arrow_forward</mat-icon>
          <mat-card-title>{{ model }}</mat-card-title>
        </mat-card-title-group>
      </mat-card-header>
      <mat-card-content></mat-card-content>
    </mat-card>
  </div>
</div>
"""
    with open(routing_path, "w") as f:
        f.write(content)