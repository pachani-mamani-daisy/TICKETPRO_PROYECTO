from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Role
from app.extensions import db
from . import auth_bp

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash('El usuario ya existe', 'danger')
            return redirect(url_for('auth.register'))

        role_name = 'Admin' if User.query.count() == 0 else 'Cliente'
        user_role = Role.query.filter_by(nombre=role_name).first()

        new_user = User(username=username, role=user_role)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        flash('Registro exitoso. Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f'Bienvenido {user.username}', 'success')

            if user.role.nombre == 'Admin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('movie.index'))
        
        flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
