import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { AnalyticsTableComponent } from './analytics-table/analytics-table.component';
import { GetDataFromServerService } from './get-data-from-server/get-data-from-server.service';

@NgModule({
  declarations: [
    AppComponent,
    AnalyticsTableComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule
  ],
  providers: [GetDataFromServerService],
  bootstrap: [AppComponent]
})
export class AppModule { }
