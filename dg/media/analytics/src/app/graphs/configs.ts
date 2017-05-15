export const configs = [
    {   
        chart:{
            type:'line',
            renderTo: 'line_chart'
        },
        chartName : 'state_#trainings',
        title : {text : 'State wise traingings conducted'},
        tabHolder : {'id':'line_chart','heading':'Line Chart'},
        xAxis:{categories:[]},
        plotOptions: {
            line: {
                dataLabels: {enabled: true},
            }
        },
        series: []
    },
    {
        chart:{
            type:'bar',
            renderTo: 'bar_chart'
        },
        chartName : 'state_#trainings',
        title: {text: 'District wise traingings conducted'},
        tabHolder : {'id':'bar_chart','heading':'Bar Chart'},
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
        chart:{
            type:'pie',
            renderTo: 'pie_chart'
        },
        chartName : 'sate_%trainings',
        title: {text: 'State wise number of trainings'},
        tabHolder : {'id':'pie_chart','heading':'Pie Chart'},
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