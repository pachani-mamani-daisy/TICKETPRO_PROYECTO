from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.models import Boleto, User, Pelicula
from sqlalchemy import func
from app.extensions import db
from . import admin_bp

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role.nombre != 'Admin':
        abort(403)

    # MÉTRICAS BÁSICAS
    total_ventas = db.session.query(func.sum(Boleto.total)).scalar() or 0
    total_usuarios = User.query.count()
    total_peliculas = Pelicula.query.count()
    ultimas_ventas = Boleto.query.order_by(Boleto.fecha_compra.desc()).limit(5).all()

    # --- DETALLE IMPORTANTE: Traer todas las pelis para el CRUD ---
    todas_las_pelis = Pelicula.query.all()

    return render_template('admin/dashboard.html', 
                           ventas=total_ventas, 
                           users=total_usuarios, 
                           pelis=total_peliculas,
                           recientes=ultimas_ventas,
                           peliculas_all=todas_las_pelis) # Pasamos la lista aquí

@admin_bp.route('/movies/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_movie(id):
    if current_user.role.nombre != 'Admin':
        abort(403)
        
    peli = Pelicula.query.get_or_404(id)
    
    if request.method == 'POST':
        peli.titulo = request.form.get('titulo')
        peli.duracion = request.form.get('duracion')
        peli.sinopsis = request.form.get('sinopsis')
        db.session.commit()
        flash('Película actualizada correctamente', 'success')
        return redirect(url_for('admin.dashboard'))
        
    return render_template('admin/edit_movie.html', peli=peli)

@admin_bp.route('/movies/delete/<int:id>')
@login_required
def delete_movie(id):
    if current_user.role.nombre != 'Admin':
        abort(403)
        
    peli = Pelicula.query.get_or_404(id)
    db.session.delete(peli)
    db.session.commit()
    flash('Película eliminada del inventario', 'warning')
    return redirect(url_for('admin.dashboard'))