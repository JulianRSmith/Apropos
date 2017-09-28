<!DOCTYPE html>
<html lang="en-GB">
<head>
    <meta charset="UTF-8">

    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Appropos Beta</title>

    <!--[if IE]><link rel="shortcut icon" href="media/favicon-ico.ico"><![endif]-->
    <link rel="icon" href="media/favicon.png">
    <link rel="apple-touch-icon-precomposed" href="media/favicon-apple.png">

    <link rel="stylesheet" href="https://necolas.github.io/normalize.css/6.0.0/normalize.css">
    <link rel="stylesheet" href="style.css">

    <link href="https://fonts.googleapis.com/css?family=Nunito|Open+Sans" rel="stylesheet">

    <script type="text/javascript">
        window.onload = function()
        {
            document.getElementById("searchInput").focus();
        }
    </script>
    <script type="text/javascript">

    </script>


</head>
<body>
<div class="bg_gradient">
    <div class="wrapper">
        <div class="logo">
            <img src="media/Logo.svg" onerror="this.onerror=null; this.src='media/logoXL.png'">
        </div>
        <div class="search">
            <form action="search.php" method="get">
                <input type="search" name="s" id="searchInput" placeholder="Search..."" >
            </form>
        </div>
    </div>
    <footer class = "footerMain">
        <div class="version">
            Version: 0.6
        </div>
    </footer>
</div>
</body>
</html>