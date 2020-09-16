google.load("visualization", "1", {
  packages: ["controls"]
});
google.setOnLoadCallback(drawCharts);

var exp_total_line_chart;
var color_arr = ['#008000', '#ff0000', '#1489B6', '#9BA0A7', '#66E214'];
var line_options = {
  colors: color_arr,
  lineWidth: 2,
  hAxis: {
    slantedText: false,
    maxAlternation: 1
  }
};

function drawCharts() {

  $.getJSON('/coco/analytics/overview_line_graph/' + search_params, {
    type: ['prod', 'screen', 'prac', 'person', 'adopt']
  }, function(analytics_data) {
    overview_line(analytics_data);
  });
}

function overview_line(analytics_data) {
  var total_line_chart_data = google.visualization.arrayToDataTable(analytics_data, false);
  var options = jQuery.extend(true, {}, line_options);
  options['legend'] = {
    position: 'bottom',
    alignment: 'start',
    textStyle: {
      fontSize: 12
    }
  };
  options['chartArea'] = {
    left: 100,
    top: 40,
    width: "90%",
    height: "70%"
  };
  options['vAxis'] = {
    logScale: true
  }
  // var options = {
  // series: {
  //         0: {targetAxisIndex: 0},
  //         1: {targetAxisIndex: 1}
  //       },
  //       vAxes: {
  //         // Adds titles to each axis.
  //         0: {title: 'Temps (Celsius)'},
  //         1: {title: 'Daylight'}
  //       },
  //       chartArea:{
          
  //   width: "80%",
    
  // },
  // legend : {
  //   position: 'bottom',
  //   alignment: 'start',
  //   textStyle: {
  //     fontSize: 12
  //   }
  // }
  // vAxis: {
  //           logScale: true
  //       }

  //     };

  var total_line_chart = new google.visualization.ChartWrapper({
    'chartType': 'LineChart',
    'containerId': 'javascript_total_line',
    'options': options,
    'dataTable': total_line_chart_data
  });

  total_line_chart.draw();
  exp_total_line_chart = new google.visualization.ChartWrapper({
    'chartType': 'LineChart',
    'options': options,
    'dataTable': total_line_chart_data
  });
}
