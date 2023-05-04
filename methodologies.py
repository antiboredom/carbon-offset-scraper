import json
import re

import requests
from bs4 import BeautifulSoup

FINAL = "data/verra_methodologies.json"


def get_description(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    desc = soup.select_one(".methodologies-detail").text.strip()
    return desc


def run():
    """
    Downloads methodologies from verra
    """

    out = []

    r = requests.get("https://verra.org/methodologies-main/")
    soup = BeautifulSoup(r.text, "html.parser")
    sections = soup.select(".accordionGroup_wrapper")

    for s in sections:
        category = s.select_one(".accordion-title").text.strip()
        methods = s.select("p a")
        for m in methods:
            url = m.attrs.get("href", "")
            if not url.startswith("https://verra.org"):
                url = "https://verra.org" + url
            t = m.text.strip()
            version = None
            v_matches = re.search(r", v([0-9.]+)$", t)
            if v_matches:
                version = v_matches.groups(0)[0]
                t = re.sub(r", v([0-9.]+)$", "", t)
            desc = get_description(url)
            item = {
                "name": t,
                "url": url,
                "version": version,
                "category": category,
                "description": desc,
            }
            out.append(item)

    with open(FINAL, "w") as outfile:
        json.dump(out, outfile, indent=2)


if __name__ == "__main__":
    run()
