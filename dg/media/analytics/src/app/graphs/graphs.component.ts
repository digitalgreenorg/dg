import { Component } from '@angular/core';
import { configs } from './configs';
import { GraphsService } from './graphs.service';
//import { TabsetComponent } from 'ngx-bootstrap';
//import { ChartModule } from 'angular2-highcharts';
//import { HighchartsStatic } from 'angular2-highcharts/dist/HighchartsService';
declare var require: any
const Highcharts = require('highcharts/highcharts.src');
import 'highcharts/adapters/standalone-framework.src';
@Component({
    selector: 'graphs',
    templateUrl: './graphs.component.html',
    styleUrls: ['./graphs.component.css'],
    providers: [GraphsService]
})

export class GraphsComponent {
    tabs = [];
    charts = [];
    ch : any;
    constructor(private graphService: GraphsService){}
    
    ngOnInit(): void{
        configs.forEach(config => {
            //Generate tabs dynamically
            this.tabs.push(config.tabHolder); 
            //Add charts
            this.charts.push(config);
        });
        
    }

    ngAfterViewInit(): void {
        this.charts.forEach(chart => {
             this.graphService.getData(chart.chart.type, chart.chartName).then(dataList => {
                //console.log(dataList);
                Object.keys(dataList).forEach(key => {
                    if(key === chart.chartName) {
                        chart.series.push(dataList[key]);
                        chart.xAxis.categories = dataList[key].name;
                    }
                });            
             });
        });
    }

    /*feedData(dataList,config) : void {
        config.series.push(dataList[config.chartName]);
        config.xAxis.categories = dataList[config.chartName].name;
        this.charts.push(config);
    }*/
}
