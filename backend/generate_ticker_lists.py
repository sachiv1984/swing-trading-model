import urllib.request
from bs4 import BeautifulSoup
import csv


def fetch_sp500():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    html = urllib.request.urlopen(req).read()

    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"id": "constituents"})

    rows = table.find_all("tr")
    tickers = []

    for row in rows[1:]:
        cols = row.find_all("td")
        if len(cols) > 0:
            ticker = cols[0].text.strip()
            name = cols[1].text.strip()

            if ticker == "BRK.B":
                ticker = "BRK-B"
            if ticker == "BF.B":
                ticker = "BF-B"

            tickers.append((ticker, name))

    return tickers


def fetch_ftse100():
    url = "https://en.wikipedia.org/wiki/FTSE_100_Index"

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html, "html.parser")

    tables = soup.find_all("table", {"class": "wikitable"})
    tickers = []

    for table in tables:
        header_text = " ".join([th.get_text(" ", strip=True) for th in table.find_all("th")]).lower()

        if "company" not in header_text or "ticker" not in header_text:
            continue

        rows = table.find_all("tr")

        for row in rows[1:]:
            cols = row.find_all("td")
            if len(cols) < 2:
                continue

            # FTSE table layout is: Company | Ticker | Sector
            company = cols[0].get_text(" ", strip=True)
            epic = cols[1].get_text(" ", strip=True).upper()

            # Fix common formatting issues
            epic = epic.replace(".", "").strip()

            # Allow hyphenated tickers like BT-A
            if not epic.replace("-", "").isalpha():
                continue

            # Add .L suffix
            if not epic.endswith(".L"):
                epic = epic + ".L"

            tickers.append((epic, company))

        if tickers:
            break

    print("UK tickers found:", len(tickers))
    return tickers

def main():
    sp500 = fetch_sp500()
    ftse100 = fetch_ftse100()

    combined = sp500 + ftse100

    with open("tickers_full_list.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Ticker", "Exchange", "Name", "Notes"])
        for ticker, name in combined:
            exchange = "LSE" if ticker.endswith(".L") else "NASDAQ"
            writer.writerow([ticker, exchange, name, ""])

    print("Generated tickers_full_list.csv with", len(combined), "tickers.")


if __name__ == "__main__":
    main()