import requests
from bs4 import BeautifulSoup

url = "https://arxiv.org"
topic = "/list/cs.LG/recent"
# topic = "/list/cs.LG/pastweek?show=795"

def get_papers(url, topic):
    page = requests.get(url + topic)
    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find(id="content")
    links = results.find_all("a", {"title": "Abstract"}, href=True)
    titles = results.find_all("div", {"class": "list-title"})

    info = []
    for title, link in zip(titles, links):
        title.find("span").extract()

        paper = requests.get(url + link['href'])
        soup = BeautifulSoup(paper.content, "html.parser")
        authors = soup.find("div", {"class": "authors"})
        authors.find("span").extract()

        abstract = soup.find("blockquote", {"class": "abstract"})
        abstract.find("span").extract()

        info.append(title.text[2:-1] + '\n\n' +
                    "Paper: " + url + link['href'] + '\n\n' +
                    "Authors: " + authors.text + ')\n\n' +
                    abstract.text[3:-6].replace('\n', ' '))

        if len(info) == 5:
            break

    return info