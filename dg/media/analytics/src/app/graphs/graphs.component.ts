import { Component } from '@angular/core';
import { chartsConfig } from './configs';
import { tabsConfig } from './configs_tab';
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
    
    constructor(private graphService: GraphsService){}
    
    ngOnInit(): void{
        //Generate tabs dynamically
        tabsConfig.forEach(tab => {
            this.tabs.push(tab);
        })

        chartsConfig.forEach(config => {
            // divs to tabs
            tabsConfig.forEach(tab => {
                if(config.chart.tabID === tab.id){
                    tab.showDivs.push(config.chart.renderTo);
                }
            })
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
            this.graphService.getData(chart.options.chart.type, chart.options.chartName).then(dataList => {
               Object.keys(dataList).forEach(key => {
                   if(key === chart.options.chartName) {
                       console.log(chart.nativeChart);
                       chart.nativeChart.xAxis[0].setCategories(dataList[key]['outerData']['categories'], true);
                       dataList[key]['outerData']['series'].forEach(entry => {
                            chart.nativeChart.addSeries(entry, true);
                        });
                   }
                });           
            });
        });
    }
}
