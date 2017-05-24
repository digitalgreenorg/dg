export const chartsConfig = [
  {
    chart: {
      type: 'column',
      renderTo: 'column',
      tabID: 'tab1',
      drillDown: true
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
      type: 'line',
      renderTo: 'line_chart',
      tabID: 'tab2',
      drillDown: false
    },
    chartName: 'state_#trainings',
    title: { text: 'State wise traingings conducted' },
    xAxis: { categories: [] },
    plotOptions: {
      line: {
        dataLabels: { enabled: true },
      }
    },
    series: [],
    drilldown: { series: [] }
  },
  {
    chart: {
      type: 'bar',
      renderTo: 'bar_chart',
      tabID: 'tab2',
      drillDown: false
    },
    chartName: 'state_#trainings',
    title: { text: 'District wise traingings conducted' },
    xAxis: {
      categories: [],
      title: {
        text: null
      }
    },
    yAxis: {
      min: 0,
      title: { text: 'Trainings' },
    },
    plotOptions: {
      bar: {
        dataLabels: {
          enabled: true
        }
      }
    },
    series: [],
    drilldown: { series: [] }
  },
  {
    chart: {
      type: 'pie',
      renderTo: 'pie_chart',
      tabID: 'tab2',
      drillDown: false
    },
    chartName: 'sate_%trainings',
    title: { text: 'State wise number of trainings' },
    tooltip: { pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>' },
    plotOptions: {
      pie: {
        allowPointSelect: true,
        cursor: 'pointer',
        dataLabels: {
          enabled: true,
          format: '<b>{point.name}</b>: {point.percentage:.1f} %',
        }
      }
    },
    xAxis: { categories: [] },
    series: [],
    drilldown: {
      series: []
    }
  },
  {
    chart: {
      type: 'column',
      renderTo: 'column_tab_3',
      tabID: 'tab1',
      drillDown: true
    },
    chartName: 'state__#trainings',
    title: {
      text: '# of Trainings '
    },
    // subtitle: {
    //   text: 'Click the columns to view state wise trainer figures.'
    // },
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
  }
]
