"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36"
}


def scrape_ra_events(city: str):

    formatted_city = city.lower().replace(" ", "")
    url = f"https://ra.co/ra-guide/{formatted_city}"

    response = requests.get(url, headers=HEADERS, timeout=10)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    events = []
    event_cards = soup.select("div.guide-event")  # selector real de RA

    for card in event_cards:
        # título
        title_tag = card.select_one("h3.title")
        title = title_tag.get_text(strip=True) if title_tag else "Unknown event"

        # venue
        venue_tag = card.select_one("span.venue")
        venue = venue_tag.get_text(strip=True) if venue_tag else "Unknown venue"

        # fecha
        date_tag = card.select_one("span.date")
        date_raw = date_tag.get_text(strip=True) if date_tag else "Unknown date"

        # URL
        link_tag = card.select_one("a")
        url = "https://ra.co" + link_tag["href"] if link_tag else ""

        events.append({
            "title": title,
            "venue": venue,
            "date": date_raw,
            "url": url
        })

    return events
"""