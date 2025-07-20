from firecrawl_scraper import scrape_website_firecrawl
from firestore_utils import store_scraped_data

def scrape_and_store_website(url: str, workflow_id: str):
    data = scrape_website_firecrawl(url)
    store_scraped_data(workflow_id, data)
    return data
