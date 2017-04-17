import { Component, OnInit } from '@angular/core';
import { Data } from './data';
import { Bar } from './model';
import { GraphsService } from './graphs.service';
import { ChartModule } from 'angular2-highcharts';
import { HighchartsStatic } from 'angular2-highcharts/dist/HighchartsService';

//declare let d3:any;

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers: [GraphsService]
})

export class AppComponent{


  title = 'Graphs';
  chart_one;
  chart_two;

  constructor() {
    this.chart_one = {
        series: [{
                data: [29.9, 71.5, 106.4, 129.2],
            }]
    }
    //console.log(this.chart_one);
    /*this.chart_two = {
        title : { text : 'simple chart' },
            series: [{
                data: [29.9, 71.5, 106.4, 129.2],
            }]
    }*/
    let json_data = '{"title" : "{ "text" : "simple chart" }","series": "[{data: [29.9, 71.5, 106.4, 129.2],}]"}';
    //let json_data = '{"title" : "hi bye"}';
    console.log(typeof(json_data));
    let bar : Bar = Object.assign(new Bar, JSON.parse(json_data));

    console.log(bar);
    
  }

  
}
