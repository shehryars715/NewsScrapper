from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_dawn():
    url = "https://www.dawn.com/latest-news"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.find_all("article", class_="story")
    news_list = []

    for article in articles:
        title_tag = article.find("h2", class_="story__title")
        title = title_tag.get_text(strip=True) if title_tag else None
        link_tag = title_tag.find("a") if title_tag else None
        link = link_tag["href"] if link_tag else None
        excerpt_tag = article.find("div", class_="story__excerpt")
        excerpt = excerpt_tag.get_text(strip=True) if excerpt_tag else None
        img_tag = article.find("img")
        image_url = img_tag.get("data-src") or img_tag.get("src") if img_tag else None
        time_tag = article.find("span", class_="timestamp--time")
        timestamp = time_tag.get("title") if time_tag else None
        time_text = time_tag.get_text(strip=True) if time_tag else None

        if title and link and image_url and timestamp:
            news_list.append({
                "title": title,
                "link": link,
                "excerpt": excerpt if excerpt else "",
                "image": image_url,
                "timestamp": timestamp,
                "time_text": time_text
            })
    return news_list

@app.route("/")
def index():
    news_data = scrape_dawn()
    return render_template("index.html", news_data=news_data)

if __name__ == "__main__":
    app.run(debug=True)
