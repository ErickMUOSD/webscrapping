import json
import os
from typing import List, Dict

from scrapfly import ScrapflyClient, ScrapeConfig, ScrapeApiResponse
from loguru import logger as log
from parsel import Selector
from dynamo.products import save_product_data


async def scrape_products_scrapfly(urls: List[str], ):
    """scrape Walmart product pages"""
    log.info(f"scraping {len(urls)} products from Walmart")
    client = ScrapflyClient(key=os.environ.get("SCRAPFLY_API_KEY"))

    results = []
    for url in urls:
        log.info(f"scraping {url}")
        api_result =  client.scrape(ScrapeConfig(
            url=url,
            asp=True,
        ))
        if api_result.status_code == 200:
            results.append(parse_product_walmart(api_result.content))

    for result in results:
        print(result)
        obj = extract_product_data(result)
        save_product_data(obj)

    return results
def extract_product_data(product: Dict) -> Dict:
    id = product["product"]["id"]
    availability_status = product["product"]["availabilityStatus"]
    price = product["product"]["priceInfo"]["currentPrice"]["price"]
    name = product["product"]["name"]
    return {
        "id": id,
        "availability_status": availability_status,
        "current_price": price,
        "name": name,
        "type": product["type"]
    }

def parse_product_walmart(html_text: str) -> Dict:
    """parse walmart product"""
    sel = Selector(text=html_text)
    data = sel.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
    data = json.loads(data)
    _product_raw = data["props"]["pageProps"]["initialData"]["data"]["product"]
    # There's a lot of product data, including private meta keywords, so we need to do some filtering:
    wanted_product_keys = [
        "availabilityStatus",
        "averageRating",
        "brand",
        "id",
        "imageInfo",
        "manufacturerName",
        "name",
        "orderLimit",
        "orderMinLimit",
        "priceInfo",
        "shortDescription",
        "type",
    ]
    product = {k: v for k, v in _product_raw.items() if k in wanted_product_keys}
    reviews_raw = data["props"]["pageProps"]["initialData"]["data"]["reviews"]
    return {"product": product, "reviews": reviews_raw, "type" :"walmart"}

