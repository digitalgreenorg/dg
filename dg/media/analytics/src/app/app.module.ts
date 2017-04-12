import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { AnalyticsTableComponent } from './analytics-table/analytics-table.component';
import { GetDataFromServerService } from './get-data-from-server/get-data-from-server.service';
import { Ng2TableModule } from 'ng2-table/ng2-table';
import { PaginationModule } from 'ng2-bootstrap/pagination';

@NgModule({
  declarations: [
    AppComponent,
    AnalyticsTableComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    Ng2TableModule,
    PaginationModule,
  ],
  providers: [GetDataFromServerService],
  bootstrap: [AppComponent]
})
export class AppModule { }
