# ---------------------------------------------------------------------------------------------
# Main.py
# Python 3.X required to run
# Created by Julian Smith

import visit
import webdata
import links
import index
import sys

loop_main = True
loop = True
indexing = True
user_url = ""
# Advanced options variables
custom_search_words = ""
custom_title_class = ""
custom_description_class = ""
custom_code_class = ""
custom_def_class = ""
custom_def_id = ""
custom_global_tags = ""

# Welcome Message
print("--------------------------------------------------------------------------------------")
print("|                                  Welcome to Apropos                                |")
print("--------------------------------------------------------------------------------------")
print("|           To get started, type the website you want to crawl's URL below           |")
print("--------------------------------------------------------------------------------------")
while loop_main:
    # This while loop is in place as a check to make sure the user wants to visit the website they've typed in
    while loop:
        user_url = input("Website URL = ")
        if ("https://" or "http://") not in user_url:
            print("WARNING | URL does not contain HTTP or HTTPS request")
            httpAdd = input("Add HTTP [1] , add HTTPS [2] , continue [3] = ")
            if httpAdd is "1":
                user_url = "http://" + user_url
            elif httpAdd is "2":
                user_url = "https://" + user_url
        print("--------------------------------------------------------------------------------------")
        print("Is " + user_url + " the website you want to index?")
        check_url = input("Enter Y for Yes or N for No = ")
        if "y" in check_url or "Y" in check_url:
            loop = False
    print("--------------------------------------------------------------------------------------")
    # How many pages to index
    indexLimit = input("Maximum number of pages to index (0 = No Limit) = ")
    indexLimit = int(indexLimit)
    if indexLimit is 0:
        indexLimit = 1000000
        indexLimitBool = False
    else:
        indexLimitBool = True
    print("--------------------------------------------------------------------------------------")
    # Advanced options question
    print("Enter Advanced Options?")
    ask = input("Enter Y for Yes or N for No = ")
    advanced_options = False
    if "y" in ask or "Y" in ask:
        advanced_options = True
        print("--------------------------------------------------------------------------------------")
        print("|                                   Advanced Options                                 |")
        print("--------------------------------------------------------------------------------------")
        print("|    In advanced options you can set specific class names to items Apropos indexes   |")
        print("|       If you don't want to make changes to one of the options, leave it blank      |")
        print("--------------------------------------------------------------------------------------")
        ask = ""
    while advanced_options:
        print("DEFINITION & CODE SETTINGS | Enter settings to enable definition and code gathering, ")
        ask = input("press Y to enter = ")
        if "y" in ask or "Y" in ask:
            ask = ""
            print("--------------------------------------------------------------------------------------")
            print("|                             DEFINITION & CODE SETTINGS                             |")
            print("--------------------------------------------------------------------------------------")
            custom_def_id = input(
                "DEFINITION DIV ID NAME | Enter the ID name for the DIV which contains the definition = ")
            print("DEFINITION DIV CLASS NAME | Enter the CLASS name for the DIV which contains the")
            custom_def_class = input("definition = ")
            print("CODE CLASS NAME | Enter the class name for the DIV which contains the code section on")
            custom_code_class = input("each web page =  ")
        print("TITLE CLASS NAME | Enter the class name for the class which contains the title on ")
        custom_title_class = input("each web page =  ")
        print("DESCRIPTION CLASS NAME | Enter the class name for the class which contains the ")
        custom_description_class = input("description on each web page =  ")
        # COMPLETE
        custom_global_tags = input("Keywords to apply to whole website (separated by \" , \") = ")
        # COMPLETE
        print("INDEX CRITERIA | Only index the web page if  it contains the following text on the ")
        custom_search_words = input("web page. Separate different items by adding \" , \" between each item = ")
        if indexing:
            ask = input("Turn Indexing Off? Enter Y for Yes = ")
            if "y" in ask or "Y" in ask:
                ask = ""
                indexing = False
        else:
            if not indexing:
                ask = input("Turn Indexing On? Enter Y for Yes = ")
                if "y" in ask or "Y" in ask:
                    ask = ""
                    indexing = True
        print("--------------------------------------------------------------------------------------")
        ask = input("Apply changes? Enter Y for Yes or N for No = ")
        if "y" in ask or "Y" in ask:
            ask = ""
            advanced_options = False
    print("--------------------------------------------------------------------------------------")
    print("Visiting " + user_url)

    # ---------------------------------------------------------------------------------------------
    # Visit Site
    class GetSite:
        soup = visit.soup_setup()
        links_to_visit = True
        links_list = []
        i = 0
        index_url = user_url
        link_search = False
        indexCount = 0
        # ---------------------------------------------------------------------------------------------
        # Loop through while there are still links on thr website that have not been visited
        while links_to_visit or (indexCount <= indexLimit):
            web_index = True
            # If links list is empty i.e not scanned website yet for links
            if not links_list:
                # Visit the link the user provided
                soup = visit.soup_visit(index_url, link_search)
                # Handle HTTP and URL errors
                if soup == "FAIL":
                    links_to_visit = False
                    break
            # If links list is not empty
            if links_list:
                link_search = True
                # Visit the next link in the list
                soup = visit.soup_visit(links_list[i], link_search)
                # Handle HTTP and URL errors
                while soup == "FAIL":
                    i += 1
                    # Visit next link as a fallback for the previous link failing
                    soup = visit.soup_visit(links_list[i], link_search)
                index_url = links_list[i]
                i += 1
            links_list = links.get_links(soup, user_url)
            # ---------------------------------------------------------------------------------------------
            # Check to see if the web page contains the keywords the user specified
            if custom_search_words:
                web_index = webdata.web_contains(soup, custom_search_words)
            # ---------------------------------------------------------------------------------------------
            if web_index:
                indexCount += 1
                urlTitle = webdata.url_title(soup, custom_title_class)
                print("{:11} = {}".format('TITLE', urlTitle))
                print("{:11} = {}".format('URL', index_url))
                urlDesc = webdata.url_desc(soup, custom_description_class)
                print("{:11} = {}".format('DESCRIPTION', urlDesc))
                urlKeywords = webdata.url_keywords(soup, index_url, custom_global_tags)
                print("{:11} = {}".format('KEYWORDS', urlKeywords))
                urlCode = webdata.url_code(soup, custom_code_class)
                print("{:11} = {}".format('CODE', urlCode))
                urlDef = webdata.url_definitions(soup,custom_def_id, custom_def_class)
                print("{:11} = {}".format('DEFINITION', urlDef))
                # ---------------------------------------------------------------------------------------------
                # If indexing is turned on, store the web page
                if indexing:
                    index.index_links(urlTitle, index_url, urlDesc, urlKeywords, urlDef, urlCode)
                # ---------------------------------------------------------------------------------------------
                print("--------------------------------------------------------------------------------------")
            if i > 0 and i is len(links_list) or (indexCount == indexLimit - 1):
                links_list = []
                links_to_visit = False
                print("--------------------------------| FINISHED |------------------------------------------")
            elif len(links_list) is 0:
                links_list = []
                links_to_visit = False
                print("--------------------------------| FINISHED |------------------------------------------")
            else:
                if indexLimitBool:
                    link_count = indexLimit
                else:
                    link_count = len(links_list) - i
                percentComplete = (indexCount / link_count) * 100
                print("{:11} = {} / {} | {:.2f}%".format('Links Left', indexCount, link_count, percentComplete))

    # Gives user option to index another website or to exit the program
    print("Index another web site or end program?")
    ask = input("Enter Y to index another website or N to end = ")
    if "n" in ask or "N" in ask:
        loop_main = False
        sys.exit("PROGRAM TERMINATED")
    else:
        loop = True