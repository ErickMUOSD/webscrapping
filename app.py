from flask import Flask

from helpers import scrape_products_scrapfly

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/scrap_walmart')
async def scrape_products_from_walmart():  # put application's code here

    await scrape_products_scrapfly(urls=[
        "https://www.walmart.com.mx/ip/00750303766931",
        "https://www.walmart.com.mx/ip/00072679824735"
    ],
)

    return 'Scraped Walmart!'


if __name__ == '__main__':
    app.run()
