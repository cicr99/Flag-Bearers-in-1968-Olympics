import requests, os
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs


def main():
    pages_dir = "pages/bearers/"
    next_page = "Next 500 results"
    wiki = "https://en.wikipedia.org/"
    prefix = "List of flag bearers for"
    basic_wiki_query = "/w/index.php?title=Special:Search&limit=500&offset=0&profile=default&search=List_of_flag_bearers&advancedSearch-current={}&ns0=1"
    
    os.makedirs(pages_dir, exist_ok=True)

    def valid_tags(tag):
        return tag.name == 'a' and tag.has_attr('title') and (tag['title'][:len(prefix)] == prefix or tag['title'] == next_page)

    pages = [basic_wiki_query]
    while len(pages):
        page = pages.pop(0)
        req = requests.get(urljoin(wiki, page))
        soup = bs(req.content, 'lxml')
        tags = soup.findAll(valid_tags)

        for tag in tags:
            title, link = tag['title'], tag['href']
            if title == next_page:
                pages.append(link)
            else:
                file_name = link.split('/')[-1]
                req = requests.get(urljoin(wiki, link))
                with open(f'{pages_dir}{file_name}.html', 'w') as fd:
                    fd.write(req.text)


if __name__ == "__main__":
    main()