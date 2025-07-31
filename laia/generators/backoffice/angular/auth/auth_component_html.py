import os


def modify_auth_component_html():
    routing_path = "backoffice/src/app/pages/auth/auth.component.html"
    if not os.path.exists(routing_path):
        return

    content = """<div class="page">
    <h1>Auth</h1>
    <mat-card class="example-card" appearance="outlined">
        <mat-card-header>
          <mat-card-title-group>
            <mat-icon routerLink="/auth/new-user">add</mat-icon>
            <mat-card-title>Users</mat-card-title>
          </mat-card-title-group>
        </mat-card-header>
        <mat-card-content>
            <mat-form-field appearance="outline" class="full-width">
                <mat-label>Search...</mat-label>
                <input matInput type="text" [(ngModel)]="searchQuery">
                <mat-icon matSuffix>search</mat-icon>
            </mat-form-field>
            <app-table
            [headers]="headers"
            [data]="users">
            </app-table>
        </mat-card-content>
        <mat-paginator
          [length]="total"
          [pageSize]="pageSize"
          [pageSizeOptions]="[10, 25, 50]"
          (page)="onPageChange($event)">
        </mat-paginator>
    </mat-card>
</div>
"""
    with open(routing_path, "w") as f:
        f.write(content)