import requests
import time
from bs4 import BeautifulSoup
from datetime import date
import random
import logging
from ..config.config import *


def get_data():
    url="https://www.animenewsnetwork.com/news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    main_feed = soup.find('div', class_="mainfeed-section herald-boxes")
    articles = main_feed.find_all('div', class_="herald box news t-news")

    articles = articles[:5]
    data = []
    titles = []
    links = []
    image_thumbnails = []
    contents = []

    for article in articles:
        title = article.find('h3').text.replace('\n', '')
        titles.append(title)
        urls = article.find_all('a', href=True)
        for url in urls:
            if "/news/" in url['href']:
                article_url = "https://www.animenewsnetwork.com" + url['href']
                break
        links.append(article_url)
        image_url = "https://cdn.animenewsnetwork.com" + article.find('div', class_="thumbnail lazyload")['data-src']
        image_thumbnails.append(image_url)
        response = requests.get(article_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        main_feed = soup.find('div', class_="meat")
        main_content = main_feed.find_all('p')
        content = "".join([item.text + "<br>" for item in main_content])
        contents.append(content)
        time.sleep(1)

    data.append(titles)
    data.append(links)
    data.append(image_thumbnails)
    data.append(contents)
    return data

def get_related_keywords(article_title):
    query = article_title + " related keywords"
    url = f"https://www.google.com/search?q={query}"
    related_keywords = []
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    div_elements = soup.find_all('div', class_="BNeawe vvjwJb AP7Wnd")
    for div_element in div_elements:
        related_keyword = div_element.text
        if related_keyword not in related_keywords:
            related_keywords.append(related_keyword)

    return related_keywords

def choose_random_pickup_line():
    pickup_lines = [
        "Enhance your anime journey with our handpicked selection of products. :",
        "Discover the perfect anime merchandise to express your fandom. :",
        "Immerse yourself in the world of anime with our curated collection. :",
        # Add the rest of your pickup lines here...
    ]
    return """<br><br> <h3>{}</h3> <br> [products limit="4" columns="4" orderby="rand" order="rand" visibility="visible"]""".format(random.choice(pickup_lines))


def Paraphrasing_Tool_API(article_content):
    # Paraphrasing Tool By Healthy Tech
    # 5 req/day
    # 40% plagrism
    url = "https://paraphrasing-tool1.p.rapidapi.com/api/rewrite"

    payload = { "sourceText": article_content }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": PARAPHRASING_BY_HEALTHY_TECH_API_KEY,
        "X-RapidAPI-Host": "paraphrasing-tool1.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()['newText']



def Rewriter_Paraphraser_API(article_content):
    # Rewriter Paraphraser By NLP Hub
    # 100 req / month
    # after testing found 56% plagrism

    url = "https://rewriter-paraphraser1.p.rapidapi.com/rewrite"

    payload = { "text": article_content}
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": PARAPHRASING_BY_NEURAL_NETWORK_API_KEY,
        "X-RapidAPI-Host": "rewriter-paraphraser1.p.rapidapi.com"
    }

    response = requests.post(url, data=payload, headers=headers)

    return response.json()['paraphrase']



def Plagiarism_Remover_API(article_content):
    # 5 req/day
    # 45% plagrism

    url = "https://plagiarism-remover.p.rapidapi.com/api/rewrite"

    payload = { "sourceText": article_content }
    headers = {
        "content-type": "application/json",
        "Content-Type": "application/json",
        "X-RapidAPI-Key": PLAGIARISM_REMOVER_BY_HEALTHY_TECH_API_KEY,
        "X-RapidAPI-Host": "plagiarism-remover.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()['NewText']




# Helper function to check the current date
def get_current_date():
    return date.today().strftime('%Y-%m-%d')

def api_call(article_content, api_call_record_file_path):
    # Check the number of API calls made today
    current_date = get_current_date()
    api_calls_today = {'primary': 0, 'alternate': 0, 'alternate2': 0}  # Initialize the counters

    # Load the counters from a file if it exists
    try:
        with open(api_call_record_file_path, 'r') as counter_file:
            saved_date, primary_calls, alternate_calls, alternate2_calls = counter_file.read().split(',')

            if saved_date == current_date:
                api_calls_today['primary'] = int(primary_calls)
                api_calls_today['alternate'] = int(alternate_calls)
                api_calls_today['alternate2'] = int(alternate2_calls)
            else:
                # Reset the counters if it's a new day
                api_calls_today = {'primary': 0, 'alternate': 0, 'alternate2': 0}
    except FileNotFoundError:
        pass

    if api_calls_today['primary'] < 3:
        # making call to primary API
        rewritten_content = Paraphrasing_Tool_API(article_content)
        logging.info(f"Primary API Called: {api_calls_today['primary']}")
        api_calls_today['primary'] += 1

        # Save the updated counters to a file
        with open(api_call_record_file_path, 'w') as counter_file:
            counter_file.write(
                f"{current_date},{api_calls_today['primary']},{api_calls_today['alternate']},{api_calls_today['alternate2']}")

        # Process the API response
        # TODO: Add your code here

    elif api_calls_today['alternate'] < 3:
        # Make a call to the alternate API
        rewritten_content = Plagiarism_Remover_API(article_content)
        logging.info(f"Alternate API Called: {api_calls_today['alternate']}")
        api_calls_today['alternate'] += 1

        # Save the updated counters to a file
        with open(api_call_record_file_path, 'w') as counter_file:
            counter_file.write(
                f"{current_date},{api_calls_today['primary']},{api_calls_today['alternate']},{api_calls_today['alternate2']}")

        # Process the alternate API response
        # TODO: Add your code here

    elif api_calls_today['alternate2'] < 10:
        # Making Call to final alternative API
        rewritten_content = Rewriter_Paraphraser_API(article_content)
        logging.info(f"Alternate2 API Called: {api_calls_today['alternate2']}")
        api_calls_today['alternate2'] += 1

        # Save the updated counters to a file
        with open(api_call_record_file_path, 'w') as counter_file:
            counter_file.write(
                f"{current_date},{api_calls_today['primary']},{api_calls_today['alternate']},{api_calls_today['alternate2']}")

    else:
        logging.info("All APIs have reached the daily limit.")

    return rewritten_content