var jsdata = {
    "series": [{
      "color": "#800000",
      "values": [{
        "y": 11,
        "x": 0
      }, {
        "y": 8,
        "x": 1
      }, {
        "y": 11,
        "x": 2
      }, {
        "y": 8,
        "x": 3
      }, {
        "y": 11,
        "x": 4
      }, {
        "y": 8,
        "x": 5
      }, {
        "y": 11,
        "x": 6
      }, {
        "y": 8,
        "x": 7
      }, {
        "y": 11,
        "x": 8
      }, {
        "y": 8,
        "x": 9
      }],
      "key": "DUPA"
    }, {
      "color": "#ff7f0e",
      "values": [{
        "y": 33.5,
        "x": 0
      }, {
        "y": 13.0,
        "x": 1
      }, {
        "y": 7.1,
        "x": 2
      }, {
        "y": 7.4,
        "x": 3
      }, {
        "y": 0.8,
        "x": 4
      }, {
        "y": 9.9,
        "x": 5
      }, {
        "y": 18.9,
        "x": 6
      }, {
        "y": 13.1,
        "x": 7
      }, {
        "y": 17.0,
        "x": 8
      }, {
        "y": 0.3,
        "x": 9
      }],
      "key": "s2"
    }, {
      "color": "#000080",
      "values": [{
        "y": 13.5,
        "x": 0
      }, {
        "y": 20.0,
        "x": 1
      }, {
        "y": 0.1,
        "x": 2
      }, {
        "y": 9.4,
        "x": 3
      }, {
        "y": 5.8,
        "x": 4
      }, {
        "y": 3.9,
        "x": 5
      }, {
        "y": 3.9,
        "x": 6
      }, {
        "y": 23.1,
        "x": 7
      }, {
        "y": 7.0,
        "x": 8
      }, {
        "y": 0,
        "x": 9
      }],
      "key": "s3"
    }],
    "xlabel": ["12:00", "12:10", "12:20", "12:30", "12:40", "12:50",
      "13:00", "13:10", "13:20", "13:30"
    ],
    "tickValues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
  }
  //    var width = 400, height = 600;

nv.addGraph(function() {
  var data = jsdata['series'];
  var xlab = jsdata['xlabel'];
  var chart;
  var fitScreen = false;
  var width = 500;
  var height = 300;
  var zoom = 1;
  var w = width;
  var h = height;
  var tickValues = jsdata["tickValues"]

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
    .axisLabel("DateTime (s)")
    .tickFormat(d3.format(',.1f'))
    .staggerLabels(true)
    .tickValues(tickValues)
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
