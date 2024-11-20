from django.apps import apps
from celery import shared_task
import helpers


@shared_task
def scrape_judgment_url_task(url, cnt):
    if url is None:
        return 
    elif url == "":
        return
    JudgmentScrapeEvent = apps.get_model('judgments', 'JudgmentScrapeEvent')
    # scrape home page and get todays price rate url
    html = helpers.scrape(url)

    # get the link for the next page
    json_links_data = helpers.extract_links(url, html, cnt)

    # scrape main rates page
    for item in json_links_data:
        print(f"Scraping URL: {item['link']}")  
        html = helpers.scrape(item['link'])
        paragraphs = helpers.scrape_page_content(html)
        item["content"] = paragraphs if paragraphs else "No content found"

    JudgmentScrapeEvent.objects.create_scrape_event(json_links_data)
    return


@shared_task
def scrape_judgement_task():
    Judgment = apps.get_model('judgments', 'Judgment')
    qs = Judgment.objects.filter(active=True)
    for obj in qs:
        url = obj.url
        scrape_judgment_url_task.delay(url)

