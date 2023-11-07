import sqlite3

DBNAME = "films.db"

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


def get_films_by(id_director):
    requete = """select film.titre, film.annee
                        from film
                        where film.idRealisateur=?
                        order by film.annee desc"""
    return _select(requete, params=(id_director,))

def get_all_films():
    requete = """select film.titre, film.annee, genre.nom
                        from film inner join genre on film.idGenre=genre.id"""
    return _select(requete)
