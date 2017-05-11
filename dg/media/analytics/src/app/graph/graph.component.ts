import { Component, OnInit } from '@angular/core';
import * as d3 from "d3"

@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.css']
})
export class GraphComponent implements OnInit {

  constructor() { }
  options: any;
  data: any;

  ngOnInit() {
    this.options = {
      chart: {
        type: 'discreteBarChart',
        height: 450,
        x: function (d) {
             return d.label; 
            },
        y: function (d) {
             return d.value; 
            }
      }
    }

    this.data = [
      {
        key: 'Cumulative Return',
        values: [
          { 'label': 'A', 'value': 10 },
          { 'label': 'B', 'value': 20 }
        ]
      }
    ];
  }

}
