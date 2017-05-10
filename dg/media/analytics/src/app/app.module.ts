import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { AnalyticsTableComponent } from './analytics-table/analytics-table.component';
import { GetDataFromServerService } from './get-data-from-server/get-data-from-server.service';
import { Ng2TableModule } from 'ng2-table/ng2-table';
import { PaginationModule } from 'ngx-bootstrap/pagination';
import { CollapseModule } from 'ngx-bootstrap';
import { FiltersComponent } from './filters/filters.component';
import { SearchPipe } from './filters/search.pipe';


@NgModule({
  declarations: [
    AppComponent,
    AnalyticsTableComponent,
    FiltersComponent,
    SearchPipe,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    Ng2TableModule,
    PaginationModule.forRoot(),
    CollapseModule
  ],
  providers: [GetDataFromServerService],
  bootstrap: [AppComponent]
})
export class AppModule { }
