from bs4 import BeautifulSoup
import requests
import re
import hashlib
import json

url = "https://www.wienzufuss.at/blog/"
r = requests.get(url)
doc = BeautifulSoup(r.text, "html.parser")

divs = doc.find_all("div", {"class": "post"})
blog = {}
cont = True
while cont:
    for d in divs:
        link = d.find("h2").find("a").get("href")
        header = d.find("h2").find("a").text.strip()
        comments = re.sub("[^[0-9]", "", d.find(text=re.compile("Kommentar")))
        comments = int(comments) if comments else 0

        meta = d.find("div", {"class": "post-meta"})
        categories = [cat.text.strip() for cat in meta.find_all("a", {"rel": "category"})]
        author = meta.find("a", {"rel": "author"}).text.strip()

        blog_entry = BeautifulSoup(requests.get(link).text, "html.parser")
        content = blog_entry.find("div", {"class": "text"})

        headings = [heading.text.strip() for heading in content.find_all("h2")]
        headings = [heading for heading in headings if heading != ""]

        link_count = len(content.find_all("a"))
        pic_count = len(content.find_all("img"))
        word_count = len(content.text.strip().split(" "))

        blog[hashlib.md5(header.encode()).hexdigest()[:10]] = {
            "link": link,
            "title": header,
            "comments": comments,
            "categories": categories,
            "author": author,
            "headings": headings,
            "#links": link_count,
            "#pictures": pic_count,
            "#words": word_count
        }

    next_page = doc.find("div", {"class": "paging"}).find("a", {"class": "next page-numbers"})
    if next_page is not None:
        cont = True
        doc = BeautifulSoup(requests.get(next_page.get("href")).text, "html.parser")
        print(next_page.get("href"))
    else:
        cont = False

with open("wienzufuss.json", "w") as outfile:
    json.dump(blog, outfile, indent=4, ensure_ascii=False)
