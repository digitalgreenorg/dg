export const cardGraphConfig = {
    'No_of_clusters' : {
        chart: {
            type: 'solidgauge',
            width: 180,
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
            stops: [
                [0.1, '#DF5353'], // green
                [0.5, '#DDDF0D'], // yellow
                [0.9, '#55BF3B'] // red
            ],
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
            name:'present',
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:25px;color: black' +
                        '">{y}</span><br/>'
            },
            tooltip: {
                valueSuffix: null
            },
        }]
    },

    'No_of_Farmers' : {
        chart: {
            type: 'solidgauge',
            width: 180,
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
            stops: [
                [0.1, '#DF5353'], // green
                [0.5, '#DDDF0D'], // yellow
                [0.9, '#55BF3B'] // red
            ],
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
            name:'present',
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:25px;color: black' +
                        '">{y}</span><br/>'
            },
            tooltip: {
                valueSuffix: null
            },
        }]
    },
    'total_volume': {
        chart: {
            type: 'solidgauge',
            width: 180,
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
            stops: [
                [0.1, '#DF5353'], // green
                [0.5, '#DDDF0D'], // yellow
                [0.9, '#55BF3B'] // red
            ],
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
            name:'present',
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:25px;color: black' +
                        '">{y}</span><br/>'
            },
            tooltip: {
                valueSuffix: null
            },
        }]
    },
    'Total_payment' : {
        chart: {
            type: 'solidgauge',
            width: 180,
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
            stops: [
                [0.1, '#DF5353'], // green
                [0.5, '#DDDF0D'], // yellow
                [0.9, '#55BF3B'] // red
            ],
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
            name:'present',
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:25px;color: black' +
                        '">{y}</span><br/>'
            },
            tooltip: {
                valueSuffix: null
            },
        }]
    },
    'Sustainability' : {
        chart: {
            type: 'solidgauge',
            width: 180,
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
            stops: [
                [0.1, '#DF5353'], // green
                [0.5, '#DDDF0D'], // yellow
                [0.9, '#55BF3B'] // red
            ],
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
            name:'present',
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:25px;color: black' +
                        '">{y}</span><br/>'
            },
            tooltip: {
                valueSuffix: null
            },
        }]
    },
    'Cost_per_kg' : {
        chart: {
            type: 'solidgauge',
            width: 180,
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
            stops: [
                [0.1, '#DF5353'], // green
                [0.5, '#DDDF0D'], // yellow
                [0.9, '#55BF3B'] // red
            ],
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
            name:'present',
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:25px;color: black' +
                        '">{y}</span><br/>'
            },
            tooltip: {
                valueSuffix: null
            },
        }]
    }
}