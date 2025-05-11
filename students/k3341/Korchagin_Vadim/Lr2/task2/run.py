import asyncio
import requests
from bs4 import BeautifulSoup

import threading_
import multiprocessing_
import async_
from db.connection import init_db


def extract_user_links(page_url: str) -> list[str]:
    response = requests.get(page_url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    return [
        "https://habr.com" + a["href"]
        for a in soup.select("a.tm-user-snippet__nickname")
        if a.get("href")
    ]


def run_all():
    init_db()

    base_url = "https://habr.com/ru/users/"
    urls = extract_user_links(base_url)

    if not urls:
        print("No user URLs found.")
        return

    print(f"Parsed {len(urls)} user URLs")
    threading_.main(urls)
    multiprocessing_.main(urls)
    asyncio.run(async_.main(urls))


if __name__ == "__main__":
    run_all()
