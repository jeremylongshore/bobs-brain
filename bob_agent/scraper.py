import scrapy
from scrapy.crawler import CrawlerProcess

class WebSpider(scrapy.Spider):
    name = "web_spider"
    def __init__(self, url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [url]
    def parse(self, response):
        content = response.css('p::text').getall()
        cleaned_content = ' '.join(content).strip()
        yield {'content': cleaned_content}

def scrape_url(url):
    try:
        process = CrawlerProcess({'USER_AGENT': 'Mozilla/5.0'})
        results = []
        def collect_results(item, response, spider):
            results.append(item)
        process.crawl(WebSpider, url=url, callback=collect_results)
        process.start()
        return results[0]['content'] if results else "No content found."
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"
