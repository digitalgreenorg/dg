import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AsyncPipe } from '@angular/common';
import { HttpModule } from '@angular/http';
import { NvD3Module } from 'angular2-nvd3';
import { ChartModule } from 'angular2-highcharts'
import { HighchartsStatic } from 'angular2-highcharts/dist/HighchartsService';
import { AppComponent } from './app.component';
import { GraphsComponent } from './graphs/graphs.component';
import { GraphsService } from './graphs/graphs.service';
import { TabsModule } from 'ngx-bootstrap/tabs';

declare var require: any;
export function highchartsFactory() {
  const highChart = require('highcharts');
  const drillDown = require('highcharts/modules/drilldown');
  drillDown(highChart);
  return highChart;
}

@NgModule({
  declarations: [
    AppComponent,
    GraphsComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    NvD3Module,
    ChartModule,
    TabsModule.forRoot()
  ],
  providers: [{
      provide: HighchartsStatic,
      useFactory: highchartsFactory,
    },
    GraphsService, AsyncPipe],
  bootstrap: [AppComponent]
})
export class AppModule { }
