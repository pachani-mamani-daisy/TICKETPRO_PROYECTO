from .extensions import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# 1. Tabla de Roles (Para Requisito de Roles)
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False) 
    usuarios = db.relationship('User', backref='role', lazy=True)

# 2. Tabla de Usuarios (Para Autenticación)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    boletos = db.relationship('Boleto', backref='cliente', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# 3. Tabla de Géneros de Película
class Genero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    peliculas = db.relationship('Pelicula', backref='genero', lazy=True)

# 4. Tabla de Películas
class Pelicula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    sinopsis = db.Column(db.Text)
    duracion = db.Column(db.Integer) 
    imagen_url = db.Column(db.String(500)) 
    genero_id = db.Column(db.Integer, db.ForeignKey('genero.id'), nullable=False)
    funciones = db.relationship('Funcion', backref='pelicula', lazy=True)

# 5. Tabla de Sucursales (Cines)
class Sucursal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200))
    salas = db.relationship('Sala', backref='sucursal', lazy=True)

# 6. Tabla de Salas
class Sala(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_sala = db.Column(db.Integer, nullable=False)
    capacidad = db.Column(db.Integer, nullable=False)
    sucursal_id = db.Column(db.Integer, db.ForeignKey('sucursal.id'), nullable=False)
    funciones = db.relationship('Funcion', backref='sala', lazy=True)

# 7. Tabla de Funciones (Horarios)
class Funcion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    horario = db.Column(db.DateTime, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    pelicula_id = db.Column(db.Integer, db.ForeignKey('pelicula.id'), nullable=False)
    sala_id = db.Column(db.Integer, db.ForeignKey('sala.id'), nullable=False)
    boletos = db.relationship('Boleto', backref='funcion', lazy=True)

# 8. Tabla de Boletos (Ventas)
class Boleto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_compra = db.Column(db.DateTime, default=datetime.utcnow)
    cantidad = db.Column(db.Integer, default=1)
    total = db.Column(db.Float, nullable=False)
    asiento = db.Column(db.String(10)) # Ejemplo: A-12
    calidad = db.Column(db.String(20)) # Ejemplo: 3D, IMAX
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    funcion_id = db.Column(db.Integer, db.ForeignKey('funcion.id'), nullable=False)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    