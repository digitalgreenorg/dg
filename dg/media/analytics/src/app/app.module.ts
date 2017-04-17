import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { NvD3Module } from 'angular2-nvd3';
import { ChartModule } from 'angular2-highcharts'
import { HighchartsStatic } from 'angular2-highcharts/dist/HighchartsService';
import { AppComponent } from './app.component';

declare var require: any;
export function highchartsFactory() {
  return require('highcharts');
}

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    NvD3Module,
    ChartModule
  ],
  providers: [{
      provide: HighchartsStatic,
      useFactory: highchartsFactory
    },],
  bootstrap: [AppComponent]
})
export class AppModule { }
