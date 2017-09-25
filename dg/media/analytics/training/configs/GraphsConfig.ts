import { commonOptions } from './CommonHighchartsOptions';

export const chartsConfig = {
  'state_trainer_#trainings': {
    chart: {
      type: 'column',
      renderTo: 'state_trainer_#trainings',
      tab: {
        'id': 'tab1',
        'class': 'col-sm-6'
      },
      drillDown: true
    },
    title: {
      text: 'Trainings Conducted',
      style: {
        "color": "#656566",
      }
    },
    xAxis: { type: 'category' },
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
        'id': 'tab1',
        'class': 'col-sm-6'
      },
      drillDown: true
    },
    title: {
      text: 'Mediators trained',
      style: {
        "color": "#656566",
      }
    },
    xAxis: { type: 'category' },
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

  'question_wise_data': {
    chart: {
      type: 'column',
      renderTo: 'question_wise_data',
      tab: {
        'id': 'tab2',
        'class': 'col'
      },
      drillDown: false
    },
    title: {
      text: 'Questions Answered Correctly',
      style: {
        "color": "#656566",
      }
    },
    xAxis: { type: 'category' },
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
        'id': 'tab3',
        'class': 'col'
      },
      drillDown: true
    },
    title: {
      text: 'Periodical Trainings Conducted',
      style: {
        "color": "#656566",
      }
    },
    xAxis: { type: 'category' },
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
