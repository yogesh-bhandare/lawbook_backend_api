from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests

def extract_links(url, html, link_cnt=1):
    soup = BeautifulSoup(html, 'html.parser')
    contentarea = soup.find('div', class_='contentarea')
    tables = contentarea.find_all('table')

    json_data = []
    if len(tables) >= link_cnt:
        second_table = tables[3]  
        rows = second_table.find_all('tr')[:link_cnt]  

        for row in rows:
            date_td = row.find('font')  
            link = row.find('a', href=True)
            if date_td and link:
                date = date_td.text.strip()
                href = link['href']
                full_link = urljoin(url, href)
                wid = href.split("WID=")[1] if "WID=" in href else None

                json_data.append({
                    "WID": wid,
                    "date": date,
                    "link": full_link
                })

    return json_data

def scrape_page_content(html):
    try:

        soup = BeautifulSoup(html, 'html.parser')
        
        contentarea = soup.find('div', class_='contentarea')
        if not contentarea:
            return None  # Return None if contentarea is not found

        paragraphs = [p.text.strip() for p in contentarea.find_all('p')]
        return paragraphs
    except requests.RequestException as e:
        print(f"Failed to fetch data from {e}")
        return None
