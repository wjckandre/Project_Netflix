from flask import render_template, request, Flask
import database as db

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
    films = db.get_all_genre()
    return render_template("liste_genre.html", films=films)

@app.route('/admin_getReal')
def admin_real():
    reals = db.get_all_reals()
    return render_template("liste_all_real.html", reals=reals)

if __name__ == "__main__":
    app.run()
