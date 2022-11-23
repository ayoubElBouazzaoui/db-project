import urllib.request
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.parse import urlparse


def url_ok(url):
    try:
        r = urllib.request.urlopen(url).getcode()
        return r == 200
    except:
        return False

def get_data(url):
    r = requests.get(url)
    return r.text

def get_destination_redirect(page_url):
    redirect = requests.get(page_url).url.replace('www.', '')
    print(redirect)
    return redirect

# create empty dict
dict_href_links = {}
word_exclusion = ['.pdf', 'jpg', '/fr/', '/en/', '/be-fr/', '/be-en/']


def get_links(website_link):
    html_data = get_data(website_link)
    soup = BeautifulSoup(html_data, "html.parser")
    list_links = []
    for link in soup.find_all("a", href=True):
        if not any(word in str(link['href']) for word in word_exclusion):
            # Append to list if new link contains original link
            if str(link["href"]).startswith((str(website_link))):
                list_links.append(get_destination_redirect(link['href']))

            # Include all href that do not start with website link but with "/"
            if str(link["href"]).startswith("/"):
                if link["href"] not in dict_href_links:
                    dict_href_links[link["href"]] = None
                    if website_link.endswith("/"):
                        link_with_www = website_link + link["href"][1:]
                    else:
                        link_with_www = website_link + link["href"]
                    list_links.append(get_destination_redirect(link_with_www))

    # Convert list of links to dictionary and define keys as the links and the values as "Not-checked"
    dict_links = dict.fromkeys(list_links, "Not-checked")
    return dict_links


def get_subpage_links(l):
    for link in l:
        # If not crawled through this page start crawling and get links
        if l[link] == "Not-checked":
            dict_links_subpages = get_links(link)
            # Change the dictionary value of the link to "Checked"
            l[link] = "Checked"
        else:
            # Create an empty dictionary in case every link is checked
            dict_links_subpages = {}
        # Add new dictionary to old dictionary
        l = {**dict_links_subpages, **l}
    return l


def get_all_pages(website):
    # create dictionary of website
    hostname = "http://" + urlparse(website).hostname
    print(hostname)
    dict_links = {hostname:"Not-checked"}

    counter, counter2 = None, 0
    while counter != 0:
        counter2 += 1
        dict_links2 = get_subpage_links(dict_links)
        # Count number of non-values and set counter to 0 if there are no values within the dictionary equal to the string "Not-checked"
        counter = sum(value == "Not-checked" for value in dict_links2.values())
        dict_links = dict_links2

    return dict_links



def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_webpage(webpage):
    body = get_data(webpage)
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


