from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
# from openai import OpenAI

# def get_openai_client():
#     return OpenAI(
#         base_url = 'http://localhost:11434/v1',
#         api_key='ollama', # required, but unused
#     )

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

        if paragraphs:
            paragraphs = "\n\n".join([line.strip() for line in paragraphs if line.strip()])
        else:
            paragraphs = None
        return paragraphs
    except requests.RequestException as e:
        print(f"Failed to fetch data from {e}")
        return None



def extract_content_summary(content=""):
    # client = get_openai_client()

    system_prompt = "".join([
        "You are an expert web scraper and researcher.",
        "When you get data, you perform expert-level summarization.",
    ])
    prompt_start = "".join([
        "Provide a concise summary of the contents of the text",
        "The summary should not include anything related to the discussion nature of the text.",
        "The summary should not include anything related to the conversation nature of the text.",
        "The summary should be a minimum 3 paragraphs.",
        "Use the following text: "
    ])
    prompt_end="Using format of \"<generated-summary>\" return a response with paragraph"
    messages=[
        {"role": "system", "content": system_prompt},
        {
            "role": "user", 
            "content": f"{prompt_start} {content} {prompt_end}",
        }
    ]
    # summary = client.chat.completions.create(
    #   model="llama3.2",
    #   messages=messages,
    # )
    return messages
