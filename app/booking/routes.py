from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Funcion, Boleto, Pelicula
from app.extensions import db
from . import booking_bp 

@booking_bp.route('/buy/<int:peli_id>', methods=['GET', 'POST'])
@login_required
def buy_ticket(peli_id):
    pelicula = Pelicula.query.get_or_404(peli_id)
    funciones_db = Funcion.query.filter_by(pelicula_id=peli_id).order_by(Funcion.horario).all()

    dias_es = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    meses_es = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

    funciones_formateadas = []
    for f in funciones_db:
        dia_n = dias_es[f.horario.weekday()]
        mes_n = meses_es[f.horario.month - 1]
        texto = f"{dia_n} {f.horario.day} de {mes_n} — {f.horario.strftime('%H:%M')} ({f.sala.sucursal.nombre})"

        funciones_formateadas.append({
            'id': f.id,
            'precio': f.precio,
            'texto_espanol': texto
        })

    if request.method == 'POST':
        funcion_id = request.form.get('funcion_id')
        asientos_str = request.form.get('asiento_seleccionado')
        calidad = request.form.get('calidad')
        lista_asientos = [s.strip() for s in asientos_str.split(',')]
        cantidad = len(lista_asientos)
        func_obj = Funcion.query.get(funcion_id)
 
        precio_final = func_obj.precio 

        extra = 0
        if calidad == '3D Digital': extra = 10
        elif calidad == 'IMAX Extreme': extra = 25
        
        precio_final = (func_obj.precio + extra) * cantidad

        nuevo_boleto = Boleto(
            user_id=current_user.id, 
            funcion_id=func_obj.id, 
            cantidad=1, 
            total=precio_final, 
            asiento=asientos_str,
            calidad=calidad
        )
        db.session.add(nuevo_boleto)
        db.session.commit()
        
        return redirect(url_for('booking.show_ticket', boleto_id=nuevo_boleto.id))
        
    return render_template('booking/buy.html', pelicula=pelicula, funciones=funciones_formateadas)

@booking_bp.route('/ticket/<int:boleto_id>')
@login_required
def show_ticket(boleto_id):
    boleto = Boleto.query.get_or_404(boleto_id)
    return render_template('booking/ticket.html', boleto=boleto)