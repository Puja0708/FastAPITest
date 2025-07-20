import requests


def scrape_website_firecrawl(url: str, output_format: str = "json") -> dict:
    endpoint = "https://api.firecrawl.dev/scrape"
    payload = {"url": url, "format": output_format}
    headers = {"Authorization": "Bearer <YOUR_FIRECRAWL_API_KEY>"}
    response = requests.post(endpoint, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Firecrawl API failed: {response.text}")

    return response.json()
