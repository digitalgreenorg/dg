import { Component,OnInit, AfterViewInit } from '@angular/core';
import { GraphsService } from './graphs.service';
import { SharedService } from '../shared.service';
import { environment } from '../../environments/environment.training';

@Component({
  selector: 'graphs',
  templateUrl: './graphs.component.html',
  styleUrls: ['./graphs.component.css'],
})

export class GraphsComponent implements OnInit, AfterViewInit{
    tabs = [];
    charts = [];

  constructor(private graphService: GraphsService, private _sharedService: SharedService) {
    this._sharedService.argsList$.subscribe(filters => {
      this.getGraphsData(filters);
    });
  }

  ngOnInit(): void {
    //Generate tabs dynamically
    environment.tabsConfig.forEach(tab => {
      this.tabs.push(tab);
    });
    environment.chartsConfig.forEach(config => {
      //Add divs to tabs
      environment.tabsConfig.forEach(tab => {
        if (config.chart.tab.id === tab.id) {
          tab.showDivs.push({
            'id': config.chart.renderTo,
            'class': config.chart.tab.class
          });
        }
      })
      //Add empty charts to DOM
      this.charts.push({
        options: config,
        nativeChart: null // To be obtained with saveInstance
      });
    });
  }

  saveInstance(chartInstance, chart) {
    chart.nativeChart = chartInstance;
  }

  ngAfterViewInit(): void {
    this.getGraphsData({ 'params': {} });
  }

  private getGraphsData(filters): void {
    this.charts.forEach(chart => {
      chart.nativeChart.showLoading();
      filters.params['chartType'] = chart.options.chart.type;
      filters.params['chartName'] = chart.options.chartName;
      this.graphService.getData(filters).subscribe(dataList => {
        Object.keys(dataList).forEach(key => {
          //Find already displayed cart to enter data
          if (key === chart.options.chartName) {
            chart.nativeChart.hideLoading();
            this.clearSeriesFromGraph(chart);
            dataList[key]['outerData']['series'].forEach(entry => {
              chart.nativeChart.addSeries(entry);
            });
            if (chart.options.chart.drillDown) {
              dataList[key]['innerData'].forEach(drilldownEntry => {
                chart.options.drilldown.series.push(drilldownEntry);
              });
            }
          }
          else {
            this.clearSeriesFromGraph(chart);
            chart.nativeChart.showLoading(dataList['error']);
          }
        });
      });
    });

  }

  private clearSeriesFromGraph(chart) {
    if (chart.nativeChart.series.length > 0) {
      for (var i = chart.nativeChart.series.length - 1; i >= 0; i--) {
        chart.nativeChart.series[i].remove();
      }
    }
  }
}
