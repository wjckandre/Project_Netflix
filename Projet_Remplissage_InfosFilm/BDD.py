import requests
import json
import sqlite3

DBNAME = "InfosFilms.db"

def _select(requete, params=None):
    """ Exécute une requête type select"""
    with sqlite3.connect(DBNAME) as db:
        c = db.cursor()
        if params is None:
            c.execute(requete)
        else:
            c.execute(requete, params)
        res = c.fetchall()
    return res
page = 1
url_movie = "https://api.themoviedb.org/3/trending/movie/day?language=en-US"
url_personne = "https://api.themoviedb.org/3/trending/person/day?language=en-US&page=1"
url_genre = "https://api.themoviedb.org/3/genre/movie/list?language=en"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1NmNlZDhiOWNmM2I5NGRkYjBjYzc2MzFkYzQ4YjE0NyIsInN1YiI6IjY1MmVhMDA5Y2FlZjJkMDBhZGE4MGQzOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.fVacvY556R8-Zg0eCBqUEBOSWaQso4RwpnVSuIEqNrU"
}

list_personne_id = []
list_film_id = []

def insert_genre(id, nom):
    requete = f""" INSERT INTO genre (id, nom)
                  VALUES ({id}, '{nom}') """
    return _select(requete)

def insert_real(id, name, popularity, profile_path, gender):
    requete = f""" INSERT INTO personne (id, nom, sexe, popularity, profile_path)
                   VALUES ({id}, '{name}', {gender}, {popularity}, '{profile_path}') """
    return _select(requete)

def insert_movie(id, titre, annee, idRealisateur, idGenre, note, description, trailer, affiche, popularity):
    requete = f""" INSERT INTO film (id, titre, annee, idRealisateur, idGenre, note, description, trailer, affiche, popularity)
                   VALUES ({id}, "{titre}", '{annee}', {idRealisateur}, {idGenre}, {note}, "{description.replace('"', "'")}", '{trailer}', '{affiche}' , {popularity}) """
    print(requete)
    return _select(requete)

response_movie = requests.get(url_movie, headers=headers)
response_personne = requests.get(url_personne, headers=headers)
response_genre = requests.get(url_genre, headers=headers)

print(response_movie.json())

# for x in range(100):  
    # response_personne = requests.get(url_personne, headers=headers)
    # page =+1
for i in response_personne.json()['results']:
    if i['known_for_department'] == 'Directing' and i['id'] not in list_personne_id:
        insert_real(i['id'], i['name'], i['popularity'], i['profile_path'], i['gender'])
        list_personne_id.append(i['id'])
        # print(i['known_for'])
    elif i['known_for_department'] == 'Directing':
        for a in i['known_for']:
            if a['id'] not in list_film_id:
                print(list_film_id)
                insert_movie(a['id'], a['title'], a['release_date'], i["id"], a['genre_ids'][0], a['vote_average'], a['overview'], 'blub', a['poster_path'], a['popularity'])
                list_film_id.append(a['id'])
                print(a['id'], a['title'], a['release_date'], i["id"], a['genre_ids'][0], a['vote_average'], a['overview'], 'blub', a['poster_path'], a['popularity'])

