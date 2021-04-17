<html lang="en">
<head>
    <!-- Theme Made By www.w3schools.com - No Copyright -->
    <title>SAINT CTI Tool - CSNA Time Series</title>
    <meta charset="utf-8">

    <!-- Favicons -->
    <link rel="apple-touch-icon-precomposed" sizes="57x57" href="images/apple-touch-icon-57x57.png" />
    <link rel="apple-touch-icon-precomposed" sizes="114x114" href="images/apple-touch-icon-114x114.png" />
    <link rel="apple-touch-icon-precomposed" sizes="72x72" href="images/pple-touch-icon-72x72.png" />
    <link rel="apple-touch-icon-precomposed" sizes="144x144" href="images/apple-touch-icon-144x144.png" />
    <link rel="apple-touch-icon-precomposed" sizes="60x60" href="images/apple-touch-icon-60x60.png" />
    <link rel="apple-touch-icon-precomposed" sizes="120x120" href="images/apple-touch-icon-120x120.png" />
    <link rel="apple-touch-icon-precomposed" sizes="76x76" href="images/apple-touch-icon-76x76.png" />
    <link rel="apple-touch-icon-precomposed" sizes="152x152" href="images/apple-touch-icon-152x152.png" />
    <link rel="icon" type="image/png" href="images/favicon-196x196.png" sizes="196x196" />
    <link rel="icon" type="image/png" href="images/favicon-96x96.png" sizes="96x96" />
    <link rel="icon" type="image/png" href="images/favicon-32x32.png" sizes="32x32" />
    <link rel="icon" type="image/png" href="images/favicon-16x16.png" sizes="16x16" />
    <link rel="icon" type="image/png" href="images/favicon-128.png" sizes="128x128" />
    <meta name="application-name" content="&nbsp;"/>
    <meta name="msapplication-TileColor" content="#FFFFFF" />
    <meta name="msapplication-TileImage" content="images/mstile-144x144.png" />
    <meta name="msapplication-square70x70logo" content="images/mstile-70x70.png" />
    <meta name="msapplication-square150x150logo" content="images/mstile-150x150.png" />
    <meta name="msapplication-wide310x150logo" content="images/mstile-310x150.png" />
    <meta name="msapplication-square310x310logo" content="images/mstile-310x310.png" />

    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <link href="https://fonts.googleapis.com/css?family=Montserrat" rel="stylesheet">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>

<!--    <script src="http://code.highcharts.com/highcharts.js"></script>-->
<!--    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>-->
<!--    <script src="https://code.highcharts.com/modules/data.js"></script>-->
<!--    <script src="https://code.highcharts.com/modules/exporting.js"></script>-->

<!--    <script src="https://code.jquery.com/jquery-3.1.1.min.js"></script>-->
    <script src="https://code.highcharts.com/stock/highstock.js"></script>
    <script src="https://code.highcharts.com/stock/modules/exporting.js"></script>


    <style>

        body {
            font: 20px Montserrat, sans-serif;
            line-height: 1.8;
            color: #f5f6f7;
        }
        p {font-size: 16px;}
        .margin {margin-bottom: 45px;}
        .bg-1 {
            background-color: #e4bb21; /* Yellow */
            color: #ffffff;
        }
        .bg-2 {
            background-color: #e0e0e0; /* Dark Blue */
            color: #ffffff;
        }
        .bg-3 {
            background-color: #ffffff; /* White */
            color: #555555;
        }
        .bg-4 {
            background-color: #2f2f2f; /* Black Gray */
            color: #fff;
        }
        .container-fluid {
            padding-top: 70px;
            padding-bottom: 70px;
        }
        .navbar {
            padding-top: 15px;
            padding-bottom: 15px;
            border: 0;
            border-radius: 0;
            margin-bottom: 0;
            font-size: 12px;
            letter-spacing: 5px;
        }
        .navbar-nav  li a:hover {
            color: #e4bb21 !important;
        }
        /* class added for avoiding disabling the text when clicking inside datepicker */
        .highcharts-range-selector {
            color: black;
        }

        #copyright-link {
            text-decoration: none !important;
        }


        /* unvisited link */
        #copyright-link:link {
            color: #6699ff;
        }

        /* visited link */
        #copyright-link:visited {
            color: #6699ff;
        }

        /* mouse over link */
        #copyright-link:hover {
            color: #E4BB21;
        }

        /* selected link */
        #copyright-link:active {
            color: #6699ff;
        }

        .download {

        }

    </style>

</head>

<body>

<!-- Navbar -->
<nav class="navbar navbar-default">
    <div class="container">
        <div class="navbar-header">
            <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="index.php"><img style="width:60px; padding-bottom: 5px;" src="images/saint_logo_bl.png"></a>
        </div>
        <div class="collapse navbar-collapse" id="myNavbar">
            <ul class="nav navbar-nav navbar-right">
                <li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href="#">CSNA<span class="caret"></span></a>
                    <ul class="dropdown-menu">
                        <li><a href="sna-time-series.php">Time Series Analysis</a></li>
                        <li><a href="sna-bar-plots.php">Categorical Analysis</a></li>
                        <li><a href="timeline-feeds-threats.php">Threats Top Timelines</a></li>
                        <li><a href="timeline-feeds-markets.php">Markets Top Timelines</a></li>
                        <li><a href="wordclouds.php">Wordclouds</a></li>
                    </ul>
                </li>
                <li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href="#">Threats<span class="caret"></span></a>
                    <ul class="dropdown-menu">
                        <li><a href="web-based-attacks.php">Web Based Attacks</a></li>
                        <li><a href="phishing.php">Phishing</a></li>
                        <li><a href="botnets.php">Botnets</a></li>
                        <li><a href="malware.php">Malware</a></li>
                        <li><a href="ddos.php">DDoS</a></li>
                        <li><a href="ransomware.php">Ransomware</a></li>
                    </ul>
                </li>
                <li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href="#">Markets<span class="caret"></span></a>
                    <ul class="dropdown-menu">
                        <li><a href="market-exploits.php">Market Exploits</a></li>
                        <li><a href="bug-bounty-programs.php">Bug Bounty Programs</a></li>
                    </ul>
                </li>
            </ul>
        </div>
    </div>
</nav>

<!--<nav class="navbar navbar-default">-->
<!--    <div class="container">-->
<!--        <div class="navbar-header">-->
<!--            <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">-->
<!--                <span class="icon-bar"></span>-->
<!--                <span class="icon-bar"></span>-->
<!--                <span class="icon-bar"></span>-->
<!--            </button>-->
<!--            <a class="navbar-brand" href="index.php"><img style="width:60px;" src="images/saint_logo_bl.png"></a>-->
<!--        </div>-->
<!--        <div class="collapse navbar-collapse" id="myNavbar">-->
<!--            <ul class="nav navbar-nav navbar-right">-->
<!--                <li><a href="index.php">Time Series</a></li>-->
<!--                <li><a href="output2.php">Bar Plots</a></li>-->
<!--            </ul>-->
<!--        </div>-->
<!--    </div>-->
<!--</nav>-->

<!-- First Container -->
<div class="container-fluid bg-1 text-center">
    <h1 class="margin">Twitter CSNA v.2.1</h1>
    <h2>Time Series Descriptive Analysis</h2>
    <p style="margin: auto; width: 60%; color: #2f2f2f;">The charts below provide real time information on how users react to ongoing events. The information is provided
        as a set of successive observations over a given interval. The information refers to publicly available tweets
        collected at the given interval.  The categorization was based on a set of predefined hashtags of interest.</p>
    <h3><u>Bug Bounties</u></h3>
    <p style="margin: auto; width: 60%; color: #2f2f2f;">Real time information on tweets discussing #bugbounties</p>
    <div id="container1" style="width:100%; height:450px;"></div>
    <div><button type="button" class="btn btn-primary btn-block download" onclick="downloadExcelTimeSeriesBugBounty()">Download Excel Format</button></div>
</div>

<!-- Second Container -->
<div class="container-fluid bg-2 text-center">
    <h3 style="color: black;"><u>Ransomware</u></h3>
    <p style="margin: auto; width: 60%; color: #2f2f2f;">Real time information on tweets discussing #ransomware</p>
    <div id="container2" style="width:100%; height:450px;"></div>
    <div><button type="button" class="btn btn-primary btn-block download" onclick="downloadExcelTimeSeriesRansomware()">Download Excel Format</button></div>
</div>

<!-- Third Container -->
<div class="container-fluid bg-1 text-center">
    <h3><u>Malware</u></h3>
    <p style="margin: auto; width: 60%; color: #2f2f2f;">Real time information on tweets discussing #malware</p>
    <div id="container3" style="width:100%; height:450px;"></div>
    <div><button type="button" class="btn btn-primary btn-block download" onclick="downloadExcelTimeSeriesMalware()">Download Excel Format</button></div>
</div>

<!-- Fourth Container -->
<div class="container-fluid bg-2 text-center">
    <h3 style="color: black;"><u>Trojan</u></h3>
    <p style="margin: auto; width: 60%; color: #2f2f2f;">Real time information related to tweets about #trojanvirus
        (trojan horse | RAT - Remote Access Tool )</p>
    <div id="container4" style="width:100%; height:450px;"></div>
    <div><button type="button" class="btn btn-primary btn-block download" onclick="downloadExcelTimeSeriesTrojan()">Download Excel Format</button></div>
</div>

<!-- Fifth Container -->
<div class="container-fluid bg-1 text-center">
    <h3><u>Botnet</u></h3>
    <p style="margin: auto; width: 60%; color: #2f2f2f;">Real time information on tweets discussing #botnets</p>
    <div id="container5" style="width:100%; height:450px;"></div>
    <div><button type="button" class="btn btn-primary btn-block download" onclick="downloadExcelTimeSeriesBotnet()">Download Excel Format</button></div>
</div>

<!-- Sixth Container -->
<div class="container-fluid bg-2 text-center">
    <h3 style="color: black;"><u>Phishing</u></h3>
    <p style="margin: auto; width: 60%; color: #2f2f2f;">Real time information on tweets discussing #phishing</p>
    <div id="container6" style="width:100%; height:450px;"></div>
    <div><button type="button" class="btn btn-primary btn-block download" onclick="downloadExcelTimeSeriesPhishing()">Download Excel Format</button></div>
</div>

<!-- Sponsors Container (Grid) -->
<div class="container-fluid bg-3 text-center">
    <div class="row">
        <div class="col-sm-4"><img src="images/saint-logo-color.png" style="height: 100px;"></div>
        <div class="col-sm-4"><img src="images/EUflag_yellow_low.jpg" style="height: 100px;"></div>
        <div class="col-sm-4"><img src="images/ctilogo.jpg" style="height: 100px;"></div>
        <br>
    </div>
</div>

<!-- Footer -->
<footer class="container-fluid bg-4 text-center">
    <p>Copyrights 2018. CTI - Developed by <a id="copyright-link" href="https://www.linkedin.com/in/pantelis-tzamalis-03814891/">Pantelis Tzamalis</a></p>
</footer>


<!-- SCRIPTS -->

<script>

    /* CHARTS */
    // BugBounties Chart
    $.getJSON('data_analysis_exports/perdayTimeSeriesBugBounty.json', function (data) {

        // Create the chart
        var chart = Highcharts.stockChart('container1', {

            chart: {
                // height: 400
            },

            title: {
                text: '#BugBounty tweets'
            },

            subtitle: {
                text: 'Click small/large buttons or change window size to test responsiveness'
            },
            xAxis: {
                type: 'datetime'
            },
            yAxis: {
                title: {
                    text: 'Tweets rate'
                },
                min: 0
            },
            plotOptions: {
                area: {
                    fillColor: {
                        linearGradient: {
                            x1: 0,
                            y1: 0,
                            x2: 0,
                            y2: 1
                        },
                        stops: [
                            [0, Highcharts.getOptions().colors[0]],
                            [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                        ]
                    },
                    marker: {
                        radius: 2
                    },
                    lineWidth: 1,
                    states: {
                        hover: {
                            lineWidth: 1
                        }
                    },
                    threshold: null
                }
            },
            rangeSelector: {
                selected: 1,
                inputEnabled: true
            },

            series: [{
                name: 'tweets',
                data: data,
                type: 'area',
                threshold: null,
                tooltip: {
                    valueDecimals: 0
                }
            }],

            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 500
                    },
                    chartOptions: {
                        chart: {
                            height: 300
                        },
                        subtitle: {
                            text: null
                        },
                        navigator: {
                            enabled: false
                        }
                    }
                }]
            }
        });
    });


    // Ransomware chart
    $.getJSON('data_analysis_exports/perdayTimeSeriesRansomware.json', function (data) {

        // Create the chart
        var chart = Highcharts.stockChart('container2', {

            chart: {
                // height: 400
            },

            title: {
                text: '#ransomware tweets'
            },

            subtitle: {
                text: 'Click small/large buttons or change window size to test responsiveness'
            },
            xAxis: {
                type: 'datetime'
            },
            yAxis: {
                title: {
                    text: 'Tweets rate'
                },
                min: 0
            },
            plotOptions: {
                area: {
                    fillColor: {
                        linearGradient: {
                            x1: 0,
                            y1: 0,
                            x2: 0,
                            y2: 1
                        },
                        stops: [
                            [0, Highcharts.getOptions().colors[0]],
                            [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                        ]
                    },
                    marker: {
                        radius: 2
                    },
                    lineWidth: 1,
                    states: {
                        hover: {
                            lineWidth: 1
                        }
                    },
                    threshold: null
                }
            },
            rangeSelector: {
                selected: 1
            },

            series: [{
                name: 'tweets',
                data: data,
                type: 'area',
                threshold: null,
                tooltip: {
                    valueDecimals: 0
                }
            }],

            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 500
                    },
                    chartOptions: {
                        chart: {
                            height: 300
                        },
                        subtitle: {
                            text: null
                        },
                        navigator: {
                            enabled: false
                        }
                    }
                }]
            }
        });
    });

    // Malware chart
    $.getJSON('data_analysis_exports/perdayTimeSeriesMalware.json', function (data) {

        // Create the chart
        var chart = Highcharts.stockChart('container3', {

            chart: {
                // height: 400
            },

            title: {
                text: '#malware tweets'
            },

            subtitle: {
                text: 'Click small/large buttons or change window size to test responsiveness'
            },
            xAxis: {
                type: 'datetime'
            },
            yAxis: {
                title: {
                    text: 'Tweets rate'
                },
                min: 0
            },
            plotOptions: {
                area: {
                    fillColor: {
                        linearGradient: {
                            x1: 0,
                            y1: 0,
                            x2: 0,
                            y2: 1
                        },
                        stops: [
                            [0, Highcharts.getOptions().colors[0]],
                            [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                        ]
                    },
                    marker: {
                        radius: 2
                    },
                    lineWidth: 1,
                    states: {
                        hover: {
                            lineWidth: 1
                        }
                    },
                    threshold: null
                }
            },
            rangeSelector: {
                selected: 1
            },

            series: [{
                name: 'tweets',
                data: data,
                type: 'area',
                threshold: null,
                tooltip: {
                    valueDecimals: 0
                }
            }],

            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 500
                    },
                    chartOptions: {
                        chart: {
                            height: 300
                        },
                        subtitle: {
                            text: null
                        },
                        navigator: {
                            enabled: false
                        }
                    }
                }]
            }
        });
    });

    // Trojan chart
    $.getJSON('data_analysis_exports/perdayTimeSeriesTrojan.json', function (data) {

        // Create the chart
        var chart = Highcharts.stockChart('container4', {

            chart: {
                // height: 400
            },

            title: {
                text: '#trojan tweets'
            },

            subtitle: {
                text: 'Click small/large buttons or change window size to test responsiveness'
            },
            xAxis: {
                type: 'datetime'
            },
            yAxis: {
                title: {
                    text: 'Tweets rate'
                },
                min: 0
            },
            plotOptions: {
                area: {
                    fillColor: {
                        linearGradient: {
                            x1: 0,
                            y1: 0,
                            x2: 0,
                            y2: 1
                        },
                        stops: [
                            [0, Highcharts.getOptions().colors[0]],
                            [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                        ]
                    },
                    marker: {
                        radius: 2
                    },
                    lineWidth: 1,
                    states: {
                        hover: {
                            lineWidth: 1
                        }
                    },
                    threshold: null
                }
            },
            rangeSelector: {
                selected: 1
            },

            series: [{
                name: 'tweets',
                data: data,
                type: 'area',
                threshold: null,
                tooltip: {
                    valueDecimals: 0
                }
            }],

            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 500
                    },
                    chartOptions: {
                        chart: {
                            height: 300
                        },
                        subtitle: {
                            text: null
                        },
                        navigator: {
                            enabled: false
                        }
                    }
                }]
            }
        });
    });

    // Botnet chart
    $.getJSON('data_analysis_exports/perdayTimeSeriesBotnet.json', function (data) {

        // Create the chart
        var chart = Highcharts.stockChart('container5', {

            chart: {
                // height: 400
            },

            title: {
                text: '#botnet tweets'
            },

            subtitle: {
                text: 'Click small/large buttons or change window size to test responsiveness'
            },
            xAxis: {
                type: 'datetime'
            },
            yAxis: {
                title: {
                    text: 'Tweets rate'
                },
                min: 0
            },
            plotOptions: {
                area: {
                    fillColor: {
                        linearGradient: {
                            x1: 0,
                            y1: 0,
                            x2: 0,
                            y2: 1
                        },
                        stops: [
                            [0, Highcharts.getOptions().colors[0]],
                            [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                        ]
                    },
                    marker: {
                        radius: 2
                    },
                    lineWidth: 1,
                    states: {
                        hover: {
                            lineWidth: 1
                        }
                    },
                    threshold: null
                }
            },
            rangeSelector: {
                selected: 1
            },

            series: [{
                name: 'tweets',
                data: data,
                type: 'area',
                threshold: null,
                tooltip: {
                    valueDecimals: 0
                }
            }],

            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 500
                    },
                    chartOptions: {
                        chart: {
                            height: 300
                        },
                        subtitle: {
                            text: null
                        },
                        navigator: {
                            enabled: false
                        }
                    }
                }]
            }
        });
    });



    // Phishing chart
    $.getJSON('data_analysis_exports/perdayTimeSeriesPhishing.json', function (data) {

        // Create the chart
        var chart = Highcharts.stockChart('container6', {

            chart: {
                // height: 400
            },

            title: {
                text: '#phishing tweets'
            },

            subtitle: {
                text: 'Click small/large buttons or change window size to test responsiveness'
            },
            xAxis: {
                type: 'datetime'
            },
            yAxis: {
                title: {
                    text: 'Tweets rate'
                },
                min: 0
            },
            plotOptions: {
                area: {
                    fillColor: {
                        linearGradient: {
                            x1: 0,
                            y1: 0,
                            x2: 0,
                            y2: 1
                        },
                        stops: [
                            [0, Highcharts.getOptions().colors[0]],
                            [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                        ]
                    },
                    marker: {
                        radius: 2
                    },
                    lineWidth: 1,
                    states: {
                        hover: {
                            lineWidth: 1
                        }
                    },
                    threshold: null
                }
            },
            rangeSelector: {
                selected: 1
            },

            series: [{
                name: 'tweets',
                data: data,
                type: 'area',
                threshold: null,
                tooltip: {
                    valueDecimals: 0
                }
            }],

            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 500
                    },
                    chartOptions: {
                        chart: {
                            height: 300
                        },
                        subtitle: {
                            text: null
                        },
                        navigator: {
                            enabled: false
                        }
                    }
                }]
            }
        });
    });



    /* Download Excel Format - CSV */
    // BugBoutny
    function downloadExcelTimeSeriesBugBounty() {
        location.href = "data_analysis_exports/perdayTimeSeriesBugBounty.csv";
    }

    // Ransomware
    function downloadExcelTimeSeriesRansomware() {
        location.href = "data_analysis_exports/perdayTimeSeriesRansomware.csv";
    }

    // Malware
    function downloadExcelTimeSeriesMalware() {
        location.href = "data_analysis_exports/perdayTimeSeriesMalware.csv";
    }

    // Trojan
    function downloadExcelTimeSeriesTrojan() {
        location.href = "data_analysis_exports/perdayTimeSeriesTrojan.csv";
    }

    // Botnet
    function downloadExcelTimeSeriesBotnet() {
        location.href = "data_analysis_exports/perdayTimeSeriesBotnet.csv";
    }

    // Phishing
    function downloadExcelTimeSeriesPhishing() {
        location.href = "data_analysis_exports/perdayTimeSeriesPhishing.csv";
    }


</script>

</body>

</html>