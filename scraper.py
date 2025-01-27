import re
import requests
from bs4 import BeautifulSoup

def get_all_pages():
    urls = []
    page_number = 1
    for i in range(105):
        i = f"https://www.barreaudenice.com/annuaire/avocats/?fwp_paged={page_number}"
        page_number += 1
        urls.append(i)
    return urls

def parse_attorney(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    avocats = soup.find_all("div", class_="callout secondary annuaire-single")
#la boucle for nous  permis de parcourir dans chaque avocat pour prende son nom, adresse, etc..
    for avocat in avocats:
        try:
            nom = avocat.find("h3").text.strip()
        except AttributeError as e:
            nom = ""

        adresse = avocat.find("span", class_="adresse").text.strip()
        try:
            adresse_propre = re.sub(r"\s+", " ", adresse)
        except AttributeError as e:
            adresse_propre = ""
        try:
            telephone = avocat.find("span", class_="telephone").text.strip()
        except AttributeError as e:
            telephone = ""
        try:
            email = avocat.find("a").text.strip()
        except AttributeError as e:
            email = ""

        chemin = r"C:\Users\User\Documents\scraping\annuaire.csv"
        with open(chemin, "a") as f:
            f.write(f"{nom}\n")
            f.write(f"{adresse_propre}\n")
            f.write(f"{telephone}\n")
            f.write(f"{email}\n\n")

def perse_all_attorney():
    pages = get_all_pages()
    for page in pages:
        parse_attorney(url=page)
        print(f"on scrape {page}")
perse_all_attorney()