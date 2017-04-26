import { Component, OnInit } from '@angular/core';
import { Bar } from './model';
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
    bar_charts = [];
    ngOnInit(): void{
        for(let json of configs) {
            //console.log(typeof(JSON.stringify(json)));
            let bar_one : Bar = Object.assign(new Bar, JSON.parse(JSON.stringify(json)));
            this.bar_charts.push(bar_one);
            console.log(bar_one);
        }
        console.log(configs.length);
    }
}
