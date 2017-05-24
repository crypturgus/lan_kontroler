var checkboxes = document.getElementById("setHoursForm");
document.getElementById("time_delta").value = {
  {
    limit | safe
  }
};
var req_series_bool = {
  {
    request_series | safe
  }
};
var si = 0;
for (var i = 0; i < checkboxes.length; i++) {
  if (checkboxes[i].type == 'checkbox') {
    checkboxes[i].checked = req_series_bool[si];
    si++;
  }
}
var s1 = {
  {
    s1 | safe
  }
};
var s2 = {
  {
    s2 | safe
  }
};
var s3 = {
  {
    s3 | safe
  }
};
var s4 = {
  {
    s4 | safe
  }
};
var days = {
  {
    dt | safe
  }
};
var data = [];
if (s1.length > 1) {
  data.push({
    key: "KORYTARZ",
    values: s1
  })
};
if (s2.length > 1) {
  data.push({
    key: "ZEWNETRZE",
    values: s2
  })
};
if (s3.length > 1) {
  data.push({
    key: "PODWYZSZENIE",
    values: s3
  })
};
if (s4.length > 1) {
  data.push({
    key: "WILGOTNOSC",
    values: s4
  })
};

function get_min_and_max(s1, s2, s3, s4) {
  var merged_array = [];
  merged_array.push.apply(merged_array, s1);
  merged_array.push.apply(merged_array, s2);
  merged_array.push.apply(merged_array, s3);
  merged_array.push.apply(merged_array, s4);
  var y_value_list = []
  for (ob in merged_array) {
    y_value_list.push(merged_array[ob]['y']);
  };

  var min_val = Math.min.apply(null, y_value_list);
  var max_val = Math.max.apply(null, y_value_list);
  var limit_values = {
    "min_val": min_val,
    "max_val": max_val
  };
  return limit_values
};


var min_max = get_min_and_max(s1, s2, s3, s4);


nv.addGraph(function() {
  var chart = nv.models.lineChart()
    .color(d3.scale.category10().range())
    .margin({
      top: 30,
      right: 60,
      bottom: 50,
      left: 70
    });
  var fitScreen = false;
  var width = 500;
  var height = 300;
  var zoom = 1;

  chart.useInteractiveGuideline(true);

  chart.xAxis
    .tickFormat(function(d) {
      return days[d]
    });

  chart.yAxis //Chart y-axis settings
    .tickFormat(d3.format('.02f'));

  chart.lines.dispatch.on("elementClick", function(evt) {
    console.log(evt);
  });

  var min_ = min_max['min_val'];
  var max_ = min_max['max_val'];
  var diff = (max_ - min_) * 0.10;
  diff = 2
  chart.forceY([min_ - diff, max_ + diff]);


  d3.select('#chart1 svg')
    .attr('perserveAspectRatio', 'xMinYMid')
    .datum(data);


  setChartViewBox();
  resizeChart();

  nv.utils.windowResize(resizeChart);


  function setChartViewBox() {
    var w = width * zoom,
      h = height * zoom;

    chart
      .width(w)
      .height(h);

    d3.select('#chart1 svg')
      .attr('viewBox', '0 0 ' + w + ' ' + h)
      .transition().duration(500)
      .call(chart);
  }


  // This resize simply sets the SVG's dimensions, without a need to recall the chart code
  // Resizing because of the viewbox and perserveAspectRatio settings
  // This scales the interior of the chart unlike the above
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
  return chart;
});
