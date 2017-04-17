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
    bar : Bar = {
        chart: {
        type: 'bar'
    },
    title: {
        text: 'Historic World Population by Region'
    },
    xAxis: {
        categories: ['Africa', 'America', 'Asia', 'Europe', 'Oceania'],
    },
    yAxis: {
        min: 0,
        title: {
            text: 'Population (millions)',
            align: 'high'
        },
        labels: {
            overflow: 'justify'
        }
    },
    tooltip: {
        valueSuffix: ' millions'
    },
    plotOptions: {
        bar: {
            dataLabels: {
                enabled: true
            }
        }
    },
    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'top',
        floating: true,
        borderWidth: 1,
        //backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
        shadow: true
    },
    series: [{
        data: [107, 31, 635, 203, 2]
    }]}

  /*title = 'Graphs';
  chart_one;
  chart_two;

  constructor() {
    this.chart_one = {
        title : { text : 'simple chart' },
            series: [{
                data: [29.9, 71.5, 106.4, 129.2],
            }]
    }
    /*this.chart_two = {
        title : { text : 'simple chart' },
            series: [{
                data: [29.9, 71.5, 106.4, 129.2],
            }]
    }
    this.chart_two =  {
    chart: {
        type: 'bar'
    },
    title: {
        text: 'Historic World Population by Region'
    },
    xAxis: {
        categories: ['Africa', 'America', 'Asia', 'Europe', 'Oceania'],
    },
    yAxis: {
        min: 0,
        title: {
            text: 'Population (millions)',
            align: 'high'
        },
        labels: {
            overflow: 'justify'
        }
    },
    tooltip: {
        valueSuffix: ' millions'
    },
    plotOptions: {
        bar: {
            dataLabels: {
                enabled: true
            }
        }
    },
    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'top',
        floating: true,
        borderWidth: 1,
        //backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
        shadow: true
    },
    series: [{
        data: [107, 31, 635, 203, 2]
    }]
};
  }*/
}
