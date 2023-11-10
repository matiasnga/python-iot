import json

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'tu_llave_secreta'


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# def init_db():
#     with app.app_context():
#         db = get_db_connection()
#         db.execute(
#             "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL)")
#         db.commit()
#         db.execute(
#             """
#               CREATE TABLE IF NOT EXISTS devices (
#                   id INTEGER PRIMARY KEY AUTOINCREMENT,
#                   user_id INTEGER NOT NULL,
#                   device_serial_number TEXT UNIQUE NOT NULL,
#                   description TEXT  NOT NULL,
#                   type INTEGER NOT NULL,
#                   FOREIGN KEY(user_id) REFERENCES users(id)
#               )
#               """)
#         db.commit()
#         db.close()


@app.route('/')
def index():
    if 'user_id' in session:
        conn = get_db_connection()
        user = conn.execute('SELECT username FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        rows = conn.execute('SELECT u.id, u.username, d.device_serial_number, d.description, d.type from devices d inner join users u on u.id = d.user_id where user_id = ?', (session['user_id'],)).fetchall()
        conn.close()
        device_list = [
            {'id': row[0], 'username': row[1], 'device_serial_number': row[2], 'description': row[3], 'type': row[4]} for
            row in rows]
        return render_template('index.html', devices=device_list, username=user['username'])
    else:
        # En caso de que no haya una sesión activa
        return render_template('index.html', devices=[], username='')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_confirm = request.form['password-repeat']
        if password != password_confirm:
            flash('Las contraseñas no coinciden')
            return redirect(url_for('signup'))

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user:
            flash('El nombre de usuario ya existe.')
            return redirect(url_for('signup'))

        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                     (username, generate_password_hash(password)))
        conn.commit()
        conn.close()
        flash('Usuario registrado con éxito.')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        else:
            flash('Nombre de usuario o contraseña incorrectos')

    return render_template('login.html')


@app.route('/logout')
def logout():
    # Eliminar los datos de usuario de la sesión
    session.pop('user_id', None)
    # Puedes redirigir al usuario a la página de inicio o de login después
    return redirect(url_for('login'))


@app.route('/add_device', methods=['GET', 'POST'])
def add_device():
    if request.method == 'POST':
        device_serial_number = request.form['device-serial-number']
        description = request.form['device-description']
        print(device_serial_number, description)
        conn = get_db_connection()
        conn.execute('INSERT INTO devices ( user_id, device_serial_number, description, type) VALUES (?, ?, ?, ?)',
                     (session['user_id'], device_serial_number, description, 1))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_device.html')


if __name__ == '__main__':
    # init_db()
    app.run(debug=True, host='0.0.0.0', port=8080)
