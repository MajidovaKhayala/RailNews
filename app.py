from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_news():
    urls = [
        "https://az.trend.az/",  # nümunə saytlar
        "https://apa.az/"
    ]
    news_results = []

    headers = {"User-Agent": "Mozilla/5.0"}

    for url in urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Sadə nümunə: h2 headline linkləri götürürük
            headlines = []
            for a in soup.select("h2 a, h3 a"):
                title = a.get_text(strip=True)
                link = a.get("href")
                if title and link:
                    if not link.startswith("http"):
                        link = url.rstrip("/") + "/" + link.lstrip("/")
                    headlines.append({"title": title, "link": link})

            news_results.append({"url": url, "headlines": headlines})
        except Exception as e:
            news_results.append({"url": url, "headlines": [], "error": str(e)})

    return news_results

@app.route("/", methods=["GET", "POST"])
def index():
    news_data = []
    if request.method == "POST":
        news_data = scrape_news()
    return render_template("index.html", news_data=news_data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
