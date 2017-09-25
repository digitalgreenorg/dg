import { BrowserModule, Title } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { DatePipe } from '@angular/common';

import { HighchartsStatic } from 'angular2-highcharts/dist/HighchartsService';
import { ChartModule } from 'angular2-highcharts'
import { InfiniteScrollModule } from 'angular2-infinite-scroll';

import { TabsModule } from 'ngx-bootstrap/tabs';
import { ButtonsModule } from 'ngx-bootstrap';
import { CollapseModule } from 'ngx-bootstrap/collapse';
import { PerfectScrollbarModule, PerfectScrollbarConfigInterface } from 'ngx-perfect-scrollbar';
import { MyDatePickerModule } from 'mydatepicker';

import { AppComponent } from './app.component';
import { CardsComponent } from './cards/cards.component';
import { FiltersComponent } from './filters/filters.component';
import { GraphsComponent } from './graphs/graphs.component';
import { NavsComponent } from './navs/navs.component';

import { GraphsService } from './navs/navs.service';
import { CardsService } from './cards/cards.service';
import { GetFilterDataService } from './filters/get-filter-data.service';
import { SharedService } from './shared.service';
import { GlobalFilterService } from './global-filter/global-filter.service'

import { SearchPipe } from './filters/search.pipe';

import { BsDropdownModule } from 'ngx-bootstrap';
import { GlobalFilterComponent } from './global-filter/global-filter.component';
import { GlobalFilterSharedService } from './global-filter/global-filter-shared.service';
import { FooterComponent } from './footer/footer.component';

declare var require: any;
export function highchartsFactory() {
  const highChart = require('highcharts/highstock');
  const drillDown = require('highcharts/modules/drilldown');
  const highcharts_more = require('highcharts/highcharts-more');
  const solid_gauge = require('highcharts/modules/solid-gauge');
  const exp = require('highcharts/modules/exporting');
  const noData = require('highcharts/modules/no-data-to-display');
  highChart.setOptions({
    lang: {
      thousandsSep: ','
    }
  });
  drillDown(highChart);
  exp(highChart);
  highcharts_more(highChart);
  solid_gauge(highChart);
  // noData(highChart);
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
    NavsComponent,
    GlobalFilterComponent,
    FooterComponent,
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
    BsDropdownModule.forRoot(),
    CollapseModule.forRoot(),
  ],
  providers: [{
    provide: HighchartsStatic,
    useFactory: highchartsFactory,
  },
    GraphsService, CardsService, DatePipe, GetFilterDataService, SharedService, GlobalFilterService, GlobalFilterSharedService, Title],
  bootstrap: [AppComponent]
})
export class AppModule { }
