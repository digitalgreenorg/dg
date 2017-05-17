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
/*            this.ch = new Highcharts.Chart(config);
            console.log(this.ch);*/
            this.graphService.getData(config.chart.type, config.chartName).then(dataList => {
                //console.log(dataList);
                Object.keys(dataList).forEach(key => {
                    if(key === config.chartName) {
                        config.series.push(dataList[key]);
                        config.xAxis.categories = dataList[key].name;
                        this.charts.push(config); 
                        //this.cdRef.detectChanges();
                    }
                });            
             }); 
            
        });
        
    }

    ngAfterViewInit(): void {
        this.charts.forEach(chart => {
             
        });
    }

    /*feedData(dataList,config) : void {
        config.series.push(dataList[config.chartName]);
        config.xAxis.categories = dataList[config.chartName].name;
        this.charts.push(config);
    }*/
}
