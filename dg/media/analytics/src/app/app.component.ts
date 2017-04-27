import { Component, OnInit } from '@angular/core';
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
        
        for(let json of configs) {
            this.graphService.getData().then(dataList => {
                for(let data of dataList){
                    json.series.push(data);
                    json.xAxis.categories = data.categories;
                }
                console.log(json);
                this.charts.push(json)
            });    
        }
    }
}
