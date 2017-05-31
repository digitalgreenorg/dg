export const chartsConfig = [
  {
    chart: {
      type: 'column',
      renderTo: 'column_tab_3',
      tab: {
          'id': 'tab1',
          'class':'col-sm-6 container'
      },
      drillDown: true
    },
    credits: {
        enabled: false
    },
    chartName: 'state__#trainings',
    title: {
      text: 'Trainings Conducted'
    },
    xAxis: { type: 'category' },
    yAxis: {
      title: {
        text: 'Number of Trainings'
      }
    },
    legend: {
      enabled: false
    },
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
  {
    chart: {
      type: 'column',
      renderTo: 'column',
      tab: {
          'id': 'tab1',
          'class':'col-sm-6 container'
      },
      drillDown: true
    },
    credits: {
        enabled: false
    },
    chartName: 'state_district__#trainings',
    title: {
      text: 'Mediators trained '
    },
    subtitle: {
      text: 'Click the columns to view state wise trainer figures.'
    },
    xAxis: { type: 'category' },
    yAxis: {
      title: {
        text: 'Number of Mediators'
      }
    },
    legend: {
      enabled: false
    },
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
  {
    chart: {
      type: 'column',
      renderTo: 'graph_3',
      tab: {
          'id': 'tab2',
          'class':'col container'
      },
      drillDown: false
    },
    credits: {
        enabled: false
    },
    chartName: 'question_wise_data',
    title: {
      text: 'Questions Answered Correctly'
    },
    xAxis: { type: 'category' },
    yAxis: {
      title: {
        text: 'Percentage Answered'
      }
    },
    legend: {
      enabled: false
    },
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
  {
    chart: {
      type: 'column',
      renderTo: 'graph_4',
      tab: {
          'id': 'tab3',
          'class':'col container'
      },
      drillDown: true
    },
    credits: {
        enabled: false
    },
    chartName: 'year_month_wise_data',
    title: {
      text: 'Periodical Trainings Conducted'
    },
    xAxis: { type: 'category' },
    yAxis: {
      title: {
        text: 'Number of Trainings'
      }
    },
    legend: {
      enabled: false
    },
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
  
]
