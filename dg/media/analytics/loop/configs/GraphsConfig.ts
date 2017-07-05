export const chartsConfig = {
  'cummulativeCount': {
    chart: {
      type: 'column',
      renderTo: 'cummulativeCount',
      tab: {
        'id': 'tab1',
        'class': 'col-sm-12'
      },
      drillDown: true
    },
    credits: { enabled: false },
    title: { text: '' },
    xAxis: { type: 'category' },
    yAxis: {
      tickInterval: 10,
      title: { text: 'Volume' }
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
    series: [{
      name: 'Installation',
      data: [43934, 52503, 57177, 69658, 97031, 119931, 137133, 154175]
    }, {
        name: 'Manufacturing',
        data: [24916, 24064, 29742, 29851, 32490, 30282, 38121, 40434]
      }, {
        name: 'Sales & Distribution',
        data: [11744, 17722, 16005, 19771, 20185, 24377, 32147, 39387]
      }, {
        name: 'Project Development',
        data: [null, null, 7988, 12169, 15112, 22452, 34400, 34227]
      }, {
        name: 'Other',
        data: [12908, 5948, 8105, 11248, 8989, 11816, 18274, 18111]
      }],
    drilldown: {}
  },
  /*'aggrvol' : {
                          chart: {
                                  type: 'column',
                                  renderTo: 'aggrvol',
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
  'aggrvisit' : {
                          chart: {
                                  type: 'column',
                                  renderTo: 'aggrvisit',
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
  'aggrrecoveredtotal' : {
                          chart: {
                                  type: 'column',
                                  renderTo: 'aggrrecoveredtotal',
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
  'volFarmerTS': {
    chart: {
      type: 'areaspline'
    },
    title: {
      text: 'Average fruit consumption during one week'
    },
    legend: {
      layout: 'vertical',
      align: 'left',
      verticalAlign: 'top',
      x: 150,
      y: 100,
      floating: true,
      borderWidth: 1,
    },
    xAxis: {
      categories: [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday'
      ],
      plotBands: [{ // visualize the weekend
        from: 4.5,
        to: 6.5,
        color: 'rgba(68, 170, 213, .2)'
      }]
    },
    yAxis: {
      title: {
        text: 'Fruit units'
      }
    },
    tooltip: {
      shared: true,
      valueSuffix: ' units'
    },
    credits: {
      enabled: false
    },
    plotOptions: {
      areaspline: {
        fillOpacity: 0.5
      }
    },
    series: [{
      name: 'John',
      data: [3, 4, 3, 5, 4, 10, 12]
    }, {
        name: 'Jane',
        data: [1, 3, 4, 3, 3, 5, 4]
      }]
  }
}
