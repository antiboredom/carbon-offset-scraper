import json
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests

from data import OffsetProject

PROJECT_FILE = "data/gold_standard/projects.json"
FINAL = "data/gold_standard.csv"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/112.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    # 'Accept-Encoding': 'gzip, deflate, br',
    "Origin": "https://registry.goldstandard.org",
    "Connection": "keep-alive",
    "Referer": "https://registry.goldstandard.org/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}


def get_list(outname=PROJECT_FILE):
    items = []
    page = 1
    while True:
        try:
            print("page", page)
            params = {
                "query": "",
                "page": page,
                "size": "100",
                "sortColumn": "",
                "sortDirection": "",
            }

            response = requests.get(
                "https://public-api.goldstandard.org/projects",
                params=params,
                headers=headers,
            )

            _items = response.json()
            items += _items

            page += 1
            if len(_items) == 0:
                break
        except Exception as e:
            print(e)
            pass

    with open(outname, "w") as outfile:
        json.dump(items, outfile)


def get_summaries():
    with open(PROJECT_FILE, "r") as infile:
        projects = json.load(infile)
    ids = [p["id"] for p in projects]

    def get_detail(pid):
        print(pid)
        r = requests.get(
            f"https://public-api.goldstandard.org/projects/{pid}/credits/summary",
            headers=headers,
        )
        with open(f"data/gold_standard/details/{pid}_summary.json", "w") as outfile:
            json.dump(r.json(), outfile)

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(get_detail, ids)


def get_details():
    with open(PROJECT_FILE, "r") as infile:
        projects = json.load(infile)
    ids = [p["id"] for p in projects]

    def get_detail(pid):
        print(pid)
        r = requests.get(
            f"https://public-api.goldstandard.org/projects/{pid}",
            headers=headers,
        )
        with open(f"data/gold_standard/details/{pid}_details.json", "w") as outfile:
            json.dump(r.json(), outfile)

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(get_detail, ids)


def merge():
    out = []

    with open(PROJECT_FILE, "r") as infile:
        projects = json.load(infile)

    for p in projects:
        pid = p["id"]
        with open(f"data/gold_standard/details/{pid}_details.json", "r") as infile:
            details = json.load(infile)
        with open(f"data/gold_standard/details/{pid}_summary.json", "r") as infile:
            summary = json.load(infile)

        total = 0
        retired = 0

        for item in summary:
            for i in item["summary"]:
                if i["status"] == "ISSUED":
                    total += i["total"]
                elif i["status"] == "RETIRED":
                    retired += i["total"]

        project = OffsetProject(
            registry_id=p["id"],
            total_credits=total,
            # retired_credits=retired,
            description=details["description"],
            status=p["status"],
            registry_url=f"https://registry.goldstandard.org/projects/details/{pid}",
            developer=p["project_developer"],
            project_type=p["type"],
            methodology=p["methodology"],
            location=p["country"],
            name=p["name"],
            registry="gold_standard",
        )

        out.append(project.dict())

    out = pd.DataFrame.from_records(out)
    out.to_csv(FINAL, index=False)
    return out


def run():
    get_list()
    get_details()
    get_summaries()
    merge()


if __name__ == "__main__":
    # get_list()
    # get_details()
    # get_summaries()
    merge()
