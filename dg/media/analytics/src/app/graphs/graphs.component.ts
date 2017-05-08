import { Component, OnInit, Pipe } from '@angular/core';
import { configs } from './configs';
import { GraphsService } from './graphs.service';
import { ChartModule } from 'angular2-highcharts';
import { HighchartsStatic } from 'angular2-highcharts/dist/HighchartsService';

@Component({
    selector: 'graphs',
    templateUrl: './graphs.component.html',
    styleUrls: ['./graphs.component.css'],
    providers: [GraphsService]
})

export class GraphsComponent implements OnInit{
    charts = [];
    constructor(private graphService: GraphsService){}
    
    ngOnInit(): void{

        configs.forEach(config => {
            console.log("hi");
            this.graphService.getData(config.chart.type, config.placeholder).then(dataList => {
                config.series.push(dataList[config.placeholder]);
                config.xAxis.categories = dataList[config.placeholder].name;
                this.charts.push(config);
            })
        });
    }
}

