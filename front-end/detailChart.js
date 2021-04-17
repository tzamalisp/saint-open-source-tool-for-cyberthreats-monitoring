var apple=[];
$.getJSON(
    'http://150.140.193.156:2080/saint/markets/allBugsRatePerDay.json',
    function (rate_data) {
        var detailChart;

        Highcharts.chart('container6', {
    chart: {
        type: 'area',
        zoomType: 'x'
    },
    title: {
        text: 'Resolved Reports per day'
    },
    subtitle: {
                text: document.ontouchstart === undefined ?
                        'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
            },
     xAxis: {
                    type: 'datetime'
                },
    credits: {
        enabled: false
    },
    tooltip: {
                formatter: function () {

                  //get the index number in series of current point
                  var index = this.points[0].series.xData.indexOf(this.x);
                  console.log(index);
                  //trace previous point
                  if (typeof this.points[0].series.data[index-1] !== 'undefined') {
                        // the variable is defined
                        previousValue=this.points[0].series.data[index-1].y;
                    }
                    else{
                      previousValue = this.y;
                    }

                  //ti eixame, ti xasame
                  if (previousValue != 0 ){
                    diff = ((this.y - previousValue)*100)/previousValue;
                  }
                  else {
                    diff = 0 ;
                  }
                  console.log("previous value: "+previousValue+" diff % "+diff);
                    var point = this.points[0];
                    var sign = diff > 0 ? '+' : '';
                    return Highcharts.dateFormat('%A %B %e %Y', this.x) + ':<br/>'+ point.series.name + ' : '+
                    '<b>'+this.y+ " ("+sign+Highcharts.numberFormat(diff, 2) + '%'+")"+'</b>';
                },
                shared: true
            },
    series: [{
        name: 'Resolved Reports',
        data: rate_data,
        color: '#0cd391'
    }]
});
    }
);
