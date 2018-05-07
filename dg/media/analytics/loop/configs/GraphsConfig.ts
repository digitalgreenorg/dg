import { commonOptions } from './CommonHighchartsOptions';
const tooltip = {
  headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
  pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b><br/>'
};

const drillUpButton = {
  relativeTo: 'spacingBox',
  position: {
    y: -12,
    x: 0
  }
};
const legend_weighted_total = {
  enabled: true,
  labelFormatter: function() {
    var total = 0;
    var total_volume = 0;
    for (var i = this.yData.length; i--;) {
      let volume = this.userOptions.data[i].volume;
      total += this.yData[i] * volume;
      total_volume += volume;
    };
    if (total_volume) {
      return this.name + ' - Avg :  ' + (total / total_volume).toFixed(2);
    }
    else {
      return this.name;
    }
  },
};

const legend_total = {
  enabled: true,
  labelFormatter: function() {
    var total = 0;
    for (var i = this.yData.length; i--;) { total += this.yData[i]; };
    return this.name + ' - Total :  ' + total.toFixed(0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }
};

const legend_enable = {
  enabled: true,
}

export const chartsConfig = {
  'cummulativeCount': {
    chart: {
      type: 'spline',
      renderTo: 'cummulativeCount',
      tab: {
        'class': 'col'
      },
    },
    type: "StockChart",
    rangeSelector: {
      selected: 5
    },
    yAxis: [{ // Primary yAxis
      title: {
        text: 'Volume',
      },
      opposite: false
    }, { // Secondary yAxis
      title: {
        text: 'Farmer',
      }
    }],
    tooltip: {
      // shared: true,
      pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b><br/>',
      valueDecimals: 0
    },
    series: [],
    drilldown: {},
    legend: legend_enable
  },
  'volFarmerTS': {
    chart: {
      type: "areaspline",
      renderTo: 'volFarmerTS',
      drilldown: false,
      tab: {
        'class': 'col'
      },
    },
    rangeSelector: {
      selected: 0
    },
    type: "StockChart",
    yAxis: [{ // Primary yAxis
      title: {
        text: 'Volume',
      },
      opposite: false
    }, { // Secondary yAxis
      title: {
        text: 'Farmers',
      }
    }],
    tooltip: {
      pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b><br/>',
      valueDecimals: 2,
      // split: true
    },
    series: [],
    // drilldown: {}
    legend: legend_enable
  },
  'cpkSpkTS': {
    chart: {
      type: "areaspline",
      renderTo: 'cpkSpkTS',
      drilldown: false,
      tab: {
        'class': 'col'
      },
    },
    rangeSelector: {
      selected: 0
    },
    type: "StockChart",
    yAxis: { // Primary yAxis
      title: {
        text: 'CPK / SPK',
      }
    },
    tooltip: {
      shared: true,
      valueDecimals: 2,
      // valueSuffix: ' units'
    },
    series: [],
    legend: legend_enable
  },
  'aggrvol': {
    chart: {
      type: 'column',
      renderTo: 'aggrvol',
      tab: {
        'id': 'tab1',
        'class': 'col'
      },
      drillDown: true,
      inverted: true,
    },
    xAxis: {
      type: 'category', max: 5
    },
    yAxis: {
      title: { text: '' },
      labels: {
        enabled: false
      },
    },
    tooltip: tooltip,
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: [],
      drillUpButton: drillUpButton
    },
    legend: legend_total,
  },
  'aggramt': {
    chart: {
      type: 'column',
      renderTo: 'aggramt',
      tab: {
        'id': 'tab1',
        'class': 'col'
      },
      drillDown: true,
      inverted: true,
    },
    xAxis: { type: 'category', max: 5 },
    yAxis: {
      title: { text: '' },
      labels: {
        enabled: false
      },
    },
    tooltip: tooltip,
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: [],
      drillUpButton: drillUpButton
    },
    legend: legend_total
  },
  'aggrvisit': {
    chart: {
      type: 'column',
      renderTo: 'aggrvisit',
      tab: {
        'id': 'tab1',
        'class': 'col'
      },
      drillDown: true,
      inverted: true,
    },
    xAxis: { type: 'category', max: 5 },
    yAxis: {
      title: { text: '' },
      labels: {
        enabled: false
      },
    },
    tooltip: tooltip,
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: [],
      drillUpButton: drillUpButton
    },
    legend: legend_total
  },
  'aggrspkcpk': {
    chart: {
      type: 'column',
      renderTo: 'aggrspkcpk',
      tab: {
        'id': 'tab1',
        'class': 'col'
      },
      drillDown: true,
      inverted: true,
    },
    xAxis: {
      type: 'category',
      max: 5
    },
    yAxis: {
      title: { text: '' },
      labels: {
        enabled: false
      },
    },
    tooltip: tooltip,
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: [],
      drillUpButton: drillUpButton
    },
    legend: legend_weighted_total,
  },
  'aggrrecoveredtotal': {
    chart: {
      type: 'column',
      renderTo: 'aggrrecoveredtotal',
      tab: {
        'id': 'tab1',
        'class': 'col'
      },
      drillDown: true,
      inverted: true,
    },
    xAxis: { type: 'category', max: 5 },
    yAxis: {
      title: { text: '' },
      labels: {
        enabled: false
      },
    },
    tooltip: tooltip,
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: [],
      drillUpButton: drillUpButton
    },
    legend: legend_total,
  },
  'aggrfarmercount': {
    chart: {
      type: 'column',
      renderTo: 'aggrfarmercount',
      tab: {
        'id': 'tab1',
        'class': 'col'
      },
      drillDown: true,
      inverted: true,
    },
    xAxis: { type: 'category', max: 5 },
    yAxis: {
      title: { text: '' },
      labels: {
        enabled: false
      },
    },
    tooltip: tooltip,
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: [],
      drillUpButton: drillUpButton
    }, legend: legend_total,
  },
  'mandivolume': {
    chart: {
      type: 'column',
      renderTo: 'mandivolume',
      tab: {
        'id': 'tab1',
        'class': 'col'
      },
      drillDown: true,
      inverted: true,
    },
    xAxis: { type: 'category', max: 5 },
    yAxis: {
      title: { text: '' },
      labels: {
        enabled: false
      },
    },
    tooltip: tooltip,
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: [],
      drillUpButton: drillUpButton
    },
    legend: legend_total,
  },
  'mandivisit': {
    chart: {
      type: 'column',
      renderTo: 'mandivisit',
      tab: {
        'id': 'tab1',
        'class': 'col'
      },
      drillDown: true,
      inverted: true,
    },
    xAxis: { type: 'category', max: 5 },
    yAxis: {
      // tickInterval: 1,
      title: { text: '' },
      labels: {
        enabled: false
      },
    },
    tooltip: tooltip,
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: [],
      drillUpButton: drillUpButton
    },
    legend: legend_total,
  },
  'mandispkcpk': {
    chart: {
      type: 'column',
      renderTo: 'mandispkcpk',
      tab: {
        'id': 'tab1',
        'class': 'col'
      },
      drillDown: true,
      inverted: true,
    },
    xAxis: {
      type: 'category',
      max: 5
    },
    yAxis: {
      // tickInterval: 1,
      title: { text: '' },
      labels: {
        enabled: false
      },
    },
    tooltip: tooltip,
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: [],
      drillUpButton: drillUpButton
    },
    legend: legend_weighted_total
  },
  'mandirecoveredtotal': {
    chart: {
      type: 'column',
      renderTo: 'mandirecoveredtotal',
      tab: {
        'id': 'tab1',
        'class': 'col'
      },
      drillDown: true,
      inverted: true,
    },
    xAxis: {
      type: 'category',
      max: 5
    },
    yAxis: {
      // tickInterval: 1000,
      title: { text: '' },
      labels: {
        enabled: false
      },
    },
    tooltip: tooltip,
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: [],
      drillUpButton: drillUpButton
    },
    legend: legend_total
  },
  'mandifarmercount': {
    chart: {
      type: 'column',
      renderTo: 'mandifarmercount',
      tab: {
        'id': 'tab1',
        'class': 'col-sm-12'
      },
      drillDown: true,
      inverted: true,
    },
    xAxis: { type: 'category', max: 5 },
    yAxis: {
      // tickInterval: 10,
      title: { text: '' },
      labels: {
        enabled: false
      },
    },
    tooltip: tooltip,
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: [],
      drillUpButton: drillUpButton
    },
    legend: legend_total
  },
  'cropvolume': {
    chart: {
      type: 'column',
      renderTo: 'cropvolume',
      tab: {
        'id': 'tab1',
        'class': 'col'
      },
      drillDown: true,
      inverted: true,
    },
    xAxis: {
      type: 'category', max: 5,
    },
    yAxis: {
      // tickInterval: 1000,
      title: { text: '' },
      labels: {
        enabled: false
      },
    },
    tooltip: tooltip,
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: [],
      drillUpButton: drillUpButton
    },
    legend: legend_total
  },
  'cropprices': {
    chart: {
      type: 'columnrange',
      renderTo: 'cropprices',
      tab: {
        'id': 'tab1',
        'class': 'col'
      },
      drillDown: true,
      inverted: true,
    },
    xAxis: {
      type: 'category',
      max: 5
    },
    yAxis: {
      // tickInterval: 10,
      title: { text: '' },
      labels: {
        enabled: false
      },
    },
    tooltip: tooltip,
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: [],
      drillUpButton: drillUpButton
    },
    legend: legend_enable
  },
  'cropfarmercount': {
    chart: {
      type: 'column',
      renderTo: 'cropfarmercount',
      tab: {
        'id': 'tab1',
        'class': 'col'
      },
      drillDown: false,
      inverted: true,
    },
    xAxis: { type: 'category', max: 5 },
    yAxis: {
      // tickInterval: 10,
      title: { text: '' },
      labels: {
        enabled: false
      },
    },
    tooltip: tooltip,
    series: [],
    legend: legend_enable
  },
  'crop_price_range_ts': {
    chart: {
      type: "candlestick",
      renderTo: 'crop_price_range_ts',
      drilldown: false,
      dropdown: true,
      tab: {
        'class': 'col'
      },
    },
    rangeSelector: {
      selected: 0
    },
    type: "StockChart",
    yAxis: [{ // Primary yAxis
      title: {
        text: 'Crop prices',
      }
    }],
    tooltip: {
      // pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b><br/>',
      valueDecimals: 2,
    },
    series: [],
    exporting: {
      buttons: {
        contextButton: {
          enabled: false,
        },
        toggle: {
          align: 'center',
          text: 'Select Crop',
          menuItems: []
        }
      }
    },
    navigation: {
      buttonOptions: {
        theme: {
          'stroke-width': 1,
          stroke: '#656566',
          padding: 8,
          r: 0,
          states: {
            hover: {
              fill: '#F37B55'
            },
          }
        }
      }
    }
  },
}

export class AddCommonOptions {
  public AddCommonOptionsToGraph(): void {
    Object.keys(chartsConfig).forEach(key => {
      Object.assign(chartsConfig[key], commonOptions);
    });
  }
}
