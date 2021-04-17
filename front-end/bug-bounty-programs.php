<html lang="en">
<head>
    <!-- Theme Made By www.w3schools.com - No Copyright -->
    <title>SAINT CTI Tool</title>
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


    <!--    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>-->
    <!--    <script src="https://code.highcharts.com/modules/data.js"></script>-->
    <!--    <script src="https://code.highcharts.com/modules/exporting.js"></script>-->

    <!--    <script src="https://code.jquery.com/jquery-3.1.1.min.js"></script>-->
    <script src="https://code.highcharts.com/stock/highstock.js"></script>
    <script src="https://code.highcharts.com/stock/modules/exporting.js"></script>
    <script src="https://code.highcharts.com/stock/modules/export-data.js"></script>


    <style>

        body {
            font: 20px Montserrat, sans-serif;
            line-height: 1.8;
            color: #f5f6f7;
        }
        p {font-size: 16px;}
        .margin {margin-bottom: 45px;}
        .bg-1 {
            background-color: #e4bb21; /* Deep Yellow */
            color: #ffffff;
        }
        .bg-2 {
            background-color: #e0e0e0; /* Light Grey */
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

        .description {
            color: #444444;
            text-align: justify;
        }

        .descriptionHeader {
            color: black;
        }

        .buttonDataset {
            white-space: normal;
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
    <h1 class="margin">Clearnet Crawler Tool - Bug Bounty Programs</h1>
    <h4>Feed: HackerOne - https://www.hackerone.com/</h4>
    <p style="margin: auto; width: 60%; color: #2f2f2f;">HackerOne is a vulnerability coordination and bug bounty
        platform that connects businesses with penetration testers and cybersecurity researchers.</p>
    <h3><u>Dataset</u></h3>
    <p>Download the dataset from the last instance of the feed that is stored in our database, simply by clicking the button below.</p>
    <div><button type="button" class="btn btn-default buttonDataset" onclick="downloadExcelDatasetBugBounties()">Download Bug Bounties Dataset</button></div>
    <hr>
    <h3><u>Bug Bounty programs announced in total by specified companies</u></h3>
    <p style="margin: auto; width: 60%; color: #2f2f2f;">On this graph, each day's recorded number of resolved reports that exist in the
        HackerOne platform for five companies is displayed. Each record corresponds to the number of resolved reports that were stored into the database
        until that certain day. Inside the parentheses, the percentage of stored resolved reports change is displayed. For example, in case
        a company had 632 resolved reports since the first day of records and now there are 655, then there is a 3,64% increase of
        the stored resolved reports for that company.<br>
        Parentheses percentage value: <i>100 * ( (X2 - X1) / X1 )</i><br>
    where:<br>
        X2: today's total counted resolved reports<br>
        X1: first total recorded resolved reports
    </p>
    <div id="container1" style="width:100%; height:450px;"></div>
    <div><button type="button" class="btn btn-primary btn-block download" onclick="downloadExcelperdayBugBountiesCount()">Download Excel Format</button></div>
    <br>
<!--    <div id="firstCompanyIDCount" style="color: black"></div>-->
<!--    <div id="secondCompanyIDCount" style="color: black"></div>-->
<!--    <div id="thirdCompanyIDCount" style="color: black"></div>-->
<!--    <div id="fourthCompanyIDCount" style="color: black"></div>-->
<!--    <div id="fifthCompanyIDCount" style="color: black"></div>-->
</div>


<!-- Second Container -->
<div class="container-fluid bg-2 text-center">
    <h3 style="color: black;"><u>Today's Minimum Bounty of specified companies</u></h3>
    <h4 style="color: black">Feed: https://www.hackerone.com/</h4>
    <p style="margin: auto; width: 60%; color: #2f2f2f;">The graph below shows for each day the Minimum bounty price for each of the specified companies.</p>
    <div id="container2" style="width:100%; height:450px;"></div>
    <div><button type="button" class="btn btn-primary btn-block download" onclick="downloadExcelperdayBugBountiesMinimum()">Download Excel Format</button></div>
</div>

<!-- Third Container - rates for each of five companies-->
<div class="container-fluid bg-2 text-center">
    <h3 style="color: black;"><u>Change rate of added/removed resolved reports since the first day of recorded resolved reports for specified companies</u></h3>
    <h4 style="color: black">Feed: https://www.hackerone.com/</h4>
    <p style="margin: auto; width: 60%; color: #2f2f2f;">Based on the first chart values for each company, this chart depicts the daily number of added/removed resolved reports,
        as well as the rate of that change based on the first ever calculated by CTI values of added/removed reports, for each
        of the specified companies. This is the number of resolved reports added/removed day by day and it is calculated by subtracting
        the previous day's total reports from the current day's reports. The percentage of that change is also calculated as shown below and displayed
        inside the parentheses. On this chart several occasions are observed.<br>
        <ul style="margin: auto; width: 60%; color: #2f2f2f; font-size: 15px;">
            <li>In case a company has added 2 resolved reports in one day and the other day 5 resolved reports were added, then a higher increment
                rate is displayed.</li>
            <li>The increment percentage is calculated with respect to the first recorded difference between the total resolved reports
                of the starting point day and the previous one.</li>
            <li>In case a company does not add any resolved reports in a day, then the increment is zero.
                In that case, the increment percentage is -100% whichever the previous daily record was.</li>
        </ul>
    </p>
    <br>
    <div style="margin: auto; width: 60%; color: #2f2f2f;">
    Parentheses percentage value: ( ( (Xt - Xy) - (X0 - X0-1) ) / (X0 - X0-1) ) * 100<br>
    Based on the first diagram, where:<br>
    Xt: X today --> today's total recorded resolved reports<br>
    Xy: X yesterday --> yesterday's total recorded resolved reports<br>
    X0: the first recorded value of total resolved reports that is defined as starting point<br>
    X0-1: the previous of the starting point recorded value of total resolved reports<br>
    Note: The starting point is set when the calculation of (X0 - X0-1) is different from zero.<br>
        <br>
    </div>
    <div id="container3" style="width:100%; height:450px;"></div>
    <!-- <div><button type="button" class="btn btn-primary btn-block download" onclick="downloadExcelperdayBugBountiesMinimum()">Download Excel Format</button></div> -->
</div>

<!-- Fourth Container - rates for each of five companies-->
<div class="container-fluid bg-2 text-center">
    <h3 style="color: black;"><u>Daily change rate percentage(%) of recorded resolved reports for specified companies</u></h3>
    <h4 style="color: black">Feed: https://www.hackerone.com/</h4>
    <p style="margin: auto; width: 60%; color: #2f2f2f;">This chart displays almost the same information with the previous one,
        however, the change rate is calculated with respect to the previous day's calculated number of recorded resolved reports. Furthermore,
        in case no bug was added the day previously (increment record was zero) then the next record change rate
        would be zero, whatever the number of resolved reports added are.</p>
    <br>
    <div style="margin: auto; width: 60%; color: #2f2f2f;">
        Parentheses percentage value: ( ( (Xt - Xy) - (Xy - Xy-1) ) / (Xy - Xy-1) ) * 100<br>
        Based on the first diagram, where:<br>
        Xt: X today --> today's total recorded resolved reports<br>
        Xy: X yesterday --> yesterday's total recorded resolved reports<br>
        Xy-1: the day's previous of yesterday's recorded value of total resolved reports<br>
        <br>
    </div>
    <div id="container4" style="width:100%; height:450px;"></div>
    <!-- <div><button type="button" class="btn btn-primary btn-block download" onclick="downloadExcelperdayBugBountiesMinimum()">Download Excel Format</button></div> -->
</div>

<!-- Fifth Container - rates for each of five companies-->
<div class="container-fluid bg-2 text-center">
    <p style="margin: 40px; color: #2f2f2f; text-align: justify;">The next two charts display the increment/decrement of
        all the stored resolved reports from all the companies that collaborate with HackerOne. This is the number of all the stored
        resolved reports added day by day and is calculated by subtracting the previous day sum of resolved reports from the current day sum of
        resolved reports recorded for all the companies. The increment/decrement change percentage is displayed in parentheses here
        too. On the following chart, the increment/decrement percentage is calculated with respect to the first recorded
        value that is stored into the CTI's database, while on the last chart, the increment/decrement change rate is
        calculated with respect to the previous day's calculated number of recorded resolved reports.</p>
    <br>
    <br>
    <h3 style="color: black;"><u>Daily released resolved reports change rate in respect to the first recorded value of calculated resolved reports</u></h3>
    <h4 style="color: black">Feed: https://www.hackerone.com/</h4>
    <p style="margin: auto; width: 60%; color: #2f2f2f;">Similarly to the 3rd chart, this plot shows the number of the added/removed resolved reports for <b>all the companies</b> which keep activity in
        HackerOne's platform, day by day. However, a kind of Learning has been adopted here as the mean of the resolved reports has been calculated from 25th of May
        where the first record has been stored into the CTI's database until the 25th of September. Thus, in parentheses someone can see the added/removed resolved
        reports rate percentage (second derivative of resolved reports
        number) with respect to the "system-learning" calculated value of the number of the resolved reports into the CTI's database.</p>
    <p style="margin: auto; width: 60%; color: #2f2f2f;" id="mean_val_par"></p>
    <div id="container5" style="width:100%; height:450px;"></div>
    <!-- <div><button type="button" class="btn btn-primary btn-block download" onclick="downloadExcelperdayBugBountiesMinimum()">Download Excel Format</button></div> -->
</div>

<!-- Sixth Container - rates for each of five companies-->
<div class="container-fluid bg-2 text-center">
    <h3 style="color: black;"><u>Daily released resolved reports change rate percentage(%)</u></h3>
    <h4 style="color: black">Feed: https://www.hackerone.com/</h4>
    <p style="margin: auto; width: 60%; color: #2f2f2f;">Similarly to the 4th chart, this diagram shows the number of the added/removed resolved reports <b>for all companies</b> which keep activity in
        HackerOne's platform, day by day. In parentheses someone can see the added/removed resolved reports rate percentage (second derivative of resolved reports
        number) with respect to the previous day's recorded value of the added/removed resolved reports.
    </p>
    <div id="container6" style="width:100%; height:450px;"></div>
    <!-- <div><button type="button" class="btn btn-primary btn-block download" onclick="downloadExcelperdayBugBountiesMinimum()">Download Excel Format</button></div> -->
</div>

<!-- Second Container -->
<!--<div class="container-fluid bg-2 text-center">-->
<!--    <h3 style="color: black;"><u>Bug Bounties - Minimum Bounty Comparison </u></h3>-->
<!--    <div id="container2" style="width:100%; height:450px;"></div>-->
<!--    <div><button type="button" class="btn btn-primary btn-block download" onclick="downloadExcelperdayBugBountiesMinimum()">Download Excel Format</button></div>-->
<!--    <br>-->
<!--    <div id="firstCompanyIDBounty" style="color: black"></div>-->
<!--    <div id="secondCompanyIDBounty" style="color: black"></div>-->
<!--    <div id="thirdCompanyIDBounty" style="color: black"></div>-->
<!--    <div id="fourthCompanyIDBounty" style="color: black"></div>-->
<!--    <div id="fifthCompanyIDBounty" style="color: black"></div>-->
<!--</div>-->

<!-- Third Container (Grid) -->
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
<!-- every day count script -->
<script>

    function loadJSON(path, callback) {

        var xobj = new XMLHttpRequest();
        xobj.overrideMimeType("application/json");
        xobj.open('GET', path, true); // Replace 'my_data' with the path to your file
        xobj.onreadystatechange = function () {
              if (xobj.readyState == 4 && xobj.status == "200") {
                // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
                callback(xobj.responseText);
              }
        };
        xobj.send(null);
    }

    /* BUG COUNT */
    var seriesOptions = [],
    seriesCounter = 0,
    names = ["Yahoo!", "Shopify", "Uber", "Twitter", "Slack"];

    /**
     * Create the chart when all data is loaded
     * @returns {undefined}
     */
    function createChart() {

        Highcharts.stockChart('container1', {

            rangeSelector: {
                selected: 1
            },

            yAxis: {
                labels: {
                    formatter: function () {
                        return (this.value > 0 ? ' + ' : '') + this.value + '%';
                    }
                },
                plotLines: [{
                    value: 0,
                    width: 2,
                    color: 'silver'
                }]
            },

            plotOptions: {
                series: {
                    compare: 'percent',
                    showInNavigator: true
                }
            },

            tooltip: {
                pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y:.0f}</b> ({point.change}%)<br/>',
                valueDecimals: 2,
                split: true
            },

            series: seriesOptions
        });
    }

    $.each(names, function (i, name) {

        $.getJSON('markets/perday-bug-bounties-count-' + name + '.json', function (data) {
            seriesOptions[i] = {
                name: name,
                data: data
            };

            // As we're loading the data asynchronously, we don't know what order it will arrive. So
            // we keep a counter and create the chart when all the data is loaded.
            seriesCounter += 1;

            if (seriesCounter === names.length) {
                createChart();
            }
        });
    });


    /* BUG BOUNTIES */

    // var seriesOptionsMinimum = [],
    // seriesCounterMinimum = 0,
    // namesMinimum = ["Yahoo!", "Shopify", "Uber", "Twitter", "Slack"];
    //
    // function createChartMinimum() {
    //
    //     Highcharts.stockChart('container2', {
    //
    //         rangeSelector: {
    //             selected: 4
    //         },
    //
    //         yAxis: {
    //             labels: {
    //                 formatter: function () {
    //                     return (this.value > 0 ? ' + ' : '') + this.value + '%';
    //                 }
    //             },
    //             plotLines: [{
    //                 value: 0,
    //                 width: 2,
    //                 color: 'silver'
    //             }]
    //         },
    //
    //         plotOptions: {
    //             series: {
    //                 compare: 'percent',
    //                 showInNavigator: true
    //             }
    //         },
    //
    //         tooltip: {
    //             pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',
    //             valueDecimals: 2,
    //             split: true
    //         },
    //
    //         series: seriesOptionsMinimum
    //     });
    // }
    //
    // $.each(namesMinimum, function (i, name) {
    //
    //     $.getJSON('markets/perday-bug-bounties-minimum-' + name + '.json', function (data) {
    //
    //         seriesOptionsMinimum[i] = {
    //             name: name,
    //             data: data
    //         };
    //
    //         // As we're loading the data asynchronously, we don't know what order it will arrive. So
    //         // we keep a counter and create the chart when all the data is loaded.
    //         seriesCounterMinimum += 1;
    //
    //         if (seriesCounterMinimum === namesMinimum.length) {
    //             createChartMinimum();
    //         }
    //     });
    // });

    // Download Bug Bounty Programs (Hackerone) Dataset
    function downloadExcelDatasetBugBounties() {
        location.href = "http://150.140.193.156:2080/saint/markets/dataset-bug-bounties.zip";
    }

    function downloadExcelperdayBugBountiesCount() {
        location.href = "http://150.140.193.156:2080/saint/markets/perday-bug-bounties-count.zip";
    }

    function downloadExcelperdayBugBountiesMinimum() {
        location.href = "http://150.140.193.156:2080/saint/markets/perday-bug-bounties-minimum.zip";
    }



</script>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script>


    $.getJSON('markets/bug-bounty-count-means.json', function (data) {

        var firstCompany = data[0][0];
        var secondCompany = data[1][0];
        var thirdCompany = data[2][0];
        var fourthCompany = data[3][0];
        var fifthCompany = data[4][0];

        var firstCompanyValue = data[0][1];
        var secondCompanyValue = data[1][1];
        var thirdCompanyValue = data[2][1];
        var fourthCompanyValue = data[3][1];
        var fifthCompanyValue = data[4][1];

        document.getElementById("firstCompanyIDCount").innerHTML = "<b>" + firstCompany + "</b>" + " mean bug counts: " + firstCompanyValue;
        document.getElementById("secondCompanyIDCount").innerHTML = "<b>" + secondCompany + "</b>" + " mean bug counts: " + secondCompanyValue;
        document.getElementById("thirdCompanyIDCount").innerHTML = "<b>" + thirdCompany + "</b>" + " mean bug counts: " + thirdCompanyValue;
        document.getElementById("fourthCompanyIDCount").innerHTML = "<b>" + fourthCompany + "</b>" + " mean bug counts: " + fourthCompanyValue;
        document.getElementById("fifthCompanyIDCount").innerHTML = "<b>" + fifthCompany + "</b>" + " mean bug counts: " + fifthCompanyValue;

    });

    $.getJSON('markets/bug-bounty-minimum-bounties-means.json', function (data) {

        var firstCompany = data[0][0];
        var secondCompany = data[1][0];
        var thirdCompany = data[2][0];
        var fourthCompany = data[3][0];
        var fifthCompany = data[4][0];

        var firstCompanyValue = data[0][1];
        var secondCompanyValue = data[1][1];
        var thirdCompanyValue = data[2][1];
        var fourthCompanyValue = data[3][1];
        var fifthCompanyValue = data[4][1];

        document.getElementById("firstCompanyIDBounty").innerHTML = "<b>" + firstCompany + "</b>" + " mean minimum bounty: " + firstCompanyValue;
        document.getElementById("secondCompanyIDBounty").innerHTML = "<b>" + secondCompany + "</b>" + " mean minimum bounty: " + secondCompanyValue;
        document.getElementById("thirdCompanyIDBounty").innerHTML = "<b>" + thirdCompany + "</b>" + " mean minimum bounty: " + thirdCompanyValue;
        document.getElementById("fourthCompanyIDBounty").innerHTML = "<b>" + fourthCompany + "</b>" + " mean minimum bounty: " + fourthCompanyValue;
        document.getElementById("fifthCompanyIDBounty").innerHTML = "<b>" + fifthCompany + "</b>" + " mean minimum bounty: " + fifthCompanyValue;

    });

</script>

<script>

    /* Bug Bounties for specific Companies --> Top 20 Bar Plot */
    $.getJSON('markets/minimum_bounties_perday.json', function (data) {

        // Create the chart
        var chart = Highcharts.chart('container2', {
            chart: {
                type: 'column',
                zoomType: 'x',
                panning: true,
                panKey: 'shift'
            },
            title: {
                text: 'Minimum Bounties for specific Companies'
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
                    text: 'USD'
                }
            },
            legend: {
                enabled: false
            },
            tooltip: {
                pointFormat: 'Number: <b>{point.y:.0f} USD</b>'
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

</script>

<!-- Script for rates -->
<script>

    /* BUG COUNT */
    var ratesOptions = [],
    ratesCounter = 0;
    //names = ["Yahoo!", "Shopify", "Uber", "Twitter", "Slack"];
    console.log('script called');

    function create_rateChart() {

      Highcharts.stockChart('container3', {

          title: {
              text: 'Change rates on every day resolved reports released on specific companies'
          },

          yAxis: {
              labels: {
                  formatter: function () {
                      return (this.value > 0 ? ' + ' : '') + this.value + '%';
                  }
              },
              plotLines: [{
                  value: 0,
                  width: 2,
                  color: 'silver'
              }]
          },
          plotOptions: {
              series: {
                  compare: 'percent',
                  showInNavigator: false
              }
          },
          tooltip: {
              pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y:.0f}</b> ({point.change}%)<br/>',
              valueDecimals: 2,
              split: true
          },
          series: ratesOptions
      });

    }
    /**
     * Create the chart when all data is loaded
     * @returns {undefined}
     */
     $.each(names, function (i, name) {

         $.getJSON('markets/perday-bug-bounties-count-' + name + '_rates.json', function (data) {
             ratesOptions[i] = {
                 name: name,
                 data: data
             };

             // As we're loading the data asynchronously, we don't know what order it will arrive. So
             // we keep a counter and create the chart when all the data is loaded.
             ratesCounter += 1;
             if (ratesCounter === names.length) {
                 // Create the chart
                 create_rateChart()
             }
         });
     });



</script>

<!-- Script for rates PERCENT(%) -->
<script>

    /* BUG COUNT */
    var ratesPercentOptions = [],
    ratesPercentCounter = 0;
    //names = ["Yahoo!", "Shopify", "Uber", "Twitter", "Slack"];
    console.log('script called');

    function create_ratePercentChart() {

      Highcharts.chart('container4', {
        chart: {
          type: 'area',
          zoomType: 'x'
        },
          title: {
              text: 'Change rates percent(%) on every day resolved reports released on specific companies'
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
                        apple = this;
                        retString = '';
                        //console.log(this);
                        //console.log(this.points[0].series.data);
                        //seriesData=this.points[0].series.data;
                        //  var index = seriesData.indexOf(this);
                        //get the index number in series of current point
                        var index = this.points[0].series.xData.indexOf(this.x);
                        retString = retString+Highcharts.dateFormat('%A %B %e %Y', this.x) + ':<br/>';
                        this.points.forEach(function(el){
                          if (typeof el !== 'undefined') {
                                // the variable is defined
                                console.log(el.series.name);
                                if (typeof el.series.data[index-1] !== 'undefined') {
                                      // the variable is defined
                                      previousValue=el.series.data[index-1].y;
                                  }
                                  else{
                                    previousValue = el.y;
                                  }
                                  //ti eixame, ti xasame
                                  if (previousValue != 0 ){
                                    diff = ((el.y - previousValue)*100)/previousValue;
                                  }
                                  else {
                                    diff = 0 ;
                                  }

                                  var sign = diff > 0 ? '+' : '';
                                  var seriesName = el.series.name;
                                  var seriesColor = el.series.color;
                                  retString = retString + '<span style="color:'+seriesColor+';font-weight:bold">' +seriesName + ' : '
                                  +el.y+ " ("+sign+Highcharts.numberFormat(diff, 2) + '%'+")"+'</span><br/>';
                            }

                        });
                        console.log(index);
                        //console.log(retString);
                        //trace previous point
                        // if (typeof this.points[0].series.data[index-1] !== 'undefined') {
                        //       // the variable is defined
                        //       previousValue=this.points[0].series.data[index-1].y;
                        //   }
                        //   else{
                        //     previousValue = this.y;
                        //   }
                        //
                        // //ti eixame, ti xasame
                        // if (previousValue != 0 ){
                        //   diff = ((this.y - previousValue)*100)/previousValue;
                        // }
                        // else {
                        //   diff = 0 ;
                        // }
                        //console.log("previous value: "+previousValue+" diff % "+diff);
                          // var point = this.points[0];
                          // var sign = diff > 0 ? '+' : '';
                          // return Highcharts.dateFormat('%A %B %e %Y', this.x) + ':<br/>'+ point.series.name + ' : '+
                          // '<b>'+this.y+ " ("+sign+Highcharts.numberFormat(diff, 2) + '%'+")"+'</b>';
                          return retString;
                      },
                      shared: true
                  },
          series: ratesPercentOptions
      });

    }
    /**
     * Create the chart when all data is loaded
     * @returns {undefined}
     */
     $.each(names, function (i, name) {

         $.getJSON('data_analysis_exports/markets/perday-bug-bounties-count-' + name + '_rates.json', function (data) {
             ratesPercentOptions[i] = {
                 name: name,
                 data: data
             };

             // As we're loading the data asynchronously, we don't know what order it will arrive. So
             // we keep a counter and create the chart when all the data is loaded.
             ratesPercentCounter += 1;
             if (ratesPercentCounter === names.length) {
                 // Create the chart
                 create_ratePercentChart()
             }
         });
     });



</script>


<!-- all scripts bug rate change -->
<script>
    //var apple2 = [];
    // Global variable to keep mean value of all rates
    // until 25 September 2018 (epoch 1537919999000 in ms)

    var mean_value = 1;
    var sortArray = [];
    loadJSON('data_analysis_exports/markets/allBugsRatePerDay.json', function(response) {
      // Parse JSON string into object
        var input1 = JSON.parse(response);
        //apple2 = input1;
        var sum = 0;
        var cnt = 0;
        for (let v of input1)
          {
            if (v[0]< 1537919999000)
            {
              sum = sum + v[1];
              cnt++;
            }
            else {
              sortArray.push(v);
            }
          }
          // calculation of mean value with round to nearest higher integer
          mean_value = Math.ceil(sum/cnt);
          document.getElementById("mean_val_par").innerHTML = "Mean (rounded to higher integer): <i>"+mean_value+"</i> resolved reports";
          console.log("mean value with round to nearest higher integer "+mean_value);
     });

    $.getJSON('data_analysis_exports/markets/allBugsRatePerDay.json', function (daily_data) {

        // Create the chart
        var chart_daily = Highcharts.chart('container5', {

          chart: {
              type: 'area',
              zoomType: 'x'
          },

            title: {
                text: 'Daily Resolved Reports change rate'
            },
            xAxis: {
                           type: 'datetime'
                       },
            tooltip: {
                formatter: function(){

                  //get the index number in series of current point
                  var index = this.points[0].series.xData.indexOf(this.x);
                  // apple = this.points[0].series;
                  console.log(index);
                  //trace previous point
                  // According to new approach, in case selected value is
                  // before 25 September 2018 (epoch 1537919999000 in ms)
                  // calculation is done by reference to first recorded value.
                  // For all epochs after it, mean value of all those recordings
                  // is used as a reference.

                  diff = ((this.y - mean_value)*100)/mean_value;
                  console.log("diff % "+diff);
                    var point = this.points[0];
                    var sign = diff > 0 ? '+' : '';
                    return Highcharts.dateFormat('%A %B %e %Y', this.x) + ':<br/>'+ point.series.name + ' : '+
                    '<b>'+this.y+ " ("+sign+Highcharts.numberFormat(diff, 2) + '%'+")"+'</b>';
                },
                shared: true
            },
            series: [{
                name: 'Resolved Reports rate per day',
                data: sortArray,
                color: "silver",
            }]
        });


    });



</script>

<script src="detailChart.js"></script>

</body>

</html>
