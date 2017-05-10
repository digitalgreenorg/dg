import { Component, OnInit } from '@angular/core';
import { configs } from './configs';
import { GraphsService } from './graphs.service';
import { TabsetComponent } from 'ngx-bootstrap';
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
    tab = new Tab()
    
    ngOnInit(): void{
        configs.forEach(config => {
            this.graphService.getData(config.chart.type, config.chartName).then(dataList => {
                //Generate tabs dynamically
                let tab = new Tab()
                tab.id = config.chart.renderTo;
                tab.heading = config.chart.renderTo;
                this.tabs.push(tab);           
                //Feed data into each graph
                config.series.push(dataList[config.chartName]);
                config.xAxis.categories = dataList[config.chartName].name;
                this.charts.push(config);
            })
        });
    }
}

class Tab {
    id : string;
    heading : string;
}
