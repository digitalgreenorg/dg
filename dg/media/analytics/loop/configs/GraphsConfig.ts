export const chartsConfig = {
  'cummulativeCount': {
    chart: {
      type: 'spline',
      renderTo: 'cummulativeCount',
      tab: {
        'class': 'col-sm-12'
      },
    },
    type: "StockChart",
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
      shared: true,
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
        'class': 'col-sm-6'
      },
    },
    rangeSelector: {
      selected: 0
    },
    type: "StockChart",
    title: {
      text: 'Volume Amount'
    },
    legend: { enabled: false },
    // tooltip: {
    //   shared: true,
    //   valueDecimals: 2,
    //   // valueSuffix: ' units'
    // },
    tooltip: {
      pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',
      valueDecimals: 2,
      split: true
    },
    credits: {
      enabled: false
    },
    plotOptions: {
      areaspline: {
        fillOpacity: 0.5
      }
    },
    series: [],
    drilldown: {}
  },
  'cpkSpkTS': {
    chart: {
      type: "areaspline",
      renderTo: 'cpkSpkTS',
      drilldown: false,
      tab: {
        'class': 'col-sm-6'
      },
    },
    rangeSelector: {
      selected: 0
    },
    type: "StockChart",
    title: {
      text: 'CPK SPK'
    },
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
        fillOpacity: 0.5
      }
    },
    series: [],
    drilldown: {}
  },
  'aggrvol': {
    chart: {
      type: 'column',
      renderTo: 'aggrvol',
      tab: {
        'id': 'tab1',
        'class': 'col-sm-6'
      },
      drillDown: true,
      inverted: true
    },
    credits: { enabled: false },
    title: { text: '' },
    xAxis: { type: 'category' },
    yAxis: {
      // tickInterval: 10,
      title: { text: 'Volume' }
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
    tooltip: {
      headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
      pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of total<br/>'
    },
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      drillUpButton: {
        relativeTo: 'spacingBox',
        position: {
          y: 0,
          x: -30
        },
      },
      series: []
    },
    lang: {
      drillUpText: '<< Back'
    },
  },
  'aggrvisit': {
    chart: {
      type: 'column',
      renderTo: 'aggrvisit',
      tab: {
        'id': 'tab1',
        'class': 'col-sm-6'
      },
      drillDown: true,
      inverted : true,
    },
    credits: { enabled: false },
    title: { text: '' },
    xAxis: { type: 'category', max:5 },
    yAxis: {
      tickInterval: 10,
      title: { text: 'Visits' }
    },
    scrollbar : {enabled:true},
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
    tooltip: {
      headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
      pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of total<br/>'
    },
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
        'class': 'col-sm-6'
      },
      drillDown: true,
      inverted : true,
    },
    credits: { enabled: false },
    title: { text: '' },
    xAxis: { type: 'category', max:5 },
    yAxis: {
      tickInterval: 10,
      title: { text: 'Volume' }
    },
    scrollbar : {enabled:true},
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
    tooltip: {
      headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
      pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of total<br/>'
    },
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      drillUpButton: {
        relativeTo: 'spacingBox',
        position: {
          y: 0,
          x: -30
        },
      },
      series: []
    },
    lang: {
      drillUpText: '<< Back'
    },
  },
  'mandivisit': {
    chart: {
      type: 'column',
      renderTo: 'mandivisit',
      tab: {
        'id': 'tab1',
        'class': 'col-sm-6'
      },
      drillDown: true,
      inverted : true,
    },
    credits: { enabled: false },
    title: { text: '' },
    xAxis: { type: 'category', max:5 },
    yAxis: {
      tickInterval: 10,
      title: { text: 'Visits' }
    },
    scrollbar : {enabled:true},
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
    tooltip: {
      headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
      pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of total<br/>'
    },
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: []
    }
  },
  'cropvolume':{
    chart: {
      type: 'column',
      renderTo: 'cropvolume',
      tab: {
        'id': 'tab1',
        'class': 'col-sm-6'
      },
      drillDown: true,
      inverted : true,
    },
    credits: { enabled: false },
    title: { text: '' },
    xAxis: { type: 'category', max:5 },
    yAxis: {
      tickInterval: 10,
      title: { text: 'Volume' }
    },
    scrollbar : {enabled:true},
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
    tooltip: {
      headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
      pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of total<br/>'
    },
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      drillUpButton: {
        relativeTo: 'spacingBox',
        position: {
          y: 0,
          x: -30
        },
      },
      series: []
    },
    lang: {
      drillUpText: '<< Back'
    },
  },
  'cropfarmercount': {
    chart: {
      type: 'column',
      renderTo: 'cropfarmercount',
      tab: {
        'id': 'tab1',
        'class': 'col-sm-6'
      },
      drillDown: true,
      inverted : true,
    },
    credits: { enabled: false },
    title: { text: '' },
    xAxis: { type: 'category', max:5 },
    yAxis: {
      tickInterval: 10,
      title: { text: 'Volume' }
    },
    scrollbar : {enabled:true},
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
    tooltip: {
      headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
      pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of total<br/>'
    },
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      drillUpButton: {
        relativeTo: 'spacingBox',
        position: {
          y: 0,
          x: -30
        },
      },
      series: []
    },
    lang: {
      drillUpText: '<< Back'
    },
  },
  'cropprices':{
    chart: {
      type: 'columnrange',
      renderTo: 'cropprices',
      tab: {
        'id': 'tab1',
        'class': 'col-sm-6'
      },
      drillDown: true,
      inverted: true
    },
    scrollbar : {enabled:true},
    xAxis: { type: 'category', max:5 },
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
    tooltip: {
      headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
      pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of total<br/>'
    },
    credits: { enabled: false },
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: []
    }
  },
  'aggrfarmercount' : {
                          chart: {
                                  type: 'column',
                                  renderTo: 'aggrfarmercount',
                                  tab: {
                                        'id': 'tab1',
                                        'class':'col-sm-12'
                                  },
                                  drillDown: true,
                                  inverted: true
                          },
                          credits:{ enabled: false },
                          title: { text: ''},
                          xAxis: { type: 'category', max:5 },
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
                          scrollbar:{enabled:true},
                          tooltip: {
                                    headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                                    pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of total<br/>'
                          },
                          series: [],
                          drilldown: {
                            allowPointDrilldown: false,
                            series: []
                          }
  },
  /*
  'aggrspkcpk' : {
                          chart: {
                                  type: 'column',
                                  renderTo: 'aggrspkcpk',
                                  tab: {
                                        'id': 'tab1',
                                        'class':'col-sm-12'
                                  },
                                  drillDown: true
                          },
                          credits:{ enabled: false },
                          title: { text: ''},
                          xAxis: { type: 'category' },
                          yAxis: {
                                  tickInterval: 10,
                                  title: { text: 'Volume' } },
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
                          tooltip: {
                                    headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                                    pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of total<br/>'
                          },
                          series: [],
                          drilldown: {}
  },
  'aggrrecoveredtotal': {
    chart: {
      type: 'column',
      renderTo: 'aggrrecoveredtotal',
      tab: {
        'id': 'tab1',
        'class': 'col-sm-6'
      },
      drillDown: true,
      inverted: true
    },
    credits: { enabled: false },
    title: { text: '' },
    xAxis: { type: 'category', max: 5 },
    yAxis: {
      // tickInterval: 10,
      title: { text: '' }
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
    tooltip: {
      headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
      pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of total<br/>',
    },
    series: [],
    drilldown: {
      allowPointDrilldown: false,
      series: []
    }
  },
  /*
  'aggrfarmercount' : {
                          chart: {
                                  type: 'column',
                                  renderTo: 'aggrfarmercount',
                                  tab: {
                                        'id': 'tab1',
                                        'class':'col-sm-12'
                                  },
                                  drillDown: true
                          },
                          credits:{ enabled: false },
                          title: { text: ''},
                          xAxis: { type: 'category' },
                          yAxis: {
                                  tickInterval: 10,
                                  title: { text: 'Volume' } },
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
                          tooltip: {
                                    headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                                    pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of total<br/>'
                          },
                          series: [],
                          drilldown: {}
  },
  'mandivolume' : {
                          chart: {
                                  type: 'column',
                                  renderTo: 'mandivolume',
                                  tab: {
                                        'id': 'tab1',
                                        'class':'col-sm-12'
                                  },
                                  drillDown: true
                          },
                          credits:{ enabled: false },
                          title: { text: ''},
                          xAxis: { type: 'category' },
                          yAxis: {
                                  tickInterval: 10,
                                  title: { text: 'Volume' } },
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
                          tooltip: {
                                    headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                                    pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of total<br/>'
                          },
                          series: [],
                          drilldown: {}
  },
  'mandivisit' : {
                          chart: {
                                  type: 'column',
                                  renderTo: 'mandivisit',
                                  tab: {
                                        'id': 'tab1',
                                        'class':'col-sm-12'
                                  },
                                  drillDown: true
                          },
                          credits:{ enabled: false },
                          title: { text: ''},
                          xAxis: { type: 'category' },
                          yAxis: {
                                  tickInterval: 10,
                                  title: { text: 'Volume' } },
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
                          tooltip: {
                                    headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                                    pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of total<br/>'
                          },
                          series: [],
                          drilldown: {}
  },
  'mandispkcp' : {
                          chart: {
                                  type: 'column',
                                  renderTo: 'mandispkcp',
                                  tab: {
                                        'id': 'tab1',
                                        'class':'col-sm-12'
                                  },
                                  drillDown: true
                          },
                          credits:{ enabled: false },
                          title: { text: ''},
                          xAxis: { type: 'category' },
                          yAxis: {
                                  tickInterval: 10,
                                  title: { text: 'Volume' } },
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
                          tooltip: {
                                    headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                                    pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of total<br/>'
                          },
                          series: [],
                          drilldown: {}
  },
  'mandirecoveredtotal' : {
                          chart: {
                                  type: 'column',
                                  renderTo: 'mandirecoveredtotal',
                                  tab: {
                                        'id': 'tab1',
                                        'class':'col-sm-12'
                                  },
                                  drillDown: true
                          },
                          credits:{ enabled: false },
                          title: { text: ''},
                          xAxis: { type: 'category' },
                          yAxis: {
                                  tickInterval: 10,
                                  title: { text: 'Volume' } },
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
                          tooltip: {
                                    headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                                    pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of total<br/>'
                          },
                          series: [],
                          drilldown: {}
  },
  'mandifarmercount' : {
                          chart: {
                                  type: 'column',
                                  renderTo: 'mandifarmercount',
                                  tab: {
                                        'id': 'tab1',
                                        'class':'col-sm-12'
                                  },
                                  drillDown: true
                          },
                          credits:{ enabled: false },
                          title: { text: ''},
                          xAxis: { type: 'category' },
                          yAxis: {
                                  tickInterval: 10,
                                  title: { text: 'Volume' } },
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
                          tooltip: {
                                    headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                                    pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of total<br/>'
                          },
                          series: [],
                          drilldown: {}
  },
  'cropvolume' : {
                          chart: {
                                  type: 'column',
                                  renderTo: 'cropvolume',
                                  tab: {
                                        'id': 'tab1',
                                        'class':'col-sm-12'
                                  },
                                  drillDown: true
                          },
                          credits:{ enabled: false },
                          title: { text: ''},
                          xAxis: { type: 'category' },
                          yAxis: {
                                  tickInterval: 10,
                                  title: { text: 'Volume' } },
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
                          tooltip: {
                                    headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                                    pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of total<br/>'
                          },
                          series: [],
                          drilldown: {}
  },
  'cropamount' : {
                          chart: {
                                  type: 'column',
                                  renderTo: 'cropamount',
                                  tab: {
                                        'id': 'tab1',
                                        'class':'col-sm-12'
                                  },
                                  drillDown: true
                          },
                          credits:{ enabled: false },
                          title: { text: ''},
                          xAxis: { type: 'category' },
                          yAxis: {
                                  tickInterval: 10,
                                  title: { text: 'Volume' } },
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
                          tooltip: {
                                    headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                                    pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of total<br/>'
                          },
                          series: [],
                          drilldown: {}
  },
  'cropprices' : {
                          chart: {
                                  type: 'column',
                                  renderTo: 'cropprices',
                                  tab: {
                                        'id': 'tab1',
                                        'class':'col-sm-12'
                                  },
                                  drillDown: true
                          },
                          credits:{ enabled: false },
                          title: { text: ''},
                          xAxis: { type: 'category' },
                          yAxis: {
                                  tickInterval: 10,
                                  title: { text: 'Volume' } },
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
                          tooltip: {
                                    headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                                    pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of total<br/>'
                          },
                          series: [],
                          drilldown: {}
  },
  'cropfarmercount' : {
                          chart: {
                                  type: 'column',
                                  renderTo: 'cropfarmercount',
                                  tab: {
                                        'id': 'tab1',
                                        'class':'col-sm-12'
                                  },
                                  drillDown: true
                          },
                          credits:{ enabled: false },
                          title: { text: ''},
                          xAxis: { type: 'category' },
                          yAxis: {
                                  tickInterval: 10,
                                  title: { text: 'Volume' } },
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
                          tooltip: {
                                    headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                                    pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of total<br/>'
                          },
                          series: [],
                          drilldown: {}
  },*/
}
