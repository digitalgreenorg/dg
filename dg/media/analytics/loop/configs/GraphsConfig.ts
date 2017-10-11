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
    drilldown: {}
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
    series: []
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
    }
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
    }
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
    }
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
    }
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
    }
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
    }
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
    }
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
    }
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
    }
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
    xAxis: { type: 'category', max: 5 },
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
    credits: { enabled: false },
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: [],
      drillUpButton: drillUpButton
    }
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
    series: []
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
