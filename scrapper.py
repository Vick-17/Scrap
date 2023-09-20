import pdfplumber
import pandas as pd

# Ouvrir le fichier PDF
with pdfplumber.open("liste_de_joueur.pdf") as pdf:
    data = []

    # Parcourir chaque page du PDF
    for page in pdf.pages:
        # Extraire le texte de la page
        text = page.extract_text()

        # Diviser le texte en lignes
        lines = text.split("\n")

        # Parcourir chaque ligne
        for line in lines:
            # Diviser la ligne en mots
            words = line.split()

            # Vérifier si la ligne contient suffisamment de mots pour extraire les informations du joueur
            if len(words) >= 8 and "ST GEORGES DES COTEAUX" not in line and "licences" not in line and "Généré" not in line and "Photo" not in line and "Club" not in line and "MUTATION" not in line:
                try:
                    nom = words[0]
                    prenom = words[1]
                    date_naissance = words[2]
                    nationalite = words[3]
                    licence = words[4]
                    categorie = words[5]
                    if len(words) > 12:
                        categorie += " " + words[7]
                    date_enregistrement = words[11]
                    etat = words[12]

                    # Ajouter les informations du joueur à la liste de données
                    data.append([nom, prenom, date_naissance, nationalite, licence, categorie, date_enregistrement, etat])
                except:
                    # Ignorer les lignes qui ne peuvent pas être traitées
                    pass

    # Créer un DataFrame avec les données extraites
    df = pd.DataFrame(data, columns=["nom", "prenom", "date_naissance", "nationalite", "licence", "categorie", "date_enregistrement", "etat"])

    # Afficher le DataFrame
    print(df)