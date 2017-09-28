# ---------------------------------------------------------------------------------------------
# Links.py
# Python 3.X required to run
# Created by Julian Smith

links_list_final = []


# ---------------------------------------------------------------------------------------------
# GET LINKS
# Finds every url on the website. user_url = the user inputted url | url = the current url
def get_links(soup, user_url):
    # Find anchor tags that have href's
    links = soup.findAll('a', href=True)
    link_list = []
    link_unwanted = ["#", "?"]
    # Get the url from the anchor tags and remove unwanted items
    for link in links:
        link = link.get('href')
        if link not in link_unwanted:
            link_list.append(link)
    # Add or fix url so that it correctly forms a working url that can be visited
    for i, link in enumerate(link_list):
        if link_list[i].startswith("//"):
            link = user_url + link[1:]
            link_list[i] = link
        if link_list[i].startswith("/"):
            if user_url.endswith("/"):
                link = user_url[:-1] + link
            else:
                link = user_url + link
            link_list[i] = link
        if not (link_list[i].startswith("https://") or link_list[i].startswith("http://")
                  or link_list[i].startswith("#") or link_list[i].startswith("?")):
            if not user_url.endswith("/"):
                user_url += "/"
            link = user_url + link
            link_list[i] = link
    # Only add links that are on the same website, have not already been found, and is not the starting url
    for i, link in enumerate(link_list):
        for i, link in enumerate(link_list):
            # Remove "/" from the end of the urls
            if link_list[i].endswith("/"):
                link_list[i] = link_list[i][:-1]
            if (link_list[i].startswith(user_url)) and (link_list[i] != user_url):
                if link_list[i] not in links_list_final:
                    links_list_final.append(link_list[i])
        return links_list_final
