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
    charts = [];
    ngOnInit(): void{
        for(let json of configs) {
            this.charts.push(json);
        }
        console.log(this.charts);
    }
}
