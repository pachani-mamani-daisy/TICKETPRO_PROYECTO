from flask import render_template
from . import movie_bp  
from app.models import Pelicula, Funcion

@movie_bp.route('/')
def index():
    peliculas = Pelicula.query.all()
    return render_template('movie/index.html', peliculas=peliculas)

@movie_bp.route('/<int:id>')
def detail(id):
    pelicula = Pelicula.query.get_or_404(id)
    return render_template('movie/detail.html', pelicula=pelicula)
