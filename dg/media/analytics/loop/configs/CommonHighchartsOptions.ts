export const commonOptions = {
  colors: [
    '#F37B55',
    '#656566',
  ],
  // legend: {
  //   enabled: true,
  //   labelFormatter: function() {
  //     var total = 0;
  //     for (var i = this.yData.length; i--;) { total += this.yData[i]; };
  //     return this.name + '- Total: ' + total;
  //   }
  // },
  credits: {
    enabled: false
  },
  plotOptions: {
    column: {
      cropThreshold: 100,
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
        enabled: true,
        formatter: function() {
          if (this.y == 0) {
            return '';
          }
          else {
            return '<b>' + this.y + '</b>';
          }
        }
      }
    },
    bar: {
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
