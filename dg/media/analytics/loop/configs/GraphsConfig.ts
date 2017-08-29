const colors = [
  '#F37B55',
  '#656566',
];

const tooltip = {
  headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
  pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b><br/>'
};

export const chartsConfig = {
  'cummulativeCount': {
    chart: {
      type: 'spline',
      renderTo: 'cummulativeCount',
      tab: {
        'class': 'col'
      },
      // width:500,
      // height: 230,
    },
    type: "StockChart",
    rangeSelector: {
      selected: 2
    },
    credits: { enabled: false },
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
    legend: { enabled: false },
    tooltip: {
      // shared: true,
      pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b><br/>',
      valueDecimals: 2
    },
    colors: colors,
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
    title: {
      text: 'Volume Amount'
    },
    yAxis: [{ // Primary yAxis
      title: {
        text: 'Volume',
      },
      opposite: false
    }, { // Secondary yAxis
      title: {
        text: 'Amount',
      }
    }],
    legend: { enabled: false },
    tooltip: {
      pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b><br/>',
      valueDecimals: 2,
      // split: true
    },
    credits: {
      enabled: false
    },
    plotOptions: {
      areaspline: {
        fillOpacity: 0.3
      }
    },
    colors: colors,
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
    title: {
      text: 'CPK SPK'
    },
    yAxis: [{ // Primary yAxis
      title: {
        text: 'CPK',
      },
      opposite: false
    }, { // Secondary yAxis
      title: {
        text: 'SPK',
      }
    }],
    legend: { enabled: false },
    tooltip: {
      shared: true,
      valueDecimals: 2,
      // valueSuffix: ' units'
    },
    credits: {
      enabled: false
    },
    plotOptions: {
      areaspline: {
        fillOpacity: 0.3
      }
    },
    colors: colors,
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
      // width: 530,
      // height: 230,

    },
    credits: { enabled: false },
    title: { text: '' },
    xAxis: { type: 'category', max: 5 },
    yAxis: {
      tickInterval: 10000,
      title: { text: 'Volume' }
    },
    scrollbar: {
      enabled: true
    },
    legend: { enabled: false },
    plotOptions: {
      column: {
        dataLabels: {
          enabled: true
        }
      }
    },
    colors: colors,
    tooltip: tooltip,
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: []
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
      // width: 530,
      // height: 230,
    },
    credits: { enabled: false },
    title: { text: '' },
    xAxis: { type: 'category', max: 5 },
    yAxis: {
      tickInterval: 1,
      title: { text: 'Visits' }
    },
    scrollbar: { enabled: true },
    legend: { enabled: false },
    plotOptions: {
      column: {
        grouping: false,
        borderWidth: 0,
        dataLabels: {
          enabled: true
        }
      }
    },
    colors: colors,
    tooltip: tooltip,
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: []
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
      // width: 530,
      // height: 230,
    },
    credits: { enabled: false },
    title: { text: '' },
    xAxis: {
      type: 'category',
      max: 5
    },
    yAxis: {
      tickInterval: 1,
      title: { text: 'SPK CPK' }
    },
    scrollbar: { enabled: true },
    legend: { enabled: false },
    plotOptions: {
      column: {
        grouping: false,
        borderWidth: 0,
        dataLabels: {
          enabled: true
        }
      }
    },
    colors: colors,
    tooltip: tooltip,
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: []
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
      // width: 530,
      // height: 230,
    },
    credits: { enabled: false },
    title: { text: '' },
    xAxis: { type: 'category', max: 5 },
    yAxis: {
      tickInterval: 1000,
      title: { text: 'Recovered / Total Cost' }
    },
    scrollbar: {
      enabled: true
    },
    legend: { enabled: false },
    plotOptions: {
      column: {
        grouping: false,
        borderWidth: 0,
        dataLabels: {
          enabled: true
        }
      }
    },
    colors: colors,
    tooltip: tooltip,
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: []
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
      // width: 530,
      // height: 230,
    },
    credits: { enabled: false },
    title: { text: '' },
    xAxis: { type: 'category', max: 5 },
    yAxis: {
      tickInterval: 10,
      title: { text: 'Farmer count' }
    },
    legend: { enabled: false },
    plotOptions: {
      column: {
        grouping: false,
        borderWidth: 0,
        dataLabels: {
          enabled: true
        }
      }
    },
    colors: colors,
    scrollbar: { enabled: true },
    tooltip: tooltip,
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: []
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
      // width: 530,
      // height: 230,
    },
    credits: { enabled: false },
    title: { text: '' },
    xAxis: { type: 'category', max: 5 },
    yAxis: {
      tickInterval: 1000,
      title: { text: 'Volume' }
    },
    scrollbar: { enabled: true },
    legend: { enabled: false },
    plotOptions: {
      column: {
        grouping: false,
        borderWidth: 0,
        dataLabels: {
          enabled: true
        }
      }
    },
    colors: colors,
    tooltip: tooltip,
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: []
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
      // width: 530,
      // height: 230,
    },
    credits: { enabled: false },
    title: { text: '' },
    xAxis: { type: 'category', max: 5 },
    yAxis: {
      tickInterval: 1,
      title: { text: 'Visits' }
    },
    scrollbar: { enabled: true },
    legend: { enabled: false },
    plotOptions: {
      column: {
        grouping: false,
        borderWidth: 0,
        dataLabels: {
          enabled: true
        }
      }
    },
    colors: colors,
    tooltip: tooltip,
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: []
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
      // width: 530,
      // height: 230,
    },
    credits: { enabled: false },
    title: { text: '' },
    xAxis: {
      type: 'category',
      max: 5
    },
    yAxis: {
      tickInterval: 1,
      title: { text: 'SPK CPK' }
    },
    scrollbar: { enabled: true },
    legend: { enabled: false },
    plotOptions: {
      column: {
        grouping: false,
        borderWidth: 0,
        dataLabels: {
          enabled: true
        }
      }
    },
    colors: colors,
    tooltip: tooltip,
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: []
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
      // width: 530,
      // height: 230,
    },
    credits: { enabled: false },
    title: { text: '' },
    xAxis: {
      type: 'category',
      max: 5
    },
    yAxis: {
      tickInterval: 1000,
      title: { text: 'Recovered / Total cost' }
    },
    scrollbar: { enabled: true },
    legend: { enabled: false },
    plotOptions: {
      column: {
        grouping: false,
        borderWidth: 0,
        dataLabels: {
          enabled: true
        }
      }
    },
    colors: colors,
    tooltip: tooltip,
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: []
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
      // width: 530,
      // height: 230,
    },
    credits: { enabled: false },
    title: { text: '' },
    xAxis: { type: 'category', max: 5 },
    yAxis: {
      tickInterval: 10,
      title: { text: 'Farmer count' }
    },
    scrollbar: { enabled: true },
    legend: { enabled: false },
    plotOptions: {
      column: {
        grouping: false,
        borderWidth: 0,
        dataLabels: {
          enabled: true
        }
      }
    },
    colors: colors,
    tooltip: tooltip,
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: []
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
      // width: 530,
      // height: 230,
    },
    credits: { enabled: false },
    title: { text: '' },
    xAxis: { type: 'category', max: 5 },
    yAxis: {
      tickInterval: 1000,
      title: { text: 'Volume' }
    },
    scrollbar: { enabled: true },
    legend: { enabled: false },
    plotOptions: {
      column: {
        grouping: false,
        borderWidth: 0,
        dataLabels: {
          enabled: true
        }
      }
    },
    colors: colors,
    tooltip: tooltip,
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: []
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
      // width: 530,
      // height: 230,
    },
    scrollbar: { enabled: true },
    title: { text: '' },
    xAxis: {
      type: 'category',
      max: 5
    },
    yAxis: {
      tickInterval: 10,
      title: { text: 'Price range' }
    },
    legend: {
      enabled: false
    },
    plotOptions: {
      columnrange: {
        grouping: false,
        borderWidth: 0,
        dataLabels: {
          enabled: true
        }
      }
    },
    colors: colors,
    tooltip: tooltip,
    credits: { enabled: false },
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: []
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
      // width: 530,
      // height: 230,
    },
    credits: { enabled: false },
    title: { text: '' },
    xAxis: { type: 'category', max: 5 },
    yAxis: {
      tickInterval: 10,
      title: { text: 'Farmer count' }
    },
    scrollbar: { enabled: true },
    legend: { enabled: false },
    plotOptions: {
      column: {
        grouping: false,
        borderWidth: 0,
        dataLabels: {
          enabled: true
        }
      }
    },
    colors: colors,
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
        'class': 'col-sm-11'
      },
    },
    rangeSelector: {
      selected: 0
    },
    type: "StockChart",
    title: {
      text: 'Crop Price Range'
    },
    yAxis: [{ // Primary yAxis
      title: {
        text: 'Crop prices',
      }
    }],
    legend: { enabled: false },
    tooltip: {
      // pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b><br/>',
      valueDecimals: 2,
    },
    credits: {
      enabled: false
    },
    colors: [
      '#F37B55',
      '#656566',
    ],
    series: [],
    exporting: {
      buttons: {
        contextButton: {
          enabled: false,
          symbolStrokeWidth: 2
        },
        toggle: {
          text: 'Select Crop',
          menuItems: [
          //   {
          //   text: '0-5',
          //   onclick: function() {
          //     this.xAxis[0].setExtremes(0, 5);
          //   }
          // }, {
          //   text: '5-10',
          //   onclick: function() {
          //     this.xAxis[0].setExtremes(5, 10);
          //   }
          // }
        ]
        }
      }
    },
  },
}
