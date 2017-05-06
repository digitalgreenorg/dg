export const configs = [
    {   chart:{type:'line'},
        placeholder : 'line_chart',
        title : {text : 'State wise traingings conducted'},
        xAxis:{categories:[]},
        plotOptions: {
            line: {
                dataLabels: {enabled: true},
            }
        },
        series: []
    },
    {
        chart: {type: 'bar'},
        placeholder : 'bar_chart',
        title: {text: 'District wise traingings conducted'},
        xAxis: {
            categories: [],
            title: {
                text: null
            }
        },
        yAxis: {
            min: 0,
            title: {text: 'Trainings'},
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: true
                }
            }
        },
        series: []

    },
    {
        chart: {type: 'pie'},
        placeholder : 'pie_chart',
        title: {text: 'State wise number of trainings'},
        tooltip: {pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'},
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                }
            }
        },
        xAxis : {categories: []},
        series: []
    }
   

]