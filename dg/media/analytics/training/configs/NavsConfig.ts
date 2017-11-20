export const navsConfig = {
  'navs': {
    ' ': {
      'active': true,
      'filters': true,
      'import': {
        'overall': true,
        'recent': true,
      },
      'classes': {
        'container1': 'col-md-11',
      },
      'addTab': true,
      'containers': {
        'container1': {
          'Trainings': {
            'addDivs': ['state_trainer_#trainings','state_trainer_#mediators']
          },
          'Question': {
            'addDivs': ['question_wise_data']
          },
          'Time Period': {
            'addDivs': ['year_month_wise_data']
          }
        }
      }
    }
  }
}
