<?php

    include 'resultsFind.php';

    // Connect
    $mysqli = new mysqli("212.48.67.136", "apropos_julian", "Sr0rwccd605", "apropos_indexedResultsDB");
    // Check connection
    if (!$mysqli) {
        echo("Connection to database failed: " . mysqli_connect_error());
    }

    // Gets the total number of querys
    $query = "SELECT COUNT(id)";
    $query .= pageRank($terms);
    $newquery = mysqli_query($mysqli,$query);
    $numrows = mysqli_fetch_row($newquery);
    // Total row count
    $rows = $numrows[0];
    // Number of results per page
    $pageRows = 10;
    // Number of pages required rounded up
    $pageReq  = ceil($rows/$pageRows);
    // Make sure last page cannot be less than 1
    if($pageReq < 1) {
        $pageReq = 1;
    }
    // Set page number variable
    $pageNumber = 1;
    // Get the page number from the URL variable pg if it exists otherwise it's 1
    if(isset($_GET['pg'])) {
        // Make it so only numbers can be in the URL variable
        $pageNumber = preg_replace('#[^0-9]#', '', $_GET['pg']);
    }
    // Make sure page number isn't less than 1 or greater than the last page
    if($pageNumber < 1) {
        $pageNumber = 1;
    } else if ($pageNumber > $pageReq){
        $pageNumber = $pageReq;
    }
    // Make sure to only display the certain amount of results
    $limit = ' LIMIT ' .($pageNumber - 1) * $pageRows .',' .$pageRows;
    // Add limit to query
    $query = "SELECT *";
    $query .= pageRank($terms);
    $query .= "$limit";
    $newquery = mysqli_query($mysqli,$query);
    if (!$newquery) {
        printf("Error: %s\n", mysqli_error($mysqli));
        exit();
    }

    // Pagination Controls and Setup
    // -------------------------------------------------------------------------------------------
    $pageCountLine = $rows;
    $pageNumLine = "Page $pageNumber of $pageReq";
    // Page nation controls variable
    $pageControl = '';
    // If there is more than 1 page of controls
    if ($pageReq != 1) {
        if($pageNumber > 1) {
            $previous = $pageNumber - 1;
            $pageControl .= '<a href="'.$_SERVER['PHP_SELF'].'&pg='.$previous.'">&lt; Previous</a> &nbsp; &nbsp; ';
            // Render clickable number links, the negative 4 represents the max number of pages to display
            for($i = $pageNumber - 4; $i < $pageNumber; $i++){
                // Don't make 0 render
                if($i > 0){
                    // Make items clickable
                    $pageControl .= '<a href="'.$_SERVER['PHP_SELF'].'?s='.$keywords.'&pg='.$i.'">'.$i.'</a> &nbsp; ';
                }
            }
        }
        // Render current page number without a link
        $pageControl .= '<div id="currentPage">'.$pageNumber.'</div> ';
        // Render clickable items that should appear on the right
        for($i = $pageNumber+1; $i <= $pageReq; $i++){
            $pageControl .= '<a href="'.$_SERVER['PHP_SELF'].'?s='.$keywords.'&pg='.$i.'">'.$i.'</a> &nbsp; ';
            // Limit for loop from running after running for 4 times
            if($i >= $pageNumber + 4){
                break;
            }
        }
        // Display Next word for the user
        if ($pageNumber != $pageReq) {
            $next = $pageNumber + 1;
            $pageControl .= ' &nbsp; &nbsp; <a href="'.$_SERVER['PHP_SELF'].'?s='.$keywords.'&pg='.$next.'">Next &gt;</a> ';
        }
    }

    // Results
    // -------------------------------------------------------------------------------------------
    $resultsList = '';
    $definition = '';
    $definitionLink = '';
    $code = '';
    $codeLink = '';
    while ($row = mysqli_fetch_array($newquery, MYSQLI_ASSOC)){
        $id = $row["id"];
        $title = $row["title"];
        $url = $row["url"];
        $desc = $row["description"];
        $idCount = 0;
        if (($definition == '' || $definition == 'NONE') && $idCount < 8) {
            $definition = $row['definition'];
            $definitionLink = $url;
            $idCount++;
        }
        $idCount = 0;
        if (($code == '' || $code == 'NONE' ) && $idCount < 8) {
            $code = $row["code_example"];
            if($code != strip_tags($code)) {
                $code = strtr($code,Array("<"=>"&lt;","&"=>"&amp;"));
                $code = str_replace(">","><br>",$code);
            }
            $codeLink = $url;
            $idCount++;
        }
        $resultsList .= "<div class='searchLink'><a href='$url'><div class = 'searchResult'><h2>$title</h2>
        <p class='searchURL'>$url</p><p class='searchDesc'>$desc</p></div></a></div><br>";
    }

    if ($pageCountLine == 1) {
    $resultInfoTxt = "1 Result Found in ";
}
    else {
        $resultInfoTxt = "$pageCountLine Results Found in ";
    }

mysqli_close($mysqli);

 ?>
<!DOCTYPE html>
<html lang="en-GB">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Apropos Beta | <?php echo $userQuery; ?></title>

    <!--[if IE]><link rel="shortcut icon" href="media/favicon-ico.ico"><![endif]-->
    <link rel="icon" href="media/favicon.png">
    <link rel="apple-touch-icon-precomposed" href="media/favicon-apple.png">

    <link rel="stylesheet" href="https://necolas.github.io/normalize.css/6.0.0/normalize.css">
    <link rel="stylesheet" href="style.css">

    <link href="https://fonts.googleapis.com/css?family=Nunito|Open+Sans" rel="stylesheet">

    <script type="text/javascript">
        var timerStart = Date.now();
    </script>
    <script type="text/javascript" src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script type="text/javascript">
        $(document).ready(function(){
            $(window).resize(function(){
                <!-- jQuery sticky footer -->
                if ($('#paginationControls').length) {
                    var footerHeight = $('.footerSearch').outerHeight();
                    footerHeight -= 40;
                    $('.contentWrapper').css({'marginBottom': '+' + footerHeight + 'px'});
                } else {
                    var footerHeight = $('.footerSearch').outerHeight();
                    $('.contentWrapper').css({'marginBottom': '-' + footerHeight + 'px'});
                }
                <!-- Centre search not found div -->
                if ($('#searchNoneFound').length) {
                    var screenHeight = $(window).height();
                    var verticalCentre = (screenHeight/2)-120;
                    $('.searchNoneFound').css({'marginTop': verticalCentre + 'px'});
                }
            });

            $(window).resize();
        });
    </script>

</head>
<body>
<div class="contentWrapper">
<div class = "searchTopBar">
    <div class="searchLogo">
        <a href="index.php"><img src="media/Logo.svg" onerror="this.onerror=null; this.src='media/logoXL.png'"><a/>
    </div>
    <div class="searchField">
        <form action="search.php" method="get">
            <input type="text" name="s" id="searchInput" value="<?php echo $userQuery; ?>"/>
        </form>
    </div>
</div>
<div class='searchInfo' id = 'searchInfo'>
    <p></p>
</div>
<div class='searchResultWrapper'>
        <?php
        if ($definition != "NONE") {
            if ($pageCountLine != 0) {
                echo "<div class='searchLink'><a href='$definitionLink'><div class=\"definition\">$definition</div></a></div><br>";
            }
        }
        if ($code != "NONE") {
            if ($pageCountLine != 0) {
                echo "<div class='searchLink'><a href='$codeLink'><div class=\"codeSample\">$code</div></a></div><br>";
            }
        }
        if ($pageCountLine == 0){
            echo "<div class='searchNoneFound' id='searchNoneFound'>Whoops! No results found for $userQuery!</div>";
        } else {
            echo $resultsList;
        }
    ?>
</div>
<br>
    <?php
    if ($pageReq != 1) {
        echo "<div class=\"paginationWrapper\"><div id=\"paginationControls\">$pageControl</div></div><br>";
    }
    ?>
</div>
<footer class="footerSearch" id="footer">
    <div class="version">
        Version: 0.6
    </div>
</footer>
<script type="text/javascript">
    window.onload = function() {
        var timerEnd = (Date.now()-timerStart)/ 1000;
        var time = timerEnd.toFixed(2);
        var p = document.getElementById("searchInfo");
        p.innerHTML = "<p><?php echo $pageNumLine; ?> | <?php echo $resultInfoTxt; ?>" + time + " Seconds </p>";
    };
</script>
</body>
</html>