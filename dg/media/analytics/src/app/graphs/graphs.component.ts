import { Component } from '@angular/core';
import { configs } from './configs';
import { GraphsService } from './graphs.service';
//import { TabsetComponent } from 'ngx-bootstrap';
//import { ChartModule } from 'angular2-highcharts';
//import { HighchartsStatic } from 'angular2-highcharts/dist/HighchartsService';

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
            this.charts.push({
                options: config,
                nativeChart: null // To be obtained with saveInstance
            });
        });
        
    }

    saveInstance(chartInstance, chart) {
        chart.nativeChart = chartInstance;
    }

    ngAfterViewInit(): void {
        this.charts.forEach(chart => {
            console.log(chart.options.chart.type);
             this.graphService.getData(chart.options.chart.type, chart.options.chartName).then(dataList => {
                //console.log(dataList);
                Object.keys(dataList).forEach(key => {
                    if(key === chart.options.chartName) {
                        chart.nativeChart.addSeries(dataList[key], true);
                    }
                });            
             });
        });
    }
}
