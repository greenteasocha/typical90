import sys
import urllib.request
import requests
from collections import defaultdict
from typing import *
from bs4 import BeautifulSoup

import json

url = 'https://atcoder.jp/'
url_login = 'https://atcoder.jp/login'
url_submissions = 'https://atcoder.jp/contests/typical90/submissions/me'


def login() -> requests.session:
    session = requests.session()

    # csrf_token取得
    r = session.get(url_login)
    s = BeautifulSoup(r.text, "html.parser")
    csrf_token = s.find(attrs={'name': 'csrf_token'}).get('value')

    login_info = {
        "csrf_token": csrf_token,
        "username": USERNAME,
        "password": PASSWORD
    }

    result = session.post(url_login, data=login_info)
    result.raise_for_status()
    if result.status_code == 200:
        print("log in!")
    else:
        print("failed...")

    return session


def get_all_submissions(session: requests.session) -> List:
    """
    return submission table (not contained a header column)
    """
    r = session.get(url_submissions)
    s = BeautifulSoup(r.text, "html.parser")

    found = s.find('div', class_='table-responsive')
    table = found.findAll("table", {"class": "table"})[0]

    rows = table.findAll("tr")

    return rows[1:]


def parse_problem(problem: str) -> int:
    """
    extract problem number
    """
    return int(problem[:3])


def summarize_table(rows: List):
    # res = defaultdict(defaultdict)
    res = defaultdict(str)
    for row in rows:
        cells = row.findAll("td")
        problem = cells[1].text
        problem_number = parse_problem(problem)
        # language = cells[3].text
        status = cells[6].text
        if status == "AC":
            # res[problem_number][language] = "AC"
            res[problem_number] = "AC"
        else:
            # if res[problem_number][language] != "AC":
            if res[problem_number] != "AC":
                # res[problem_number][language] = "non-AC"
                res[problem_number] = "non-AC"

    return res

def write_markdown(summarized):
    lines = []
    lines.append("See: https://atcoder.jp/contests/typical90 \n")
    lines.append("|  Problem  |  Status  |\n")
    lines.append("| ---- | ---- |\n")
    for i in range(90):
        number = i + 1
        if summarized[number] == "AC":
            status = ":heavy_check_mark:"
        elif summarized[number] == "non-AC":
            status = ":x:"
        else:
            status = ""
        lines.append("| {} | {} |\n".format(number, status))

    with open("README.md", "w") as f:
        f.writelines(lines)

    return

def main():
    session = login()
    submissions = get_all_submissions(session)
    summarized = summarize_table(submissions)
    write_markdown(summarized)

if __name__ == "__main__":
    USERNAME, PASSWORD = sys.argv[1:]
    main()

# ref
# session and login
# https://www.smartbowwow.com/2018/09/atcoder.html


