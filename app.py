from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    news_data = []
    error = None
    message = None
    if request.method == "POST":
        try:
            url = "https://www.example.com"  # Test üçün istənilən real sayt yaz
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            headlines = []
            for item in soup.select("h2 a"):
                title = item.get_text(strip=True)
                link = item.get("href")
                headlines.append({"title": title, "link": link})

            if not headlines:
                message = "Xəbər tapılmadı (empty result). CSS selector-u yoxla."

            news_data = headlines

        except Exception as e:
            error = f"Xəta baş verdi: {str(e)}"

    return render_template("index.html", news_data=news_data, error=error, message=message)

if __name__ == "__main__":
    app.run(debug=True)
