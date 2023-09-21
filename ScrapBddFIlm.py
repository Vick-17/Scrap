import requests
from bs4 import BeautifulSoup as bs
import re
import psycopg2


def clean_movie_titles(movie_titles):
    clear_movies = []
    for title in movie_titles:
        raw_title = title.get_text(strip=True)

        # Utilisation de regex pour extraire l'année entre parenthèses
        match = re.search(r"\((\d{4})\)", raw_title)
        year = match.group(1) if match else None

        # Suppression de l'année du titre
        clear_title = re.sub(r"\(\d{4}\)", "", raw_title).strip()

        clear_title = re.sub(r"[^a-zA-Z\séÉ]", "", clear_title)
        clear_title = clear_title.replace("é", "e")
        clear_title = clear_title.replace("É", "E")

        # Ajout du titre nettoyé et de l'année au dictionnaire
        clear_movies.append({"title": clear_title, "year": year})
    return clear_movies


# Fonction pour associer les images aux titres des films
def associate_images_with_titles(img_movie, clear_movies):
    movies = []
    for img in img_movie:
        src = img.get("src")
        if src.startswith("https"):
            clear_url = re.sub(r"[^a-zA-Z0-9]", "", src)
            for movie in clear_movies:
                # Déplacer cette ligne en dehors de la boucle interne
                no_space_title = movie["title"].replace(" ", "")
                if no_space_title.lower() in clear_url:
                    movies.append(
                        {"title": movie["title"], "year": movie["year"], "image_url": src})
    return movies


# Fonction pour associer les réalisateurs aux titres des films
def associate_directors_with_titles(movie_titles, director_elements):
    movies_with_directors = []
    for director_element in director_elements:
        director_name = director_element.get_text(strip=True)

        # Recherche du titre du film le plus proche en remontant l'arbre DOM
        title_element = director_element.find_parent().find(
            "a", class_="Text__SCText-sc-1aoldkr-0 Link__SecondaryLink-sc-1v081j9-1 kcGHBE jacWTu ProductListItem__StyledProductTitle-sc-1jkxxpj-3 dBFYVt")
        if title_element:
            movie_title = title_element.get_text(strip=True)
            movies_with_directors.append(
                {"title": movie_title, "director": director_name})

    return movies_with_directors


# Fonction principale (main)
def main():
    url = "https://www.senscritique.com/liste/100_films_a_voir_absolument/1568551?page=3"
    response = requests.get(url)
    html = response.content
    soup = bs(html, "lxml")

    # Récupérer tous les titres de film en passant la balise a et la classe de la balise
    movie_titles = soup.find_all(
        "a", class_="Text__SCText-sc-1aoldkr-0 Link__SecondaryLink-sc-1v081j9-1 kcGHBE jacWTu ProductListItem__StyledProductTitle-sc-1jkxxpj-3 dBFYVt")

    # Récupérer les URL des images des films
    img_movie = soup.find_all("img")

    # Nettoyage des titres et extraction de l'année
    clear_movies = clean_movie_titles(movie_titles)

    # Association des images aux titres
    movies = associate_images_with_titles(img_movie, clear_movies)

    try:
        conn = psycopg2.connect(
            user="postgres",
            password="iie254007",
            host="localhost",
            port="5432",
            database="tindMovieBdd"
        )
        cur = conn.cursor()

        for movie in movies:
            sql = """INSERT INTO public.film(titre, dates, image) VALUES(%s, %s, %s);"""
            values = (movie["title"], movie["year"], movie["image_url"])
            cur.execute(sql, values)
            conn.commit()

        conn.commit()
        count = cur.rowcount
        print(count, "enregistrement inséré avec succès dans la table film.")

        # fermeture de la connexion à la base de données
        cur.close()
        conn.close()
        print("La connexion PostgreSQL est fermée")

    except (Exception, psycopg2.Error) as error:
        print("Erreur lors de l'insertion dans la table film :", error)

if __name__ == "__main__":
    main()
