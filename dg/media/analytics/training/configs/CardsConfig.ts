export const cardConfig = {
  'no_trainings': {
    text: 'Number of Trainings',
    helpTip : 'Group of villages in close proximity served by one Loop aggregator.',
    overall: {
      filter: false,
      show: true,
      text: 'No_of_trainings',
      borrowData: false,
      cards : true,
    },
    recent: {
      dateRange: 60, // In days
      filter: true,
      show: true,
      text: 'No_of_trainings',
      borrowData: false,
      cards : true,
    },
  },

  'no_mediators': {
    text: 'Number of Mediators',
    helpTip : 'Group of villages in close proximity served by one Loop aggregator.',
    overall: {
      filter: false,
      show: true,
      text: 'No_of_mediators',
      borrowData: false,
      cards : true,
    },
    recent: {
      dateRange: 60, // In days
      filter: true,
      show: true,
      text: 'No_of_mediators',
      borrowData: false,
      cards : true,
    },
  },

  'pass_%': {
    text: 'Pass Percentage',
    helpTip : 'Group of villages in close proximity served by one Loop aggregator.',
    overall: {
      filter: false,
      show: true,
      text: 'Pass_percentage',
      borrowData: false,
      cards : true,
    },
    recent: {
      dateRange: 60, // In days
      filter: true,
      show: true,
      text: 'Pass_percentage',
      borrowData: false,
      cards : true,
    },
  },

  'avg_score': {
    text: 'Average Score',
    helpTip : 'Group of villages in close proximity served by one Loop aggregator.',
    overall: {
      filter: false,
      show: true,
      text: 'Average_score',
      borrowData: false,
      cards : true,
    },
    recent: {
      dateRange: 60, // In days
      filter: true,
      show: true,
      text: 'Average_score',
      borrowData: false,
      cards : true,
    },
  },

}
