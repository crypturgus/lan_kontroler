
nv.addGraph(function() {
  var data = jsdata_['series'];
  var xlab = jsdata_['xlabel'];
  var chart;
  var fitScreen = false;
  var width = 500;
  var height = 300;
  var zoom = 1;
  var w = width;
  var h = height;
  var diff = 2;
  chart = nv.models.lineChart()
    .options({
      duration: 300,
      useInteractiveGuideline: true,
    })
    .margin({
      top: 30,
      right: 60,
      bottom: 50,
      left: 70
    });
  chart.width(w);
  chart.height(h);
  chart.xAxis
    .axisLabel("DateTime")
    .tickFormat(function(d) {
      return xlab[d]
    });

  chart.yAxis
    .axisLabel('Temperatura (st. C)')
    .tickFormat(function(d) {
      if (d == null) {
        return 'N/A';
      }
      return d3.format(',.2f')(d);
    });
  chart.forceY([jsdata_['min'] - diff, jsdata_['max'] + diff]);

  // resizeChart();

  function resizeChart() {
    var container = d3.select('#chart1');
    var svg = container.select('svg');

    if (fitScreen) {
      // resize based on container's width AND HEIGHT
      var windowSize = nv.utils.windowSize();
      svg.attr("width", windowSize.width);
      svg.attr("height", windowSize.height);
    } else {
      // resize based on container's width
      var aspect = chart.width() / chart.height();
      var targetWidth = parseInt(container.style('width'));
      svg.attr("width", targetWidth);
      svg.attr("height", Math.round(targetWidth / aspect));
    }
  }
  nv.utils.windowResize(resizeChart);
  d3.select('#chart1 svg')
    .datum(data)
    .attr('viewBox', '0 0 ' + w + ' ' + h)
    .call(chart);



  return chart;
});
