import { Component } from '@angular/core';
import { chartsConfig } from './configs';
import { tabsConfig } from './configs_tab';
import { GraphsService } from './graphs.service';
import { SharedService } from '../shared.service';

@Component({
  selector: 'graphs',
  templateUrl: './graphs.component.html',
  styleUrls: ['./graphs.component.css'],
  // providers: [GraphsService]
})

export class GraphsComponent {
  tabs = [];
  charts = [];

  constructor(private graphService: GraphsService, private _sharedService: SharedService) {
    this._sharedService.argsList$.subscribe(filters => {
      this.getGraphsData(filters);
    });
  }

  ngOnInit(): void {
    //Generate tabs dynamically
    tabsConfig.forEach(tab => {
      this.tabs.push(tab);
    });
    chartsConfig.forEach(config => {
      //Add divs to tabs
      tabsConfig.forEach(tab => {
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
            if (chart.nativeChart.series.length > 0) {
              for (var i = chart.nativeChart.series.length - 1; i >= 0; i--) {
                chart.nativeChart.series[i].remove();
              }
            }
            dataList[key]['outerData']['series'].forEach(entry => {
              chart.nativeChart.addSeries(entry);
            });
            if (chart.options.chart.drillDown == true) {
              dataList[key]['innerData'].forEach(drilldownEntry => {
                chart.options.drilldown.series.push(drilldownEntry);
              });
            }
          }
        });
      });
    });

  }
}
