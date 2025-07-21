from utils.firecrawl_scraper import *
from utils.firestore_utils import *

def scrape_and_store_website(url: str, workflow_id: str):
    data = scrape_website_firecrawl(url)
    store_scraped_data(workflow_id, data)
    return data
