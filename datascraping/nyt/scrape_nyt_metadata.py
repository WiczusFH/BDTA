import requests
import json
from selenium import webdriver
import time
from bs4 import BeautifulSoup

key= "MVvUiiTqWWrVjMNLQlLwrAtaKPQnGyJm"

year=2022
for month in range(1,13):
    request=f"https://api.nytimes.com/svc/archive/v1/{year}/{month}.json?api-key={key}"
    response = requests.get(request).json()
    # selected_fields = ['abstract', 'web_url', 'snippet','pub_date']
    selected_fields = ['web_url','pub_date']
    response = [{field: item[field] for field in selected_fields} for item in response['response']['docs']]
    with open(f'nyt_metadata_{month}.json', 'w') as file:
        json.dump(response, file)






