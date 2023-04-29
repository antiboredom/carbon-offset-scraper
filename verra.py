import json
import os
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests

ISSUANCE_FILE = "data/verra_vcus.csv"
PROJECT_FILE = "data/verra_projects.csv"
DETAILS_FILE = "data/verra_details.json"

COOKIES = {
    "ASPSESSIONIDSEBRTARC": "JNIICHMANPKHCBEAAJLDBOMP",
    "ASPSESSIONIDSGCSRBTC": "GDEDCDJBCNJMCNGOIGKJHEKJ",
    "ASPSESSIONIDCWDQQBRB": "FMKNOKCDOOLCFONAKPLMALPA",
    "ASPSESSIONIDSEQDASRD": "BLACAKIBMEJBLCNFPJBPAKEB",
    "ASPSESSIONIDSGSCATRD": "AOGFNNKCJGCCMIDMGOGBELFG",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/112.0",
    "Accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "Accept-Language": "en-US,en;q=0.5",
    # 'Accept-Encoding': 'gzip, deflate, br',
    "Content-Type": "application/json",
    "Origin": "https://registry.verra.org",
    "Connection": "keep-alive",
    "Referer": "https://registry.verra.org/app/search/VCS?programType=ISSUANCE&exactResId=2939",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
}


def download_issuances_csv(outname=ISSUANCE_FILE):
    """
    Downloads a csv file of all project offset issuances from Verra
    Takes a long time...
    """

    json_data = {
        "program": "VCS",
        "issuanceTypeCodes": [
            "ISSUE",
        ],
    }

    print("Downloading Verra issuances. This may take a while...")

    response = requests.post(
        f"https://registry.verra.org/uiapi/asset/asset/search?$skip=0&count=true&$format=csv&$exportFileName={os.path.basename(outname)}",
        cookies=COOKIES,
        headers=HEADERS,
        json=json_data,
    )

    with open(outname, "wb") as outfile:
        outfile.write(response.content)


def download_projects_csv(outname=PROJECT_FILE):
    """
    Downloads a csv file of all projects from Verra
    Includes projects that have not yet issued credits
    """

    json_data = {
        "program": "VCS",
        "resourceStatuses": [
            "VCS_EX_CRD_PRD_VER_REQUESTED",
            "VCS_EX_CRD_PRD_REQUESTED",
            "VCS_EX_INACTIVE",
            "VCS_EX_ONHOLD",
            "VCS_EX_REGISTERED",
            "VCS_EX_REG_VER_APPR_REQUESTED",
            "VCS_EX_REGISTRATION_REQUESTED",
            "VCS_EX_REJ",
            "VCS_EX_UNDER_DEVELOPMENT_CLD",
            "VCS_EX_UNDER_VALIDATION_CLD",
            "VCS_EX_UNDER_VALIDATION_OPN",
            "VCS_EX_CRED_TRANS_FRM_OTHER_PROG",
            "VCS_EX_WITHDRAWN",
        ],
    }

    response = requests.post(
        f"https://registry.verra.org/uiapi/resource/resource/search?$skip=0&count=true&$format=csv&$exportFileName={os.path.basename(outname)}",
        cookies=COOKIES,
        headers=HEADERS,
        json=json_data,
    )

    with open(outname, "wb") as outfile:
        outfile.write(response.content)


def get_project(pid):
    """
    Gets an individual project details
    """

    response = requests.get(
        f"https://registry.verra.org/uiapi/resource/resourceSummary/{pid}",
        cookies=COOKIES,
        headers=HEADERS,
    )

    results = response.json()
    return results


def get_all_project_details(outname=DETAILS_FILE):
    """
    Scrapes all project details
    """

    # get all the unique project ids
    df = pd.read_csv(PROJECT_FILE)
    ids = df["ID"].unique().tolist()

    print(f"Downloading details for {len(ids)} projects")

    with ThreadPoolExecutor(max_workers=10) as executor:
        all = executor.map(get_project, ids)
        with open(outname, "w") as outfile:
            json.dump(list(all), outfile)


def merge_data():
    """
    merges in data from all sources
    """

    df = pd.read_csv(ISSUANCE_FILE)

    # get rid of commas in numbers
    df["Quantity Issued"] = df["Quantity Issued"].str.replace(",", "").astype(float)

    # summing "Quantity Issued" reflects the total, NOT "Total Vintage Quantity"
    total = df["Quantity Issued"].sum()

    print(total)


def run():
    download_projects_csv()
    download_issuances_csv()
    get_all_project_details()
    merge_data()


if __name__ == "__main__":
    # download_projects_csv()
    # download_issuances_csv()
    get_all_project_details()
    # merge_data()
