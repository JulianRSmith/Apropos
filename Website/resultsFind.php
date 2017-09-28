<?php
/**
 * Created by PhpStorm.
 * User: Julian Smith
 * Date: 13/04/2017
 * Time: 15:15
 */


# Get search term from the url
$keywords = $_GET['s'];
# Redirects the user to the homepage if the query is blank
if ($keywords == "" or $keywords == " " or $keywords == "+") {
    header("Location: index.php");
    exit();
}
# Eliminates white space before and after text
$keywords = trim($keywords);
# Make a copy for use in other areas of web site
$userQuery = $keywords;
# Make search term lowercase
$keywords = strtolower($keywords);
# Brake up words and add them to an array list
$terms = explode(" ", $keywords);
# Add original search term to array list too if it's more than 1 word
if(sizeof($terms)>1){
    array_push($terms, $keywords);
}


# Finds results based off the keywords and titles in the database
function pageRank($terms) {
    $i = 0;
    $query = ", MATCH(title,keywords) AGAINST('";
    foreach ($terms as $item) {
        if ($i == 0) {
            $query .= "+%$item%";
        } else {
            $query .= " +%$item%";
        }
        $i++;
    }
    $query .= "' IN BOOLEAN MODE) AS relevance FROM indexTable WHERE MATCH(title,keywords) AGAINST('";
    foreach ($terms as $item) {
        if ($i == 0) {
            $query .= "+%$item%";
        } else {
            $query .= " +%$item%";
        }
        $i++;
    }
    $query .= "' IN BOOLEAN MODE) ORDER BY relevance DESC";
    return $query;
}