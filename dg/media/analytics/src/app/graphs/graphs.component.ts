import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
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
    @ViewChild('staticTabs') staticTabs: TabsetComponent;
    tabs = [];
    charts = [];
    constructor(private graphService: GraphsService){}
    
    tab = new Tab()
    ngOnInit(): void{
        configs.forEach(config => {
            this.graphService.getData(config.chart.type, config.chartName).then(dataList => {
                config.series.push(dataList[config.chartName]);
                config.xAxis.categories = dataList[config.chartName].name;
                this.charts.push(config);
            })
        });
        this.tab.id = 'line_chart';
        this.tab.heading = 'Static title';
        this.tabs.push(this.tab);
    }

}

class Tab {
    id : string;
    heading : string;
}
