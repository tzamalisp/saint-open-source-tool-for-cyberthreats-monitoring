<html lang="en">
<head>
    <!-- Theme Made By www.w3schools.com - No Copyright -->
    <title>SAINT CTI Tool - CSNA Bar Plots</title>
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

        <script src="http://code.highcharts.com/highcharts.js"></script>
        <script src="https://code.highcharts.com/modules/data.js"></script>
        <script src="https://code.highcharts.com/modules/exporting.js"></script>

    <!--    <script src="https://code.jquery.com/jquery-3.1.1.min.js"></script>-->
<!--    <script src="https://code.highcharts.com/stock/highstock.js"></script>-->
<!--    <script src="https://code.highcharts.com/stock/modules/exporting.js"></script>-->


    <style>

        body {
            font: 20px Montserrat, sans-serif;
            line-height: 1.8;
            /*color: #f5f6f7;*/
        }
        p {font-size: 16px;}
        .margin {margin-bottom: 45px;}
        .bg-1 {
            background-color: #e4bb21; /* Green */
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

        /*a {*/
            /*text-decoration: none !important;*/
        /*}*/

        /*p {*/
            /*text-decoration: none !important;*/
        /*}*/

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

        .btn-block {
            display: inline-block;
        }

    </style>

</head>

<body>
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

    <!-- First Container -->
    <div class="container-fluid bg-1 text-center">
        <h1 class="margin">Twitter CSNA v.2.1</h1>
        <h2>Categorical Analysis</h2>
        <p style="margin: auto; width: 60%; color: #2f2f2f;">The charts below identify the 10 most frequently used terms
            hashtags, mentions, and terms in twitter users’ posts for the Cybersecurity Markets and Cyberthreats
            categories.</p>
        <h3>Most frequent used Hashtags, Mentions and Terms over the last 7 days</h3>
        <div class="row">
            <div class="col-sm-6">
                <h3><u>Hashtags Frequency - Cybersecurity Markets<u></h3>
                <p style="margin: auto; width: 60%; color: #2f2f2f; text-decoration: none !important;">Most frequent hashtags for
                    the Cybersecurity Market dataset</p>
                <div id="container1" style="width:100%; height:400px;"></div>
                <div><button type="button" class="btn btn-primary btn-block download" onclick="downloadExcelBarPlotsHashtagsSNA1()">Download Excel Format</button></div>
            </div>
            <div class="col-sm-6">
                <h3><u>Hashtags Frequency - Cyberthreats</u></h3>
                <p style="margin: auto; width: 60%; color: #2f2f2f;">Most frequent hashtags for the Cyberthreats
                    dataset</p>
                <div id="container2" style="width:100%; height:400px;"></div>
                <div><button type="button" class="btn btn-primary btn-block download" onclick="downloadExcelBarPlotsHashtagsSNA2()">Download Excel Format</button></div>
            </div>
        </div>
    </div>

    <!-- Second Container -->
    <div class="container-fluid bg-2 text-center">
        <div class="row">
            <div class="col-sm-6">
                <h3 style="color: black;"><u>Mentions Frequency - Cybersecurity Markets<u></h3>
                <p style="margin: auto; width: 60%; color: #2f2f2f;">Most influential users identified in the Markets
                    dataset</p>
                <div id="container3" style="width:100%; height:400px;"></div>
                <div><button type="button" class="btn btn-primary btn-block download" onclick="downloadExcelBarPlotsMentionsSNA1()">Download Excel Format</button></div>
            </div>
            <div class="col-sm-6">
                <h3 style="color: black;"><u>Mentions Frequency - Cyberthreats</u></h3>
                <p style="margin: auto; width: 60%; color: #2f2f2f;">Most influential users identified in the
                    Cyberthreats dataset</p>
                <div id="container4" style="width:100%; height:400px;"></div>
                <div><button type="button" class="btn btn-primary btn-block download" onclick="downloadExcelBarPlotsMentionsSNA2()">Download Excel Format</button></div>
            </div>
        </div>
    </div>

    <!-- Third Container -->
    <div class="container-fluid bg-1 text-center">
        <div class="row">
            <div class="col-sm-6">
                <h3><u>Terms Frequency - Cybersecurity Markets<u></h3>
                <p style="margin: auto; width: 60%; color: #2f2f2f;">Most frequent words used in the main body (text) of
                    the tweets on the Cybersecurity Markets dataset</p>
                <div id="container5" style="width:100%; height:400px;"></div>
                <div><button type="button" class="btn btn-primary btn-block download" onclick="downloadExcelBarPlotsTermsSNA1()">Download Excel Format</button></div>
            </div>
            <div class="col-sm-6">
                <h3><u>Terms Frequency - Cyberthreats</u></h3>
                <p style="margin: auto; width: 60%; color: #2f2f2f;">Most frequent words used in the main body (text) of
                    the tweets on the Cyberthreats dataset </p>
                <div id="container6" style="width:100%; height:400px;"></div>
                <div><button type="button" class="btn btn-primary btn-block download" onclick="downloadExcelBarPlotsTermsSNA2()">Download Excel Format</button></div>
            </div>
        </div>
    </div>

    <!-- Fourth Container (Grid) -->
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

        /* Hashtags Markets */
        $.getJSON('data_analysis_exports/hashtagsMarkets.json', function (data) {

            // Create the chart
            var chart = Highcharts.chart('container1', {
                chart: {
                    type: 'column',
                    zoomType: 'x',
                    panning: true,
                    panKey: 'shift'
                },
                title: {
                    text: 'Twitter Hashtags frequency: Markets'
                },
                subtitle: {
                    text: document.ontouchstart === undefined ?
                        'Click and drag to zoom in. Hold down shift key to pan.' : 'Pinch the chart to zoom in'
                },
                xAxis: {
                    type: 'category',
                    labels: {
                        rotation: -45,
                        style: {
                            fontSize: '13px',
                            fontFamily: 'Verdana, sans-serif'
                        }
                    }
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'Number of hashtags'
                    }
                },
                legend: {
                    enabled: false
                },
                tooltip: {
                    pointFormat: 'Frequency: <b>{point.y:.0f} hashtags</b>'
                },
                series: [{
                    name: 'Population',
                    data:
                    data
                    ,
                    dataLabels: {
                        enabled: true,
                        rotation: -90,
                        color: '#A52A2A',
                        align: 'right',
                        format: '{point.y:.0f}', // one decimal
                        y: 10, // 10 pixels down from the top
                        style: {
                            fontSize: '9px',
                            fontFamily: 'Verdana, sans-serif'
                        }
                    }
                }]
            });

        });

        /* Hashtags Malware */
        $.getJSON('data_analysis_exports/hashtagsThreats.json', function (data) {

            // Create the chart
            var chart = Highcharts.chart('container2', {
                chart: {
                    type: 'column',
                    zoomType: 'x',
                    panning: true,
                    panKey: 'shift'
                },
                title: {
                    text: 'Twitter Hashtags frequency: Threats'
                },
                subtitle: {
                    text: document.ontouchstart === undefined ?
                        'Click and drag to zoom in. Hold down shift key to pan.' : 'Pinch the chart to zoom in'
                },
                xAxis: {
                    type: 'category',
                    labels: {
                        rotation: -45,
                        style: {
                            fontSize: '13px',
                            fontFamily: 'Verdana, sans-serif'
                        }
                    }
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'Number of hashtags'
                    }
                },
                legend: {
                    enabled: false
                },
                tooltip: {
                    pointFormat: 'Frequency: <b>{point.y:.0f} hashtags</b>'
                },
                series: [{
                    name: 'Population',
                    data:
                    data
                    ,
                    dataLabels: {
                        enabled: true,
                        rotation: -90,
                        color: '#A52A2A',
                        align: 'right',
                        format: '{point.y:.0f}', // one decimal
                        y: 10, // 10 pixels down from the top
                        style: {
                            fontSize: '9px',
                            fontFamily: 'Verdana, sans-serif'
                        }
                    }
                }]
            });

        });

        /* Mentions Markets */
        $.getJSON('data_analysis_exports/mentionsMarkets.json', function (data) {

            // Create the chart
            var chart = Highcharts.chart('container3', {
                chart: {
                    type: 'column',
                    zoomType: 'x',
                    panning: true,
                    panKey: 'shift'
                },
                title: {
                    text: 'Twitter User Mentions frequency: Markets'
                },
                subtitle: {
                    text: document.ontouchstart === undefined ?
                        'Click and drag to zoom in. Hold down shift key to pan.' : 'Pinch the chart to zoom in'
                },
                xAxis: {
                    type: 'category',
                    labels: {
                        rotation: -45,
                        style: {
                            fontSize: '13px',
                            fontFamily: 'Verdana, sans-serif'
                        }
                    }
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'Number of users'
                    }
                },
                legend: {
                    enabled: false
                },
                tooltip: {
                    pointFormat: 'Frequency: <b>{point.y:.0f} users</b>'
                },
                series: [{
                    name: 'Population',
                    data:
                    data
                    ,
                    dataLabels: {
                        enabled: true,
                        rotation: -90,
                        color: '#A52A2A',
                        align: 'right',
                        format: '{point.y:.0f}', // one decimal
                        y: 10, // 10 pixels down from the top
                        style: {
                            fontSize: '9px',
                            fontFamily: 'Verdana, sans-serif'
                        }
                    }
                }]
            });
        });

        /* Mentions Malware */
        $.getJSON('data_analysis_exports/mentionsThreats.json', function (data) {

            // Create the chart
            var chart = Highcharts.chart('container4', {
                chart: {
                    type: 'column',
                    zoomType: 'x',
                    panning: true,
                    panKey: 'shift'
                },
                title: {
                    text: 'Twitter User Mentions frequency: Threats'
                },
                subtitle: {
                    text: document.ontouchstart === undefined ?
                        'Click and drag to zoom in. Hold down shift key to pan.' : 'Pinch the chart to zoom in'
                },
                xAxis: {
                    type: 'category',
                    labels: {
                        rotation: -45,
                        style: {
                            fontSize: '13px',
                            fontFamily: 'Verdana, sans-serif'
                        }
                    }
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'Number of users'
                    }
                },
                legend: {
                    enabled: false
                },
                tooltip: {
                    pointFormat: 'Frequency: <b>{point.y:.0f} users</b>'
                },
                series: [{
                    name: 'Population',
                    data:
                    data
                    ,
                    dataLabels: {
                        enabled: true,
                        rotation: -90,
                        color: '#A52A2A',
                        align: 'right',
                        format: '{point.y:.0f}', // one decimal
                        y: 10, // 10 pixels down from the top
                        style: {
                            fontSize: '9px',
                            fontFamily: 'Verdana, sans-serif'
                        }
                    }
                }]
            });
        });


        /* Terms Markets */
        $.getJSON('data_analysis_exports/termsMarkets.json', function (data) {

            // Create the chart
            var chart = Highcharts.chart('container5', {
                chart: {
                    type: 'column',
                    zoomType: 'x',
                    panning: true,
                    panKey: 'shift'
                },
                title: {
                    text: 'Twitter Terms frequency: Markets'
                },
                subtitle: {
                    text: document.ontouchstart === undefined ?
                        'Click and drag to zoom in. Hold down shift key to pan.' : 'Pinch the chart to zoom in'
                },
                xAxis: {
                    type: 'category',
                    labels: {
                        rotation: -45,
                        style: {
                            fontSize: '13px',
                            fontFamily: 'Verdana, sans-serif'
                        }
                    }
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'Number of terms'
                    }
                },
                legend: {
                    enabled: false
                },
                tooltip: {
                    pointFormat: 'Frequency: <b>{point.y:.0f} terms</b>'
                },
                series: [{
                    name: 'Population',
                    data:
                    data
                    ,
                    dataLabels: {
                        enabled: true,
                        rotation: -90,
                        color: '#A52A2A',
                        align: 'right',
                        format: '{point.y:.0f}', // one decimal
                        y: 10, // 10 pixels down from the top
                        style: {
                            fontSize: '9px',
                            fontFamily: 'Verdana, sans-serif'
                        }
                    }
                }]
            });

        });

        /* Terms Malware */
        $.getJSON('data_analysis_exports/termsThreats.json', function (data) {

            // Create the chart
            var chart = Highcharts.chart('container6', {
                chart: {
                    type: 'column',
                    zoomType: 'x',
                    panning: true,
                    panKey: 'shift'
                },
                title: {
                    text: 'Twitter Terms frequency:Threats'
                },
                subtitle: {
                    text: document.ontouchstart === undefined ?
                        'Click and drag to zoom in. Hold down shift key to pan.' : 'Pinch the chart to zoom in'
                },
                xAxis: {
                    type: 'category',
                    labels: {
                        rotation: -45,
                        style: {
                            fontSize: '13px',
                            fontFamily: 'Verdana, sans-serif'
                        }
                    }
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'Number of terms'
                    }
                },
                legend: {
                    enabled: false
                },
                tooltip: {
                    pointFormat: 'Frequency: <b>{point.y:.0f} terms</b>'
                },
                series: [{
                    name: 'Population',
                    data:
                    data
                    ,
                    dataLabels: {
                        enabled: true,
                        rotation: -90,
                        color: '#A52A2A',
                        align: 'right',
                        format: '{point.y:.0f}', // one decimal
                        y: 10, // 10 pixels down from the top
                        style: {
                            fontSize: '9px',
                            fontFamily: 'Verdana, sans-serif'
                        }
                    }
                }]
            });

        });


        /* Download Excel Format - CSV */
        function downloadExcelBarPlotsHashtagsSNA1() {
            location.href = "data_analysis_exports/hashtagsMarkets.csv";
        }

        function downloadExcelBarPlotsHashtagsSNA2() {
            location.href = "data_analysis_exports/hashtagsThreats.csv";
        }

        function downloadExcelBarPlotsMentionsSNA1() {
            location.href = "data_analysis_exports/mentionsMarkets.csv";
        }

        function downloadExcelBarPlotsMentionsSNA2() {
            location.href = "data_analysis_exports/mentionsThreats.csv";
        }

        function downloadExcelBarPlotsTermsSNA1() {
            location.href = "data_analysis_exports/termsMarkets.csv";
        }

        function downloadExcelBarPlotsTermsSNA2() {
            location.href = "data_analysis_exports/termsThreats.csv";
        }


    </script>

</body>

</html>