from run import flask_app
from app.extensions import db
from app.models import Pelicula, Funcion, Sala, Boleto
from datetime import datetime

def aplicar_ajustes():
    with flask_app.app_context():
        db.session.query(Boleto).delete()
        db.session.query(Funcion).delete()
        db.session.commit()

        datos_peliculas = {
            "Sangre de Cóndor": {"duracion": 70, "dias": [5, 12, 20], "horas": [14, 18]},
            "El Coraje del Pueblo": {"duracion": 90, "dias": [6, 13, 21], "horas": [16, 20]},
            "Utama": {"duracion": 87, "dias": [7, 14, 22], "horas": [15, 19, 22]},
            "Wiñaypacha": {"duracion": 86, "dias": [8, 15, 23], "horas": [13, 17, 21]},
            "El Atraco": {"duracion": 120, "dias": [9, 16, 24], "horas": [14, 19, 23]}
        }

        sala = Sala.query.first()

        for titulo, info in datos_peliculas.items():
            peli = Pelicula.query.filter_by(titulo=titulo).first()
            if peli:
                peli.duracion = info["duracion"]

                for dia in info["dias"]:
                    for hora in info["horas"]:
                        nueva_f = Funcion(
                            horario=datetime(2026, 7, dia, hora, 0),
                            precio=30.0 if hora < 18 else 45.0,
                            pelicula_id=peli.id,
                            sala_id=sala.id
                        )
                        db.session.add(nueva_f)
        
        db.session.commit()
        print("✅ Duraciones actualizadas y múltiples horarios creados para Julio.")

if __name__ == "__main__":
    aplicar_ajustes()