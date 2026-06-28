from run import flask_app
from app.extensions import db
from app.models import Role, User, Genero, Pelicula, Sucursal, Sala, Funcion
from datetime import datetime, timedelta

def reparar_todo():
    with flask_app.app_context():
        db.create_all()

        admin_role = Role(nombre='Admin')
        cliente_role = Role(nombre='Cliente')
        db.session.add_all([admin_role, cliente_role])

        user = User(username='daisy_admin', role=admin_role)
        user.set_password('admin123')
        db.session.add(user)

        suc = Sucursal(nombre="Cine Central El Alto", direccion="Av. 6 de Marzo")
        db.session.add(suc)
        db.session.flush()
        sala = Sala(numero_sala=1, capacidad=50, sucursal_id=suc.id)
        db.session.add(sala)

        peli = Pelicula(titulo="Utama", sinopsis="Cine Boliviano", duracion=90, 
                        genero=Genero(nombre="Drama"))
        db.session.add(peli)
        db.session.flush()

        f = Funcion(horario=datetime(2026, 7, 10, 19, 0), precio=35.0, 
                    pelicula_id=peli.id, sala_id=sala.id)
        db.session.add(f)

        db.session.commit()
        print("✅ SISTEMA RECONSTRUIDO EXITOSAMENTE")

if __name__ == "__main__":
    reparar_todo()
    