import requests
import json
import sqlite3

DBNAME = "InfosFilmsAuto.db"

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
url_genre = "https://api.themoviedb.org/3/genre/movie/list?language=en"
url_genre_TV = "https://api.themoviedb.org/3/genre/tv/list?language=en"

def url_movie_search(titre):
    return f"https://api.themoviedb.org/3/search/movie?query={titre}&include_adult=true&language=en-US&page=1"

def url_personne(page):
    return  f"https://api.themoviedb.org/3/trending/person/day?language=en-US&page={page}"

def url_search_person(name):
    return f"https://api.themoviedb.org/3/search/person?query={name}&include_adult=false&language=en-US&page=1"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1NmNlZDhiOWNmM2I5NGRkYjBjYzc2MzFkYzQ4YjE0NyIsInN1YiI6IjY1MmVhMDA5Y2FlZjJkMDBhZGE4MGQzOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.fVacvY556R8-Zg0eCBqUEBOSWaQso4RwpnVSuIEqNrU"
}


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
    return _select(requete)

def search_id(table):
    requete = f""" SELECT id FROM {table} """
    return _select(requete)

list_personne_id = []
list_film_id = []
list_genre_id = []
inserted_movies = []

for x in search_id('personne'):
    list_personne_id.append(x[0])
for y in search_id('film'):
    list_film_id.append(y[0])
for z in search_id('genre'):
    list_genre_id.append(z[0])

response_movie = requests.get(url_movie, headers=headers)
response_genre = requests.get(url_genre, headers=headers)
response_genre_TV = requests.get(url_genre_TV, headers=headers)


def NotIn(lst, x):
    count = 0
    for ele in lst:
        if (ele == x):
            count = count + 1
    return count==0

def remplissage_film_personne():
    for x in range(1, 5):  
        response_personne = requests.get(url_personne(x), headers=headers)
        for i in response_personne.json()['results']:
            if i['known_for_department'] == 'Directing' and NotIn(list_personne_id, i['id']):
                insert_real(i['id'], i['name'], i['popularity'], i['profile_path'], i['gender'])
                list_personne_id.append(i['id'])
                print(i['id'], i['name'], i['popularity'], i['profile_path'], i['gender'])
            if i['known_for_department'] == 'Directing':
                for a in i['known_for']:
                    
                    if NotIn(list_film_id, a['id']):
                        try: titre=a['title'] 
                        except: titre=a['name']
                        try: date=a['release_date']
                        except: date=a['first_air_date']
                        insert_movie(a['id'], titre, date, i["id"], a['genre_ids'][0], a['vote_average'], a['overview'], 'blub', a['poster_path'], a['popularity'])
                        list_film_id.append(a['id'])
                        inserted_movies.append(titre)
                        print(a['id'], titre, date, i["id"], a['genre_ids'][0], a['vote_average'], a['overview'], 'blub', a['poster_path'], a['popularity'])

def remplissage_genre():
    for i in response_genre.json()['genres']:
        if NotIn(list_genre_id, i['id']):
            insert_genre(i['id'], i['name'])
            print(i['id'], i['name'])
            list_genre_id.append(i['id'])
    for i in response_genre_TV.json()['genres']:
        if NotIn(list_genre_id, i['id']):
            insert_genre(i['id'], i['name'])
            print(i['id'], i['name'])
            list_genre_id.append(i['id'])

def get_info_search_movie(title_movie, nom_real):
    response_search_movie =  requests.get(url_movie_search(title_movie), headers=headers).json()['results'][0]
    response_search_person = requests.get(url_search_person(nom_real), headers=headers).json()['results'][0]
    if NotIn(list_film_id, response_search_movie['id']):
        insert_movie(response_search_movie['id'], title_movie, response_search_movie['release_date'], response_search_person['id'], response_search_movie['genre_ids'][0], response_search_movie['vote_average'], response_search_movie['overview'] ,response_search_movie['video'], response_search_movie['poster_path'] ,response_search_movie['popularity'])
        print(response_search_movie)
        if NotIn(list_personne_id, response_search_person['id']):
            insert_real(response_search_person['id'], nom_real, response_search_person['popularity'], response_search_person['profile_path'], response_search_person['gender'])
            print(response_search_person)

