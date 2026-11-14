import csv
import io
import os
import secrets
import sqlite3
from datetime import date
from decimal import Decimal, InvalidOperation
from functools import wraps
from contextlib import contextmanager
from pathlib import Path

from flask import Flask, Response, flash, redirect, render_template, request, session, url_for


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(SECRET_KEY=os.environ.get('SECRET_KEY') or secrets.token_hex(32),
                      DATABASE=str(Path(app.instance_path) / 'gastos.db'),
                      SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax')
    if config:
        app.config.update(config)
    Path(app.config['DATABASE']).parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def connect():
        db = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()

    with connect() as db:
        db.execute('CREATE TABLE IF NOT EXISTS gastos (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT NOT NULL, descripcion TEXT NOT NULL, centimos INTEGER NOT NULL CHECK(centimos > 0))')

    @app.template_filter('soles')
    def soles(value):
        return f'S/ {value / 100:,.2f}'

    @app.context_processor
    def context():
        if 'csrf' not in session:
            session['csrf'] = secrets.token_hex(24)
        return {'csrf': session['csrf'], 'hoy': date.today().isoformat()}

    @app.before_request
    def csrf_protection():
        if request.method == 'POST' and not secrets.compare_digest(session.get('csrf', ''), request.form.get('csrf', '')):
            return 'Formulario vencido. Recarga la página y vuelve a intentarlo.', 400

    def login_required(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not session.get('usuario'):
                return redirect(url_for('login'))
            return view(*args, **kwargs)
        return wrapped

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            if request.form.get('usuario') == 'admin' and request.form.get('clave') == '123':
                session.clear()
                session['usuario'] = 'admin'
                flash('¡Bienvenida! Ya puedes registrar tus gastos.', 'success')
                return redirect(url_for('inicio'), code=303)
            flash('Usuario o contraseña incorrectos.', 'error')
        return render_template('login.html')

    @app.post('/salir')
    @login_required
    def salir():
        session.clear()
        return redirect(url_for('login'), code=303)

    @app.route('/', methods=['GET', 'POST'])
    @login_required
    def inicio():
        status = 200
        if request.method == 'POST':
            try:
                fecha = request.form.get('fecha', '')
                if date.fromisoformat(fecha).isoformat() != fecha:
                    raise ValueError()
                descripcion = request.form.get('descripcion', '').strip()
                if not 1 <= len(descripcion) <= 200:
                    raise ValueError()
                monto = Decimal(request.form.get('monto', '').replace(',', '.'))
                if not monto.is_finite() or monto <= 0 or monto > Decimal('9999999.99') or monto != monto.quantize(Decimal('0.01')):
                    raise ValueError()
                with connect() as db:
                    db.execute('INSERT INTO gastos(fecha, descripcion, centimos) VALUES (?, ?, ?)', (fecha, descripcion, int(monto * 100)))
                flash('Gasto registrado correctamente.', 'success')
                return redirect(url_for('inicio'), code=303)
            except (ValueError, InvalidOperation):
                flash('Revisa la fecha, la descripción (1 a 200 caracteres) y el monto positivo con máximo dos decimales.', 'error')
                status = 400
        with connect() as db:
            gastos = db.execute('SELECT * FROM gastos ORDER BY fecha DESC, id DESC').fetchall()
        return render_template('inicio.html', gastos=gastos, total=sum(g['centimos'] for g in gastos)), status

    @app.get('/reporte')
    @login_required
    def reporte():
        desde, hasta = request.args.get('desde', ''), request.args.get('hasta', '')
        try:
            for valor in (desde, hasta):
                if valor and date.fromisoformat(valor).isoformat() != valor:
                    raise ValueError()
            if desde and hasta and desde > hasta:
                raise ValueError()
        except ValueError:
            flash('El intervalo de fechas no es válido.', 'error')
            return redirect(url_for('reporte'))
        sql, params = 'SELECT * FROM gastos WHERE 1=1', []
        if desde:
            sql += ' AND fecha >= ?'
            params.append(desde)
        if hasta:
            sql += ' AND fecha <= ?'
            params.append(hasta)
        with connect() as db:
            gastos = db.execute(sql + ' ORDER BY fecha DESC, id DESC', params).fetchall()
        if request.args.get('formato') == 'csv':
            out = io.StringIO(newline='')
            writer = csv.writer(out)
            writer.writerow(['Fecha', 'Descripción', 'Monto (S/)'])
            for g in gastos:
                descripcion = g['descripcion']
                if descripcion.lstrip().startswith(('=', '+', '-', '@')):
                    descripcion = "'" + descripcion
                writer.writerow([g['fecha'], descripcion, f"{Decimal(g['centimos']) / 100:.2f}"])
            writer.writerow(['', 'TOTAL', f"{Decimal(sum(g['centimos'] for g in gastos)) / 100:.2f}"])
            return Response('\ufeff' + out.getvalue(), content_type='text/csv; charset=utf-8', headers={'Content-Disposition': 'attachment; filename=reporte_gastos.csv'})
        return render_template('reporte.html', gastos=gastos, total=sum(g['centimos'] for g in gastos), desde=desde, hasta=hasta)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
