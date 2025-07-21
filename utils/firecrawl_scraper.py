import requests

FIRECRAWL_API_KEY = "fc-d052a653e1ba4e2b9d441882403d42a6"

def scrape_website_firecrawl(url: str, output_format: str = "json") -> dict:
    endpoint = "https://api.firecrawl.dev/scrape"
    payload = {"url": url, "format": output_format}
    headers = {"Authorization": f"Bearer {FIRECRAWL_API_KEY}"}
    response = requests.post(endpoint, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Firecrawl API failed: {response.text}")

    return response.json()

