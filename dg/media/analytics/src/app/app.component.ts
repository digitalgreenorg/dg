import { Component, OnInit } from '@angular/core';
import { Bar } from './model';
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
    bar_charts = [];
    ngOnInit(): void{
        let json_data = ['{"title" : {"text" : "simple chart"},"series": [{"data": [29.9, 71.5, 106.4, 129.2]}]}','{"title" : {"text" : "simple chart"},"series": [{"data": [29.9, 71.5, 106.4, 129.2]}]}'];
        for(let json of json_data) {
            let bar_one : Bar = Object.assign(new Bar, JSON.parse(json));
            this.bar_charts.push(bar_one);
            console.log("########################");
            console.log(bar_one);
        }
        console.log(this.bar_charts);
    }
}
