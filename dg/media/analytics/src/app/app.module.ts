import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { DatePipe } from '@angular/common';

import { HighchartsStatic } from 'angular2-highcharts/dist/HighchartsService';
import { ChartModule } from 'angular2-highcharts'
import { InfiniteScrollModule } from 'angular2-infinite-scroll';

import { TabsModule } from 'ngx-bootstrap/tabs';
import { ButtonsModule } from 'ngx-bootstrap';
import { PerfectScrollbarModule, PerfectScrollbarConfigInterface } from 'ngx-perfect-scrollbar';
import { MyDatePickerModule } from 'mydatepicker';

import { AppComponent } from './app.component';
import { CardsComponent } from './cards/cards.component';
import { FiltersComponent } from './filters/filters.component';
import { GraphsComponent } from './graphs/graphs.component';

import { GraphsService } from './graphs/graphs.service';
import { CardsService } from './cards/cards.service';
import { GetFilterDataService } from './filters/get-filter-data.service';
import { SharedService } from './shared.service';

import { SearchPipe } from './filters/search.pipe';

declare var require: any;
export function highchartsFactory() {
  const highChart = require('highcharts');
  const drillDown = require('highcharts/modules/drilldown');
  const exp = require('highcharts/modules/exporting');
  drillDown(highChart);
  exp(highChart)
  return highChart;
}

const PERFECT_SCROLLBAR_CONFIG: PerfectScrollbarConfigInterface = {
  suppressScrollX: true,
  useBothWheelAxes: true,
  suppressScrollY: false,
  minScrollbarLength: 50,
};

@NgModule({
  declarations: [
    AppComponent,
    GraphsComponent,
    FiltersComponent,
    SearchPipe,
    CardsComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule, ChartModule,
    TabsModule.forRoot(),
    MyDatePickerModule,
    ButtonsModule.forRoot(),
    InfiniteScrollModule,
    PerfectScrollbarModule.forRoot(PERFECT_SCROLLBAR_CONFIG),
  ],
  providers: [{
    provide: HighchartsStatic,
    useFactory: highchartsFactory,
  },
    GraphsService, CardsService, DatePipe, GetFilterDataService, SharedService],
  bootstrap: [AppComponent]
})
export class AppModule { }
