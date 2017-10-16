import { Component, OnInit, AfterViewInit } from '@angular/core';
import { GraphsService } from './graphs.service';
import { SharedService } from '../shared.service';
import { environment } from '../../environments/environment.training';

@Component({
  selector: 'graphs',
  templateUrl: './graphs.component.html',
  styleUrls: ['./graphs.component.css'],
})

export class GraphsComponent implements OnInit, AfterViewInit {
  tabs = [];
  charts = [];
  tabsConfig = environment.tabsConfig;
  chartsConfig = environment.chartsConfig;

  constructor(private graphService: GraphsService, private _sharedService: SharedService) {
    this._sharedService.argsList$.subscribe(filters => {
      this.getGraphsData(filters);
    });
    setInterval(() => {
      this.charts.forEach(chart => {
        chart.nativeChart.reflow();
      });
    }, 0);

  }

  ngOnInit(): void {
    //Generate tabs dynamically
    Object.keys(this.tabsConfig).forEach(tab => {
      this.tabsConfig[tab].id = tab;
      this.tabs.push(this.tabsConfig[tab]);
    });

    Object.keys(this.chartsConfig).forEach(config => {
      //Add divs to tabs
      Object.keys(this.tabsConfig).forEach(tab => {
        if (this.chartsConfig[config].chart.tab.id === this.tabsConfig[tab].id) {
          //Set div attributes
          this.tabsConfig[tab].showDivs.push({
            'id': this.chartsConfig[config].chart.renderTo,
            'class': this.chartsConfig[config].chart.tab.class
          });
        }
      })
      //assign key as chart name
      this.chartsConfig[config].chartName = config;
      //Add empty charts to DOM
      this.charts.push({
        options: this.chartsConfig[config],
        nativeChart: null // To be obtained with saveInstance
      });
    });
  }

  //function to access underlying chart
  saveInstance(chartInstance, chart) {
    chart.nativeChart = chartInstance;
  }

  ngAfterViewInit(): void {
    this.getGraphsData({ 'params': {} });
  }

  private getGraphsData(filters): void {
    this.charts.forEach(chart => {
      chart.nativeChart.showLoading();
      try {
        chart.nativeChart.drillUp();
      } catch (e) { }
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
          chart.nativeChart.redraw();
        });
      });
    });
  }

  //Empty exting data and then fill in updated data
  private clearSeriesFromGraph(chart) {
    if (chart.nativeChart.series.length > 0) {
      for (var i = chart.nativeChart.series.length - 1; i >= 0; i--) {
        chart.nativeChart.series[i].remove(false);
      }
    }
  }
}
