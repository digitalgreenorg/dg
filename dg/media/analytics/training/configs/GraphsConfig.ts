import { commonOptions } from './CommonHighchartsOptions';

export const chartsConfig = {
  'state_trainer_#trainings': {
    chart: {
      type: 'column',
      renderTo: 'state_trainer_#trainings', // to be kept as same as the key for this particular object.
      tab: {
        'id': 'tab1',
        'class': 'col-6'
      },
      drillDown: true
    },
    title: {
      text: 'Trainings Conducted',
      style: {
        "color": "#656566",
      }
    },
    xAxis: {
      type: 'category',
      labels: {
        rotation: 0
      }
    },
    yAxis: {
      tickInterval: 10,
      title: { text: 'Number of Trainings' }
    },
    tooltip: {
      headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
      pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of total<br/>'
    },
    series: [],
    drilldown: {
      activeAxisLabelStyle: {
        color: '#656566'
      },
      activeDataLabelStyle: {
        color: '#656566'
      },
      allowPointDrilldown: false,
      series: []
    },
  },

  'state_trainer_#mediators': {
    chart: {
      type: 'column',
      renderTo: 'state_trainer_#mediators',
      tab: {
        'id': 'tab3',
        'class': 'col-6'
      },
      drillDown: true
    },
    title: {
      text: 'Mediators trained',
      style: {
        "color": "#656566",
      }
    },
    xAxis: {
      type: 'category',
      labels: {
        rotation: 0
      }
    },
    yAxis: { title: { text: 'Number of Mediators' } },
    tooltip: {
      headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
      pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of total<br/>'
    },
    series: [],
    drilldown: {
      activeAxisLabelStyle: {
        color: '#656566'
      },
      activeDataLabelStyle: {
        color: '#656566'
      },
      allowPointDrilldown: false,
      series: []
    },
  },

  'state_wise_gender_data': {
    chart: {
      type: 'column',
      renderTo: 'state_wise_gender_data',
      tab: {
        'id': 'tab3',
        'class': 'col-6'
      },
      drillDown: false
    },
    title: {
      text: 'Gender Wise Distribution',
      style: {
        "color": "#656566",
      }
    },
    xAxis: {
      type: 'category',
      labels: {
        rotation: 0
      }
    },
    yAxis: { title: { text: 'Number of Mediators' } },
    tooltip: {
      headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
      pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> {series.name}<br/>'
    },
    series: [],
  },

  'question_wise_data': {
    chart: {
      type: 'column',
      renderTo: 'question_wise_data',
      tab: {
        'id': 'tab2',
        'class': 'col-12'
      },
      drillDown: false
    },
    title: {
      text: 'Questions Answered Correctly',
      style: {
        "color": "#656566",
      }
    },
    xAxis: {
      type: 'category',
      labels: {
        rotation: 0
      }
    },
    yAxis: {
      min: 0,
      max: 100,
      title: { text: 'Percentage Answered' }
    },
    // plotOptions: {
    //   column: {
    //     grouping: false,
    //     borderWidth: 0,
    //     dataLabels: {
    //       enabled: true,
    //       format: '{point.y}%'
    //     }
    //   }
    // },
    tooltip: {
      headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
      pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of total<br/>'
    },
    series: [],
    drilldown: {}
  },

  'year_month_wise_data': {
    chart: {
      type: 'column',
      renderTo: 'year_month_wise_data',
      tab: {
        'id': 'tab1',
        'class': 'col-6'
      },
      drillDown: true
    },
    title: {
      text: 'Periodical Trainings Conducted',
      style: {
        "color": "#656566",
      }
    },
    xAxis: {
      type: 'category',
      labels: {
        rotation: 0
      }
    },
    yAxis: { title: { text: 'Number of Trainings' } },
    tooltip: {
      headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
      pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of total<br/>'
    },
    series: [],
    drilldown: {
      activeAxisLabelStyle: {
        color: '#656566'
      },
      activeDataLabelStyle: {
        color: '#656566'
      },
      allowPointDrilldown: false,
      series: []
    },
  },
}

export class AddCommonOptions {
  public AddCommonOptionsToGraph(): void {
    Object.keys(chartsConfig).forEach(key => {
      Object.assign(chartsConfig[key], commonOptions);
    });
  }
}
