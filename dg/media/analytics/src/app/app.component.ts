import { Component, OnInit, Pipe } from '@angular/core';
import { configs } from './configs';
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

export class AppComponent implements OnInit{
    title = 'Graphs';
    charts = [];
    constructor(private graphService: GraphsService){}
    
    ngOnInit(): void{

        configs.forEach(config => {
            this.graphService.getData(config.chart.type, config.placeholder).then(dataList => {
                config.series.push(dataList[config.placeholder]);
                config.xAxis.categories = dataList[config.placeholder].name;
                this.charts.push(config);
            })
        });
        console.log(this.charts);
    }
}
