export const chartsConfig = {
  'cummulativeCount' : {
                          chart: {
                                  type: 'column',
                                  renderTo: 'cummulativeCount',
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
  
}
