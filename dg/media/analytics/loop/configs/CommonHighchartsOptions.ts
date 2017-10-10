export const commonOptions = {
  colors: [
    '#F37B55',
    '#656566',
  ],
  legend: { enabled: true },
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
  title: { text: '' },
  scrollbar: {
    enabled: true
  },
  lang: {
    drillUpText: "<< Back"
  }
}
