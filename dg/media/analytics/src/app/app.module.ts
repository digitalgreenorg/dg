import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { AnalyticsTableComponent } from './analytics-table/analytics-table.component';
import { GetDataFromServerService } from './get-data-from-server/get-data-from-server.service';
import { GetFilterDataService } from './get-filter-data.service';
import { Ng2TableModule } from 'ng2-table/ng2-table';
import { PaginationModule } from 'ngx-bootstrap/pagination';
import { CollapseModule } from 'ngx-bootstrap';
import { FiltersComponent } from './filters/filters.component';
import { SearchPipe } from './filters/search.pipe';

import { TopBarDataComponent } from './top-bar-data/top-bar-data.component';
import { TopBarDataService } from './top-bar-data.service';
import { SharedService } from './shared.service';

import { AccordionModule } from '../../node_modules/ngx-bootstrap';
import { KeysPipe } from './keys.pipe';
import { GraphComponent } from './graph/graph.component';
import { NvD3Module } from '../../node_modules/angular2-nvd3';
import { MyDatePickerModule } from 'mydatepicker';
import { ButtonsModule } from 'ngx-bootstrap';
import { DatePipe } from '@angular/common';
import { CardComponent } from './top-bar-data/card/card.component';

@NgModule({
  declarations: [
    AppComponent,
    AnalyticsTableComponent,
    FiltersComponent,
    SearchPipe,
    TopBarDataComponent,
    KeysPipe,
    GraphComponent,
    CardComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    Ng2TableModule,
    PaginationModule.forRoot(),
    CollapseModule,
    AccordionModule.forRoot(),
    NvD3Module,
    MyDatePickerModule,
    ButtonsModule.forRoot(),
  ],
  providers: [TopBarDataService, DatePipe, GetDataFromServerService, GetFilterDataService, SharedService],
  bootstrap: [AppComponent]
})
export class AppModule { }
