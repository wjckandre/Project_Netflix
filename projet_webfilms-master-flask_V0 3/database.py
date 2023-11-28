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


def get_films_by(id_director):
    requete = """select film.titre, film.annee
                        from film
                        where film.idRealisateur=?
                        order by film.annee desc"""
    return _select(requete, params=(id_director,))

def get_all_films():
    requete = """select film.titre, film.annee, genre.nom, film.Affiche , film.id from film 
                        inner join genre on film.idGenre=genre.id"""
    return _select(requete)

def get_all_genre():
    requete = """SELECT * FROM genre"""
    return _select(requete)

def get_all_reals():
    requete = """SELECT personne.id, personne.nom, personne.pays, personne.naissance, personne.sexe FROM personne 
                 INNER JOIN film ON personne.id = film.idRealisateur 
                 WHERE film.idRealisateur = personne.id"""
    return _select(requete)

def get_affiche():
    requete = """SELECT * FROM Affiche"""
    return _select(requete)

def get_trailer():
    requete = """SELECT * FROM Trailer"""
    return _select(requete)

def get_personne():
    requete = """SELECT * FROM personne"""
    return _select(requete)

def get_film(id_film):
    requete = """   select film.titre, film.annee, genre.nom , personne.nom , film.note , film.description, film.Affiche from film
                    inner join genre on film.idGenre=genre.id
                    inner join personne on personne.id=film.idRealisateur
                    WHERE film.id=?"""
    return _select(requete, params=(id_film,))

#def get_acteurs():
#   requete = """..."""
#   return _select(requete)

#def get_commentaire():
#   requete = """..."""
#   return _select(requete)