import re
import easygui
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def scrape_and_display(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        paragraphs = soup.find_all('p')

        print('-------------------')
        for paragraph in paragraphs:
            text = paragraph.get_text(strip=True)
            if text:
                formatted_text = re.sub(r'\.(\s|$)', '.\n', text)
                print(formatted_text)

    except requests.exceptions.RequestException as e:
        print("An error occurred while making the request:", e)

def extract_urls_from_site(site_url):
    try:
        response = requests.get(site_url)
        soup = BeautifulSoup(response.text, "lxml")
        links = soup.find_all('a', href=True)
        urls = [link['href'] for link in links if link['href'].startswith('http')]

        return urls
    except requests.exceptions.RequestException as e:
        print("An error occurred while making the request:", e)
        return []

site_urls = ["https://nascecresceignora.it/", "https://www.everyeye.it/"]
site_names = [urlparse(url).hostname.replace("www.", "").split(".")[0] for url in site_urls]

site_names.append("Enter custom URL...")  # Add option to enter a custom URL

selected_site = easygui.choicebox("Select the website to scrape:", "Website Selection", choices=site_names)

if selected_site == "Enter custom URL...":
    site_url = easygui.enterbox("Try your luck!:")
    if not site_url:
        easygui.msgbox("No website URL entered. Exiting...", "Error")
        exit()
    parsed_url = urlparse(site_url)
    site_name = parsed_url.netloc.replace("www.", "").split(".")[0]
    easygui.msgbox(f"You have entered the website: {site_name}", "Website Selection")
else:
    site_url = site_urls[site_names.index(selected_site)]
    site_name = selected_site
    easygui.msgbox(f"You have selected the website: {site_name}", "Website Selection")

urls = extract_urls_from_site(site_url)

titles = {re.sub(r'\W+', ' ', url): url for url in urls}

selected_title = easygui.choicebox("Select a news title:", "News Titles", choices=list(titles.keys()))

if selected_title:
    selected_link = titles[selected_title]
    scrape_and_display(selected_link)
