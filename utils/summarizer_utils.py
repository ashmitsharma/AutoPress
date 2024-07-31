import requests
from..config.config import SUMMARIZER_API_KEY

def summarize(full_content):
    url = "https://summarizer8.p.rapidapi.com/"
    payload = {
        "url": full_content,
        "sentenceCount": "6"
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": SUMMARIZER_API_KEY,
        "X-RapidAPI-Host": "summarizer8.p.rapidapi.com"
    }
    response = requests.post(url, json=payload, headers=headers)
    important_points = response.json()['Summary'].split('.')
    important_points = [point for point in important_points if point]
    important_points = [point.strip() + "." for point in important_points]
    rechecked_important_points = [item for item in important_points if len(item.split()) > 4]
    return rechecked_important_points
