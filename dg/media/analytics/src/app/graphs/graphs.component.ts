import { Component,OnInit, AfterViewInit } from '@angular/core';
import { chartsConfig } from './configs';
import { tabsConfig } from './configs_tab';
import { GraphsService } from './graphs.service';

@Component({
    selector: 'graphs',
    templateUrl: './graphs.component.html',
    styleUrls: ['./graphs.component.css'],
    providers: [GraphsService]
})

export class GraphsComponent implements OnInit, AfterViewInit{
    tabs = [];
    charts = [];

    constructor(private graphService: GraphsService) { }

    ngOnInit(): void {
        //Generate tabs dynamically
        tabsConfig.forEach(tab => {
        this.tabs.push(tab);
        });
        chartsConfig.forEach(config => {
            //Add divs to tabs
            tabsConfig.forEach(tab => {
                if(config.chart.tab.id === tab.id){
                    tab.showDivs.push({
                        'id' : config.chart.renderTo,
                        'class' : config.chart.tab.class
                    });
                }
            })
            //Add empty charts to DOM
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
            chart.nativeChart.showLoading();
            this.graphService.getData(chart.options.chart.type, chart.options.chartName).then(dataList => {
                Object.keys(dataList).forEach(key => {
                    //Find already displayed cart to enter data
                    if (key === chart.options.chartName) {
                        chart.nativeChart.hideLoading();
                        dataList[key]['outerData']['series'].forEach(entry => {
                            chart.nativeChart.addSeries(entry, true);
                        });
                        if (chart.options.chart.drillDown == true) {
                            dataList[key]['innerData'].forEach(drilldownEntry => {
                                chart.options.drilldown.series.push(drilldownEntry);
                          });
                        }
                    }
                });
            });
        });
    }
}
