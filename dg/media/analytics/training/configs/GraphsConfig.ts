export const chartsConfig = {
  'state_trainer_#trainings' : {
                          chart: {
                                  type: 'column',
                                  renderTo: 'graph_1',
                                  tab: {
                                        'id': 'tab1',
                                        'class':'col-sm-6'
                                  },
                                  drillDown: true
                          },
                          credits:{ enabled: false },
                          title: { text: 'Trainings Conducted'},
                          xAxis: { type: 'category' },
                          yAxis: {
                                  tickInterval: 10, 
                                  title: { text: 'Number of Trainings' } },
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
  
  'state_trainer_#mediators':{
                                chart: {
                                        type: 'column',
                                        renderTo: 'graph_2',
                                        tab: {
                                            'id': 'tab1',
                                            'class':'col-sm-6'
                                        },
                                        drillDown: true
                                },
                                credits: { enabled: false },
                                title: { text: 'Mediators trained'},
                                subtitle: { text: 'Click the columns to view state wise trainer figures.'},
                                xAxis: { type: 'category' },
                                yAxis: { title: { text: 'Number of Mediators' } },
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
                                            drillUpButton: {
                                                       relativeTo: 'spacingBox',
                                                       position: {
                                                                y: 0,
                                                                x: -30
                                                        },
                                            },
                                            allowPointDrilldown: false,
                                            series: []
                                },
                                lang: {
                                        drillUpText: '<< Back'
                                },
  },

  'question_wise_data':{
                        chart: {
                                type: 'column',
                                renderTo: 'graph_3',
                                tab: {
                                    'id': 'tab2',
                                    'class':'col-sm-12'
                                },
                                drillDown: false
                        },
                        credits: { enabled: false },
                        title: {
                                text: 'Questions Answered Correctly'
                        },
                        xAxis: { type: 'category' },
                        yAxis: {
                                min : 0,
                                max : 100,
                                title: { text: 'Percentage Answered'} },
                        legend: { enabled: false },
                        plotOptions: {
                                      column: {
                                              grouping: false,
                                              borderWidth: 0,
                                              dataLabels: {
                                                enabled: true,
                                                format: '{point.y}%'
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

  'year_month_wise_data':{
                          chart: {
                                  type: 'column',
                                  renderTo: 'graph_4',
                                  tab: {
                                      'id': 'tab3',
                                      'class':'col-sm-12'
                                  },
                                  drillDown: true
                          },
                          credits: { enabled: false },
                          title: { text: 'Periodical Trainings Conducted' },
                          xAxis: { type: 'category' },
                          yAxis: { title: { text: 'Number of Trainings'} },
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
                                        drillUpButton: {
                                                       relativeTo: 'spacingBox',
                                                       position: {
                                                                y: 0,
                                                                x: -30
                                                        },
                                        },
                                        allowPointDrilldown: false,
                                        series: []
                          },
                          lang: {
                                drillUpText: '<< Back'
                          },
        },
  
}
