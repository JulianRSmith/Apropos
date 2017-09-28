# ---------------------------------------------------------------------------------------------
# WebData.py
# Python 3.X required to run
# Created by Julian Smith

import re

# ---------------------------------------------------------------------------------------------
# TITLE
# Get the URL title
def url_title(soup, title_class):
    # Get the custom class that the user specified
    if title_class:
        title = soup.find(attrs={"class": title_class})
        title = title.getText()
    else:
        title = soup.title.string
    # Remove leading white space from the string
    if title:
        title = title.strip()
    else:
        title = ""
    return title
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# DESCRIPTION
# Find all items with the attribute name description
def url_desc(soup, desc_class):
    # Get the custom class that the user specified
    if desc_class:
        desc = soup.find("div", {"class": desc_class}).p
    else:
        # Check to see if a description has been supplied
        desc = soup.findAll(attrs={"name": "description"})
        if not desc:
            desc = soup.findAll(attrs={"name": "Description"})
        # If no description is provided...
        if not desc:
            # Description is equal to the first instance of paragraph text (p)
            try:
                desc = soup.p.getText()
            except:
                desc = ""
        # If a description is provided...
        else:
            # Get the content of the description tag and convert it to readable text
            desc = desc[0]['content'].encode('utf-8')
            desc = desc.decode('utf-8')
    # Remove any leading white space
    desc = desc.strip().replace('\n', ' ')
    # Shorten description to 160 characters if too long
    if len(desc) > 160:
        desc_trim = (len(desc) - 157)
        desc = desc[:-desc_trim]
        desc += "..."
    return desc
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# KEYWORDS
# Generate keywords for each web page
def url_keywords(soup, url, users_keywords):
    # Set up the keywords list variable
    keywords_list = []
    # Get keywords from the meta content
    keywords = soup.findAll(attrs={"name": "keywords"})
    # If that fails, try with a capital letter instead
    if not keywords:
        keywords = soup.findAll(attrs={"name": "Keywords"})
    # If keywords has now been found...
    if keywords:
        # Convert it to readable text
        keywords = keywords[0]['content'].encode('utf-8')
        keywords = keywords.decode('utf-8')
        # Make lower case and add each item to list
        keywords_list = keywords.lower().split(',')
    # If the user has supplied their own keywords
    if users_keywords:
        # Brake up each keyword supplied
        users_keywords_list = users_keywords.lower().split(" , ")
        # Add keyword to list if not already in the list
        for keyword in users_keywords_list:
            if keyword not in keywords_list:
                keywords_list.append(keyword)
    # Gets keywords from the URL
    url_keywords_list = []
    # Break up url every time there is a "."
    url_dot_keywords_list = url.lower().split('.')
    for keyword in url_dot_keywords_list:
        # Eliminates https://www from keywords
        if "://" not in keyword:
            # Get keywords from forward slashes
            if "/" in keyword:
                url_slash_keywords_list = keyword.split("/")
                for slash_keyword in url_slash_keywords_list:
                    # Brake up words with slashes
                    if "-" in slash_keyword:
                        url_dash_keywords_list = slash_keyword.split("-")
                        # Add to list if not already in list
                        for dash_keyword in url_dash_keywords_list:
                            if dash_keyword not in url_keywords_list:
                                url_keywords_list.append(dash_keyword)
                    # Brake up words with underscores
                    elif "_" in slash_keyword:
                        url_under_keywords_list = slash_keyword.split("-")
                        # Add to list if not already in list
                        for under_keyword in url_under_keywords_list:
                            if under_keyword not in url_keywords_list:
                                url_keywords_list.append(under_keyword)
                    # Otherwise, just add item to the keywords list
                    else:
                        if slash_keyword not in url_keywords_list:
                            url_keywords_list.append(slash_keyword)
            else:
                url_keywords_list.append(keyword)
    # Add url keywords to keywords list if not already in the list
    for keyword in url_keywords_list:
        if keyword not in keywords_list:
            keywords_list.append(keyword)
    # Add keywords from H1, H2, H3, and bold (b) tags
    h_tags_list = []
    h_tags = ['h1', 'h2', 'h3', 'b']
    i = 0
    while i < len(h_tags):
        keywords = soup.find_all(h_tags[i])
        if keywords:
            for keyword in keywords:
                keyword = keyword.getText().lower().strip()
                # Remove unwanted characters and content from keywords
                keyword = keyword.replace("(", "")
                keyword = keyword.replace(")", "")
                keyword = re.sub('\[.*?\]', '', keyword)
                h_tags_list.append(keyword)
        i += 1
    # Break up the words from the tags if there is a space
    for keyword in h_tags_list:
        if " " in keyword:
            h_tags_brake = keyword.split(" ")
            for keyword in h_tags_brake:
                if keyword not in keywords_list:
                    keywords_list.append(keyword)
        else:
            if keyword not in keywords_list:
                keywords_list.append(keyword)
    # Remove unwanted keywords from list
    keywords_unwanted = ['html', 'aspx', 'com', '^', 'php']
    for keyword in keywords_list:
        if keyword in keywords_unwanted:
            keywords_list.remove(keyword)
    # Remove unwanted characters from keyword
    for i, keyword in enumerate(keywords_list):
        if "¶" or ":" or "?" in keyword:
            keyword = keyword.replace("¶", "").replace(":", "").replace("?", "")
            keywords_list[i] = keyword
    # Convert list to easy to read string
    keywords_list = ' , '.join(keywords_list)
    return keywords_list


# ---------------------------------------------------------------------------------------------
# CODE
def url_code(soup,code_class):
    if code_class:
        try:
            code = soup.find("div", {"class": code_class}).text
            # Remove items commonly found in code examples
            code = code.replace(">>>", "").replace("...", "").strip()
        except:
            code = "NONE"
    else:
        code = "NONE"
    return code


# ---------------------------------------------------------------------------------------------
# WEB CONTAINS
def web_contains(soup, search_words):
    found_word = False
    # Get all text from web page
    web_text = soup.get_text()
    # Add each word to new list
    search_words_list = search_words.rsplit(" , ")
    # Check if each word in list is also in the web page
    if any(word in web_text for word in search_words_list):
        # If it does, then found word is true
        found_word = True
    # Else it is false
    return found_word


# ---------------------------------------------------------------------------------------------
# DEFINITIONS
def url_definitions(soup, def_id, def_class):
    # If user has entered the definition ID name
    if def_id:
        try:
            definition = soup.find("div", {"id": def_id}).p.text
            # Remove [] found within some descriptions in wikipedia
            definition = re.sub('\[.*?\]', '', definition).replace('\n', ' ')
        except:
            definition = "NONE"
    # If user has entered the definition CLASS name
    elif def_class:
        try:
            definition_list =[]
            # Find all instances of the class and add to a list
            for p in soup.find("div", {"class": def_class}).parent.find_all("p"):
                p = p.getText().encode('utf-8').decode('utf-8').replace("\n", " ")
                definition_list.append(p)
            # Convert list to a string and improve it's clarity
            definition = ' '.join(definition_list)
            definition = re.sub('\[.*?\]', '', definition).replace("  ", " ")
            # Limit length of string to 400 characters
            if len(definition) > 400:
                definition_trim = (len(definition) - 397)
                definition = definition[:-definition_trim]
                definition += "..."
        except:
            definition = "NONE"
    else:
        definition = "NONE"
    return definition