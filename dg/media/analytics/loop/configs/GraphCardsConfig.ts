const stopsColor = [
  [0.1, '#D14027'],
  [0.5, '#D3E7B6'],
  [0.9, '#7AC143']
];
export const cardGraphConfig = {
  'No_of_clusters': {
    chart: {
      type: 'solidgauge',
      width: 160,
      height: 100,
      plotBackgroundColor: null,
      plotBackgroundImage: null,
      plotBorderWidth: 0,
      plotShadow: false,
      margin: [-10, 0, 0, 0]
    },

    title: '#Clusters',
    pane: {
      center: ['50%', '85%'],
      size: '140%',
      startAngle: -90,
      endAngle: 90,
      background: {
        backgroundColor: '#EEE',
        innerRadius: '60%',
        outerRadius: '100%',
        shape: 'arc'
      }
    },

    tooltip: {
      enabled: false
    },

    exporting: {
      enabled: false
    },
    // the value axis
    yAxis: {
      stops: stopsColor,
      lineWidth: 0,
      minorTickInterval: null,
      tickAmount: 2,
      labels: {
        y: 16
      },
      min: 0,
      max: 50
    },

    plotOptions: {
      solidgauge: {
        dataLabels: {
          y: 5,
          borderWidth: 0,
          useHTML: true
        }
      }
    },

    credits: {
      enabled: false
    },

    series: [{
      name: 'present',
      dataLabels: {
        format: '<div style="text-align:center"><span style="font-size:1.3em;color: #3D3D3F' +
        '">' + '{y:,.0f}' + '</span><br/></div>'
      },
      tooltip: {
        valueSuffix: null
      },
    }]
  },

  'No_of_Farmers': {
    chart: {
      type: 'solidgauge',
      width: 160,
      height: 100,
      plotBackgroundColor: null,
      plotBackgroundImage: null,
      plotBorderWidth: 0,
      plotShadow: false,
      margin: [-10, 0, 0, 0]
    },

    title: '#Farmers',

    pane: {
      center: ['50%', '85%'],
      size: '140%',
      startAngle: -90,
      endAngle: 90,
      background: {
        backgroundColor: '#EEE',
        innerRadius: '60%',
        outerRadius: '100%',
        shape: 'arc'
      }
    },

    tooltip: {
      enabled: false
    },

    exporting: {
      enabled: false
    },
    // the value axis
    yAxis: {
      stops: stopsColor,
      lineWidth: 0,
      minorTickInterval: null,
      tickAmount: 2,
      labels: {
        y: 16
      },
      min: 0,
      max: 8000
    },

    plotOptions: {
      solidgauge: {
        dataLabels: {
          y: 5,
          borderWidth: 0,
          useHTML: true
        }
      }
    },

    credits: {
      enabled: false
    },

    series: [{
      name: 'present',
      dataLabels: {
        format: '<div style="text-align:center"><span style="font-size:1.3em;color: #3D3D3F' +
        '">' + '{y:,.0f}' + '</span><br/></div>'
      },
      tooltip: {
        valueSuffix: null
      },
    }]
  },
  'total_volume': {
    chart: {
      type: 'solidgauge',
      width: 160,
      height: 100,
      plotBackgroundColor: null,
      plotBackgroundImage: null,
      plotBorderWidth: 0,
      plotShadow: false,
      margin: [-10, 0, 0, 0]
    },

    title: 'Volume',

    pane: {
      center: ['50%', '85%'],
      size: '140%',
      startAngle: -90,
      endAngle: 90,
      background: {
        backgroundColor: '#EEE',
        innerRadius: '60%',
        outerRadius: '100%',
        shape: 'arc'
      }
    },

    tooltip: {
      enabled: false
    },

    exporting: {
      enabled: false
    },
    // the value axis
    yAxis: {
      stops: stopsColor,
      lineWidth: 0,
      minorTickInterval: null,
      tickAmount: 2,
      labels: {
        y: 16
      },
      min: 0,
      max: 8000000
    },

    plotOptions: {
      solidgauge: {
        dataLabels: {
          y: 5,
          borderWidth: 0,
          useHTML: true
        }
      }
    },

    credits: {
      enabled: false
    },

    series: [{
      name: 'present',
      dataLabels: {
        format: '<div style="text-align:center"><span style="font-size:1.3em;color: #3D3D3F' +
        '">' + '{y:,.0f}' + '</span><br/></div>'
      },
      tooltip: {
        valueSuffix: null
      },
    }]
  },
  'Total_payment': {
    chart: {
      type: 'solidgauge',
      width: 160,
      height: 100,
      plotBackgroundColor: null,
      plotBackgroundImage: null,
      plotBorderWidth: 0,
      plotShadow: false,
      margin: [-10, 0, 0, 0]
    },

    title: 'Payments',

    pane: {
      center: ['50%', '85%'],
      size: '140%',
      startAngle: -90,
      endAngle: 90,
      background: {
        backgroundColor: '#EEE',
        innerRadius: '60%',
        outerRadius: '100%',
        shape: 'arc'
      }
    },

    tooltip: {
      enabled: false
    },

    exporting: {
      enabled: false
    },
    // the value axis
    yAxis: {
      stops: stopsColor,
      lineWidth: 0,
      minorTickInterval: null,
      tickAmount: 2,
      labels: {
        y: 16
      },
      min: 0,
      max: 80000000
    },

    plotOptions: {
      solidgauge: {
        dataLabels: {
          y: 5,
          borderWidth: 0,
          useHTML: true
        }
      }
    },

    credits: {
      enabled: false
    },

    series: [{
      name: 'present',
      dataLabels: {
        format: '<div style="text-align:center"><span style="font-size:1.3em;color: #3D3D3F' +
        '">' + '{y:,.0f}' + '</span><br/></div>'
      },
      tooltip: {
        valueSuffix: null
      },
    }]
  },
  'Sustainability': {
    chart: {
      type: 'solidgauge',
      width: 160,
      height: 100,
      plotBackgroundColor: null,
      plotBackgroundImage: null,
      plotBorderWidth: 0,
      plotShadow: false,
      margin: [-10, 0, 0, 0]
    },

    title: 'Sustainability',

    pane: {
      center: ['50%', '85%'],
      size: '140%',
      startAngle: -90,
      endAngle: 90,
      background: {
        backgroundColor: '#EEE',
        innerRadius: '60%',
        outerRadius: '100%',
        shape: 'arc'
      }
    },

    tooltip: {
      enabled: false
    },

    exporting: {
      enabled: false
    },
    // the value axis
    yAxis: {
      stops: stopsColor,
      lineWidth: 0,
      minorTickInterval: null,
      tickAmount: 2,
      labels: {
        y: 16
      },
      min: 0,
      max: 50
    },

    plotOptions: {
      solidgauge: {
        dataLabels: {
          y: 5,
          borderWidth: 0,
          useHTML: true
        }
      }
    },

    credits: {
      enabled: false
    },

    series: [{
      name: 'present',
      dataLabels: {
        format: '<div style="text-align:center"><span style="font-size:1.3em;color: #3D3D3F' +
        '">{y}</span><br/></div>'
      },
      tooltip: {
        valueSuffix: null
      },
    }]
  },
  'Cost_per_kg': {
    chart: {
      type: 'solidgauge',
      width: 160,
      height: 100,
      plotBackgroundColor: null,
      plotBackgroundImage: null,
      plotBorderWidth: 0,
      plotShadow: false,
      margin: [-10, 0, 0, 0]
    },

    title: 'Cost per Kg',

    pane: {
      center: ['50%', '85%'],
      size: '140%',
      startAngle: -90,
      endAngle: 90,
      background: {
        backgroundColor: '#EEE',
        innerRadius: '60%',
        outerRadius: '100%',
        shape: 'arc'
      }
    },

    tooltip: {
      enabled: false
    },

    exporting: {
      enabled: false
    },
    // the value axis
    yAxis: {
      stops: stopsColor,
      lineWidth: 0,
      minorTickInterval: null,
      tickAmount: 2,
      labels: {
        y: 16
      },
      min: -1,
      max: 0
    },

    plotOptions: {
      solidgauge: {
        dataLabels: {
          y: 5,
          borderWidth: 0,
          useHTML: true
        }
      }
    },

    credits: {
      enabled: false
    },

    series: [{
      name: 'present',
      dataLabels: {
        format: '<div style="text-align:center"><span style="font-size:1.3em;color: #3D3D3F' +
        '">{y}</span><br/></div>'
      },
      tooltip: {
        valueSuffix: null
      },
    }]
  },
  'No_of_clusters_spark': {
    chart: {
      margin: [40, 10, 40, 40],
      height: 160,
      width: 160,
      type: 'area',
    },
    title: '#Clusters_spark',
    legend: { enabled: false },
    exporting: { enabled: false },
    credits: {
      enabled: false
    },
    plotOptions: {
      area: {
        lineWidth: 2,
        color: '#D14027',
        // marker: { enabled: false },
      }
    },
    xAxis: {
      title: { text: '' },
      lineWidth: .1,
      lineColor: '#000',
      tickWidth: .5,
      tickLength: 3,
      tickColor: '#000'
    },
    yAxis: {
      gridLineColor: '#eee',
      gridLineWidth: .5,
      lineWidth: .1,
      lineColor: '#000',
      tickWidth: .5,
      tickLength: 3,
      tickColor: '#000',
      title: { text: '' }
    },
    series: [{
      name: 'Chart',
      marker: {
        radius: 1,
        states: {
          hover: {
            radius: 2
          }
        }
      },
      fillOpacity: 0.25,
    }]
  }
}
