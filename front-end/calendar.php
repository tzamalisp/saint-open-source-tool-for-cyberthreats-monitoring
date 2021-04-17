<!DOCTYPE html>
<html>
<head>
	<title>Datepicker</title>

	 <!-- Latest compiled and minified CSS -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">

	<!-- jQuery library -->
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>

	<!-- Latest compiled JavaScript -->
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script> 

</head>
<body>
        <script type="text/javascript">

            var myDate="2012-02-26";
			myDate=myDate.split("-");
			var newDate=myDate[1]+"/"+myDate[2]+"/"+myDate[0];
			alert(new Date(newDate).getTime()); //will alert 1330210800000
        </script>
    </div>
</div>

</body>
</html>