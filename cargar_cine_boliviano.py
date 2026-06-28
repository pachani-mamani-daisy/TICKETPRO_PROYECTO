from run import flask_app
from app.extensions import db
from app.models import Role, User, Genero, Pelicula, Sucursal, Sala, Funcion, Boleto
from datetime import datetime

def cargar_todo_con_imagenes():
    with flask_app.app_context():
        db.session.query(Boleto).delete()
        db.session.query(Funcion).delete()
        db.session.query(Pelicula).delete()
        db.session.query(Genero).delete()
        db.session.query(User).delete()
        db.session.query(Role).delete()
        db.session.commit()

        admin_role = Role(nombre='Admin')
        db.session.add_all([admin_role, Role(nombre='Cliente')])
        user = User(username='daisy_admin', role=admin_role)
        user.set_password('admin123')
        db.session.add(user)

        suc = Sucursal(nombre="Cine Central El Alto", direccion="Av. 6 de Marzo")
        db.session.add(suc)
        db.session.flush()
        sala = Sala(numero_sala=1, capacidad=50, sucursal_id=suc.id)
        db.session.add(sala)

        g_drama = Genero(nombre='Drama')
        g_hist = Genero(nombre='Histórico')
        g_susp = Genero(nombre='Suspenso')
        db.session.add_all([g_drama, g_hist, g_susp])
        db.session.commit()

        peliculas = [
                    {"t": "Sangre de Cóndor", "g": g_hist, "s": "Resistencia de una comunidad indígena.", "img": "sangre.png"},
                    {"t": "El Coraje del Pueblo", "g": g_hist, "s": "Relato histórico sobre la masacre de San Juan.", "img": "coraje.png"},
                    {"t": "Utama", "g": g_drama, "s": "Pareja de ancianos en la sequía del altiplano.", "img": "utama.png"},
                    {"t": "Wiñaypacha", "g": g_drama, "s": "Ancianos abandonados en los Andes.", "img": "winay.png"},
                    {"t": "El Atraco", "g": g_susp, "s": "Famoso asalto a una remesa minera.", "img": "atraco.png"}
                ]

        for i, p_info in enumerate(peliculas):
            p = Pelicula(
                titulo=p_info["t"], 
                sinopsis=p_info["s"], 
                duracion=90, 
                genero=p_info["g"],
                imagen_url=p_info["img"]
            )
            db.session.add(p)
            db.session.flush()

            f = Funcion(
                horario=datetime(2026, 7, (i*2)+1, 19, 30), 
                precio=35.0, 
                pelicula_id=p.id, 
                sala_id=sala.id
            )
            db.session.add(f)

        db.session.commit()
        print("✅ SISTEMA RECONSTRUIDO: 5 Pelis con imágenes y horarios de Julio.")

if __name__ == "__main__":
    cargar_todo_con_imagenes()