import requests
from bs4 import BeautifulSoup as bs
import re

# faire une requette get sur l'url spécifier grace a la librairy requests
url = "https://www.senscritique.com/liste/100_films_a_voir_absolument/1568551"
response = requests.get(url)

# créer un objet BS pour parser et naviger dans le html récupérer
html = response.content
soup = bs(html, "lxml")

# récupérer tous les titre de film en passant la balise a et la class de la balise
movie_titles = soup.find_all(
    "a", class_="Text__SCText-sc-1aoldkr-0 Link__SecondaryLink-sc-1v081j9-1 kcGHBE jacWTu ProductListItem__StyledProductTitle-sc-1jkxxpj-3 dBFYVt")

# récupérer tous les tréalisateur en passant la balise a et la class de la balise
movie_directors = soup.find_all(
    "a", class_="Text__SCText-sc-1aoldkr-0 Link__PrimaryLink-sc-1v081j9-0 eWSucP bGxijB")

# récupérer les url des images des films
img_movie = soup.find_all("img")

# Créer ine liste de dictionnaires pour stocker les données des films
clear_movies = []

for title in movie_titles:
    clear_title = re.sub(r"[^a-zA-Z\séÉ]", "", title.get_text(strip=True))
    clear_title = clear_title.replace("é", "e")
    clear_title = clear_title.replace("É", "E")
    clear_movies.append(clear_title)


# Parcourir chaque élément img et associer l'URL de l'image au titre du film correspondant
for img in img_movie:
    src = img.get("src")
    if src.startswith("https"):
        clear_url = re.sub(r"[^a-zA-Z0-9]", "", src)
        for movie in clear_movies:
            no_space_title = movie.replace(" ", "")
            if no_space_title.lower() in clear_url:
                print(clear_url)


# for img in img_movie:
#    src = img.get("src")
#    if src.startswith("https"):
#        print(src)

# for titre in movie_titles:
#    print(titre.get_text(strip=True))
