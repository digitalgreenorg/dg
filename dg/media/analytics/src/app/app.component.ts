import { Component, OnInit } from '@angular/core';
import { Data } from './data'
import { GraphsService } from './graphs.service'

declare let d3:any;

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers: [GraphsService]
})

export class AppComponent implements OnInit {
  title = 'Graphs';
  options;
  data: Data[]
  constructor(private graphService: GraphsService) { }
  getData(): void {
    this.graphService.getDatas().then(datas => this.data = datas)
  }
  ngOnInit(): void{
        this.options = {
          chart: {
            type: 'discreteBarChart',
            height: 450,
            margin : {
              top: 20,
              right: 20,
              bottom: 50,
              left: 55
            },
            x: (d) => {return d.label;},
            y: (d) => {return d.value;},
            showValues: true,
            valueFormat: function(d){
              return d3.format(',.4f')(d);
            },
            duration: 500,
            xAxis: {
              axisLabel: 'X Axis'
            },
            yAxis: {
              axisLabel: 'Y Axis',
              axisLabelDistance: -10
            }
        }
      } 
      this.getData();
  }
}
