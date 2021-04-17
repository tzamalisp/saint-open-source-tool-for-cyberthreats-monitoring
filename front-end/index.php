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

        /* mouse over link */
        .social:hover {
            color: #444444 !important;
        }

        /* selected link */
        .social:active {
            color: #ffffff;
        }

        /* visited link */
        .social:visited {
            color: #ffffff;
        }


        /* unvisited link */
        .social:link {
            color: #ffffff;
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
    <h1 class="margin">SAINT Data Analysis Tools by CTI</h1>
    <h3>Cybersecurity Social Network Analyzer (CSNA)</h3>
    <h3>Clearnet Crawler Tool</h3>
    <hr>
    <div><a class="social" href="https://project-saint.eu/" target="_blank">SAINT Official Website</a></div>
    <div><a class="social" href="https://www.facebook.com/saintprojecteu/" target="_blank">SAINT on Facebook</a></div>
    <div><a class="social" href="https://www.linkedin.com/in/saintprojecteu/" target="_blank">SAINT on LinkedIn</a></div>
    <div><a class="social" href="https://twitter.com/saintprojecteu" target="_blank">SAINT on Twitter</a></div>
    <div><a class="social" href="https://vimeo.com/saintprojecteu" target="_blank">SAINT on Vimeo</a></div>
</div>

<!-- Second Container-->
<div class="container-fluid bg-2 text-center">
<!--    <h3 style="color: black;"><u>Hashtags time series - Ransomware</u></h3>-->
<!--    <div id="container2" style="width:100%; height:450px;"></div>-->
    <h3 class="descriptionHeader">CTI's Twitter and Threats Analysis Tools Progress Description</h3>
    <br>
    <h4 class="descriptionHeader"><b>The Cybersecurity Social Network Analyzer (CSNA)</b></h4>
    <div>
        <ul>
            <li class="description">The Time Series Descriptive Analysis has now been completed. Tweets about
                a) Markets: Bug Bounty Programs and b) Threats: Ransomware, Malware, Trojan, Botnets, Phishing are now
                collected to the database and later processed with and analyzed with Natural Language Processing
                techniques, in real-time, for the data visualization. The search keyword lists that feed the Twitter
                Crawler to crawl the Twitter’s API, are now enriched:
            </li>
                <ul>
                    <li class="description">Markets searching keywords: #BugBounty', '#vulnerability #market',
                        '#security #contest', '#bugsbounty', '#securitycontest', '#securitycontest #vulnerability',
                        '#vulnerability #bugsbounty', '#bugbounty #securitycontest', '#securitycontest #bugsbounty
                    </li>
                    <li class="description">Threats searching keywords: '#malware', '#apt', '#ransomware', '#spyware',
                        '#xss', '#lfi', '#rfi', '#websecurity', '#xee', '#webappsec', '#DoS', '#DDoS',
                        '#botnet', '#botmaster', '#botnets', '#phishing', '#phish', '#pharming', '#spam',
                        '#idtheft', '#trojan'
                    </li>
                </ul>
            <li class="description">The Categorical Analysis or Entity Analysis depicts now the 10 most frequently
                used hashtags, user mentions and word terms in users’ tweets over the last 7 days. A further research
                took place, and the stop words list in the relevant Natural Language Processing methods has been
                parameterized in the needs of the Analysis.
            </li>
            <li class="description">A real-time dynamic News Feed has been created, which is related to the Top 9 User
                Mentions in users’ tweets and is fed by the relative list that is yielded by the User Mentions Entity
                Analysis. Two News Feed menus that include the timelines of that User Mentions are outcomes of such
                analysis, the Threats Top Timelines and the Markets Top Timelines.
            </li>
            <li class="description">Two Word Clouds related to the tweets that are collected and which are related
                to the Cybersecurity markets and Cyber-attacks over the last 30 days are yielded now. The Word Clouds
                are a perfect data visualization outcome for a better understanding of the trends, about “what people
                talk”, and decision making in Human Intelligence part.
            </li>
            <li class="description">Furthermore, the data processing and analysis execution time for each Analysis
                category has been improved by 80%. The whole platform has been transferred to the MongoDB database
                (in the earlier version of the framework, the data was saved to JSON files), and relevant queries
                have been created for each Analysis part to achieve better execution times.
            </li>
            <li class="description">For each Data Analysis part of the CSNA, a downloadable CSV file is also available,
                so SAINT’s stakeholders can use for an offline analysis.
            </li>
            <li class="description">The real-time data processing and analysis of the collected data is a feature of
                CTI’s CSNA.
            </li>
        </ul>
    </div>
    <br>
    <h4 class="descriptionHeader"><b>The Clearnet Crawler Tool</b></h4>
    <div>
        <ul>
            <li class="description">Successfully crawled and scraped websites related to Bug Bounty Programs,
                Web-Based Attacks, Malware, Botnets, Phishing, DDoS attacks, and 0-day exploits.
            </li>
            <li class="description">Time Series Descriptive Analysis for each of the ENISA Top threats: Web-Based
                Attacks, Malware, Botnets, Phishing, DDoS.
            </li>
            <li class="description">Categorical Analysis for the Top Malware and
                Ransomware categories.
            </li>
            <li class="description">Categorical Analysis on Botnets for the Top IP addresses where Botnets were
                detected over the last 7 days.
            </li>
            <li class="description">Categorical Analysis of Top Malware
                attacks.
            </li>
            <li class="description">Bug Bounty programs Time Series Analysis (showing the rate of Bugs and Bounties
                for specific companies and organizations).
            </li>
            <li class="description">The CSNA is now fed by the Top Malware and Ransomware categories (as keywords)
                that are outcomes by the Clearnet Crawler tool’s processing and analysis of the data collected,
                and a Time Series Descriptive Analysis is created in the collected tweets, for each category,
                including the corresponding visualization outcomes.
            </li>
            <li class="description">All the Analysis frameworks are functional and run in
                real-time.</li>
            <li class="description">Phishing current instance of
                attacks.
            </li>
            <li class="description">Top 20 Web-Based attacks over the
                last 24 hours.
            </li>
            <li class="description">For all the crawling sub-tools, for each threat category, for the bug bounty
                programs, and the 0-day exploits, relevant datasets are also exported and available for download via
                the UI tool.
            </li>
            <li class="description">For each Data Analysis part of the Clearnet tool categories, a downloadable CSV
                file is also available, so SAINT’s stakeholders can use for an offline analysis.
            </li>
            <li class="description">Datasets are now created much faster than previous versions of Clearnet Crawler’s
                Analysis tools. A whole new method has been implemented with parallel processing to achieve these
                improvements. Each dataset is stored in a zip file that contains multiple CSV files, each for
                each month.
            </li>
            <li class="description">Phishing and Malware web crawling results feed dynamically the SNA with their top
                categorized threats, to search the trending topics in Twitter posts.</li>
        </ul>
    </div>
    <br>
    <h4 class="descriptionHeader"><b>The Dark Web Crawler Tool</b></h4>
    <div>
        <ul>
            <li class="description">Successfully scraped the Dark Wiki. All the Fraud Services + Digital Gangster +
                Hacker Group are listed and exported to a CSV file that feeds the ACHE Crawler which is now configured
                to SAINT’s needs. These are links related to the following keywords:</li>
            <ul>
                <li class="description">Economic activity keywords in the form of regular expressions: card(s), CC,
                    fraud, market, PayPal, euros, dollars, €, $, BTC, XMR, monero, *coins </li>
                <li class="description">o	Illegal activity keywords: malware, ransomware, spyware, (d)dos, xss, xee,
                    botnet, phish*, theft, crack, hack, spam, trojan, pharming</li>
            </ul>
            <li class="description">CTI team created a documentation for the KEMEA and the Hellenic Police Cybercrime
                Unit of how to access, search and read the data that are collected by the DWC tool.</li>
            <li class="description">A txt file that contains reports of the crawled websites is exported after each
                crawling process and which contains:</li>
            <ul>
                <li class="description">HTTP 2xx: Success</li>
                <li class="description">Error HTTP 401: Unauthorized</li>
                <li class="description">Error HTTP 403: Forbidden</li>
                <li class="description">Error HTTP 404: Not Found</li>
                <li class="description">Error HTTP 5xx: Server Errors</li>
                <li class="description">Relevant URLs that are downloaded</li>
            </ul>
            <li class="description">Each document (record in Database) contains the following information:</li>
            <ul>
                <li class="description">URL</li>
                <li class="description">Title</li>
                <li class="description">Category</li>
                <li class="description">HTML code of the scraped website</li>
                <li class="description">Timestamp when the link was fetched</li>
                <li class="description">MongoDB format Datetime when the link was fetched</li>
            </ul>
        </ul>
    </div>
</div>


<!-- Third Container -->
<div class="container-fluid bg-1 text-center">
    <h3>The SAINT Global Security Map that is an outcome of the analysis of the data collected in CTI's server</h3>
    <br>
    <img src="images/gsm-screenshot.png" alt="Global Security Map" width="100%">
    <div>Visit the Global Security Map tool <a class="social" href="https://3hz6pq.staging.cyberdefcon.com/#" target="_blank"><u>here</u></a></div>
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


</script>

</body>

</html>