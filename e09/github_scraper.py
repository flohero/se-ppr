import json
import re

import requests as requests
from bs4 import BeautifulSoup

base_url = "https://github.com"


def scrape_github_org(url: str):
    if base_url not in url:
        raise ValueError(f"{url} is not a github link")

    org = BeautifulSoup(requests.get(url).text, "html.parser")
    _throw_if_not_org(org)
    data = {
        "title": _get_title(org),
        "languages": _get_org_languages(org),
        "member_count": len(_get_members(url)),
        "repositories": _get_repositories(url)
    }
    return data


def _get_title(org: BeautifulSoup):
    title = org.find("main").find("header").find("h1")
    return title.get_text().strip()


def _get_org_languages(org: BeautifulSoup) -> list[str]:
    lang_container = org.find("h4", text="Top languages").parent
    langs = lang_container.find_all("a")
    return [lang.get_text().strip() for lang in langs]


def _get_members(url: str):
    member_url = f"{url.replace(base_url, f'{base_url}/orgs')}/people"
    peoples = []
    id_regex = re.compile("member-.*")

    while member_url is not None:
        people_container = BeautifulSoup(requests.get(member_url).text, "html.parser")
        people_list = people_container.find("div", {"id": "org-members-table"}).find_all("li")
        peoples += [person.find("a", id=id_regex).get_text().strip() for person in people_list]
        member_url = _pagination_next_url(people_container)
    return peoples


def _get_repositories(url):
    repos_url = f"{url.replace(base_url, f'{base_url}/orgs')}/repositories"
    repos = []
    while repos_url is not None:
        print(repos_url)
        repo_container = BeautifulSoup(requests.get(repos_url).text, "html.parser")
        repo_list = repo_container.find("div", {"id": "org-repositories"}).find_all("li")
        repo_urls = [base_url + repo.find("h3").find("a")["href"] for repo in repo_list]
        repos += [_get_repository(repo) for repo in repo_urls]
        repos_url = _pagination_next_url(repo_container)

    return repos


def _get_repository(url):
    print(url)
    repo = BeautifulSoup(requests.get(url).text, "html.parser")

    name = repo.find("h1").find("strong").get_text().strip()

    meta_info = repo.find("div", {"class": "BorderGrid BorderGrid--spacious"})

    about_heading = meta_info.find("h2", text="About")
    about_tag = about_heading.find_next_sibling("p") if about_heading is not None else None
    about = about_tag.get_text().strip() if about_tag is not None else None

    lang_heading = meta_info.find("h2", text="Languages")
    langs = lang_heading.parent.find_all("li") if lang_heading is not None else None
    languages_with_share = [{
        "language": lang.find_next("span", {"class": "color-fg-default text-bold mr-1"}).get_text().strip(),
        "share": lang.find_next("span", {"class": ""}).get_text().strip()
    } for lang in langs] if langs is not None else []

    topic_headline = meta_info.find("h3", text="Topics")
    topics = []

    if topic_headline is not None:
        topic_links = topic_headline.find_next_sibling("div").find_all("a")
        topics = [topic.get_text().strip() for topic in topic_links]

    stars = repo.find("span", {"id": "repo-stars-counter-star"}).get_text().strip()
    forks = repo.find("span", {"id": "repo-network-counter"}).get_text().strip()
    watchers = meta_info.find("h3", text="Watchers").find_next_sibling("div").find("strong").get_text().strip()

    main = repo.find("div", {"class": "Layout-main"})
    repo_bar = main.find_next("div", {"class": "file-navigation mb-3 d-flex flex-items-start"})

    branch_tag = repo_bar.find("span", text="branches")
    branches = branch_tag.parent.find("strong").get_text().strip() if branch_tag is not None else repo_bar \
        .find("span", text="branch").parent.find("strong").get_text().strip()

    tag_span = repo_bar.find("span", text="tags")
    tags = tag_span.parent.find("strong").get_text().strip() if tag_span is not None else repo_bar \
        .find("span", text="tag").parent.find("strong").get_text().strip()

    time_tag = main.find("h2", text="Latest commit").parent.find("relative-time")
    last_updated = time_tag["datetime"] if time_tag is not None else None

    return {
        "name": name,
        "about": about,
        "languages": languages_with_share,
        "stars": stars,
        "watchers": watchers,
        "forks": forks,
        "branches": branches,
        "tags": tags,
        "last_updated": last_updated,
        "topics": topics
    }


def _pagination_next_url(pagination_container: BeautifulSoup):
    pagination = pagination_container.find("div", {"class": "pagination"}).find("a", {"class": "next_page"})
    return (base_url + pagination["href"]) if pagination is not None else None


def _throw_if_not_org(org: BeautifulSoup):
    org_schema = org.find("main").find("div", {"itemtype": "http://schema.org/Organization"})
    if org_schema is None:
        raise ValueError("Not an organisation")


if __name__ == "__main__":
    with open("dotnet.json", "w") as file:
        d = (scrape_github_org("https://github.com/dotnet/"))
        json.dump(d, file, indent=4, ensure_ascii=False)

