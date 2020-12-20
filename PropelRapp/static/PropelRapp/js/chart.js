$(document).ready(function () {
    "use strict";
    // toat popup js


    //ct-visits
    new Chartist.Line('#ct-visits', {
        labels: ['2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015'],
        series: [
   [5, 2, 7, 4, 5, 3, 5, 4]
   , [2, 5, 2, 6, 2, 5, 2, 4]
 ]
    }, {
        top: 0,
        low: 1,
        showPoint: true,
        fullWidth: true,
        plugins: [
   Chartist.plugins.tooltip()
 ],
        axisY: {
            labelInterpolationFnc: function (value) {
                return (value / 1) + 'k';
            }
        },
        showArea: true
    });
    // counter
    $(".counter").counterUp({
        delay: 100,
        time: 1200
    });

    var sparklineLogin = function () {
        $('#sparklinedash').sparkline([0, 5, 6, 10, 9, 12, 4, 9], {
             type: 'bar',
            height: '80',
             barWidth: '10',
            // resize: true,
            barSpacing: '5',
            // barColor: '#7ace4c'
            data:{
                labels:['a', 'b', 'S', 'L', 'C', 'N'],
                datasets:[{
                  label:'Population',
                  
                  //backgroundColor:'green',
                  backgroundColor:[
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(153, 102, 255, 0.6)',
                    'rgba(255, 159, 64, 0.6)',
                    'rgba(255, 99, 132, 0.6)'
                  ],
                  borderWidth:1,
                  borderColor:'#777',
                  hoverBorderWidth:3,
                  hoverBorderColor:'#000'
                }]
              }
            
        });
        $('#sparklinedash2').sparkline([0, 5, 6, 10, 9, 12, 4, 9], {
            type: 'bar',
            height: '30',
            barWidth: '4',
            resize: true,
            barSpacing: '5',
            barColor: '#7460ee',
            options = {
                scales: {
                    xAxes: [{
                        gridLines: {
                            offsetGridLines: true
                        }
                    }]
                }
            }
        });
        $('#sparklinedash3').sparkline([0, 5, 6, 10, 9, 12, 4, 9], {
            type: 'bar',
            height: '30',
            barWidth: '4',
            resize: true,
            barSpacing: '5',
            barColor: '#11a0f8'
        });
        $('#sparklinedash4').sparkline([0, 5, 6, 10, 9, 12, 4, 9], {
            type: 'bar',
            height: '30',
            barWidth: '4',
            resize: true,
            barSpacing: '5',
            barColor: '#f33155'
        });
    }
    var sparkResize;
    $(window).on("resize", function (e) {
        clearTimeout(sparkResize);
        sparkResize = setTimeout(sparklineLogin, 500);
    });
    sparklineLogin();
});
