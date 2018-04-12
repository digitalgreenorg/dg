export const commonOptions = {
  colors: [
    '#7C287D',
    '#9AA0A7',
  ],
  legend: { enabled: false },
  credits: {
    enabled: false
  },
  plotOptions: {
    column: {
      grouping: false,
      borderWidth: 0,
      dataLabels: {
        enabled: true
      }
    },
    areaspline: {
      fillOpacity: 0.3
    },
    columnrange: {
      grouping: false,
      borderWidth: 0,
      dataLabels: {
        enabled: true
      }
    }
  },
  // title: { text: '' },
  scrollbar: {
    enabled: true
  },
  lang: {
    drillUpText: "<< Back"
  }
}
