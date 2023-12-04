from flask import render_template, request, Flask
import database as db
from BDD import *

app = Flask(__name__)

@app.route('/')
def index():
    films = db.get_all_films()
    return render_template("liste_all_films.html", films=films)


#essayez d'appeler cette route avec par exemple l'URL : http://127.0.0.1:5000/films_de/13848
#13848 est l'id de Charles Chaplin
@app.route('/films_de/<int:id_real>')
def films_de(id_real):
    print(id_real)
    films = db.get_films_by(id_real)
    print(films)
    return render_template("liste_films.html", films=films)

@app.route('/admin_getGenre')
def admin_genre():
    genres = db.get_all_genre()
    return render_template("liste_genre.html", genres=genres)

@app.route('/admin_getReal')
def admin_real():
    reals = db.get_all_reals()
    return render_template("liste_all_real.html", reals=reals)

@app.route('/admin_getPersonne')
def admin_personne():
    personnes = db.get_personne()
    return render_template("liste_personne.html", personnes=personnes)

@app.route('/admin_getAffiche')
def admin_affiche():
    affiches = db.get_affiche()
    return render_template("liste_affiche.html", affiches=affiches)

@app.route('/film/<int:id_film>')
def film(id_film):
    print(id_film)
    film = db.get_film(id_film)
    print(film)
    return render_template("film.html", film=film)

@app.route('/database/refresh')
def refreshDB():
    return render_template('New_films.html')

@app.route('/DB')
def DB():
    remplissage_film_personne()
    films = db.get_all_films()
    print("La fonction Python a été appelée !")
    return inserted_movies
# render_template("liste_all_films.html", films=films)

if __name__ == "__main__":
    app.run(debug=True)
