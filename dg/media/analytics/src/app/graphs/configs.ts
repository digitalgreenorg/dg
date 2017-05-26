export const chartsConfig = [
  {
    chart: {
      type: 'column',
      renderTo: 'column_tab_3',
      tab: {
          'id': 'tab1',
          'class':'col-sm-6 imageBox'
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
          'class':'col-sm-6 imageBox'
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
  
]
