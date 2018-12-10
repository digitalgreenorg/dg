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
        'container1': 'col-md-12',
      },
      'addTab': true,
      'containers': {
        'container1': {
          'Trainings': {
            'addDivs': ['state_trainer_#trainings','year_month_wise_data']
          },
          'Participants Trained': {
            'addDivs': ['state_trainer_#mediators']
          },
          'Gender Distribution': {
            'addDivs': ['state_wise_gender_data']
          },
          'Assessment': {
            'addDivs': ['question_wise_data']
          }
        }
      }
    }
  }
}
