import datetime
from datetime import date
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from psycopg2 import connect, IntegrityError, sql
#import openai
#from config import API_KEY
import os
import hashlib
#openai.api_key = API_KEY

app = Flask(__name__)
app.secret_key = os.urandom(24)
db_user = 'fl0user'
db_password = 'QX2Bg8JoaRvG'
db_host = 'ep-lively-lake-a1dxbq16.ap-southeast-1.aws.neon.fl0.io'
db_name = 'dbanasimario'
db_port = '5432'
db_url = f"postgres://fl0user:QX2Bg8JoaRvG@ep-lively-lake-a1dxbq16.ap-southeast-1.aws.neon.fl0.io:5432/dbanasimario?sslmode=require"


chatbot_requests = {}

def connect_db():
    return connect(db_url)

@app.route('/')
def index():
    print(session)
    if 'users' in session:
        username = session['users']
        admin = session.get('admin', False)
        return render_template('index.html', username=username, admin=admin)
    return render_template('index.html')

@app.route('/estils')
def estils():
    if 'users' in session:
        username = session['users']
        admin = session.get('admin', False)
        return render_template('estils.html', username=username, admin=admin)
    return render_template('estils.html')

@app.route('/reservar')
def reservar():
    print(session)
    if 'users' in session:
        username = session['users']
        admin = session.get('admin', False)
        return render_template('reservar.html', username=username, admin=admin)
    return render_template('reservar.html')

@app.route('/servicios')
def servicios():
    print(session)
    if 'users' in session:
        username = session['users']
        admin = session.get('admin', False)
        return render_template('servicios.html', username=username, admin=admin)
    return render_template('servicios.html')
    
@app.route('/galeria')
def galeria():
    if 'users' in session:
        username = session['users']
        admin = session.get('admin', False)
        return render_template('galeria.html', username=username, admin=admin)
    return render_template('galeria.html')

@app.route('/contact')
def contacto():
    print(session)
    if 'users' in session:
        username = session['users']
        admin = session.get('admin', False)
        return render_template('contacto.html', username=username, admin=admin)
    return render_template('contacto.html')
    
@app.route('/resenas', methods=['GET'])
def resenas():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM valoraciones")
    valoraciones = cur.fetchall()
    cur.close()
    conn.close()

    if 'users' in session:
        username = session['users']
        admin = session.get('admin', False)
        return render_template('resenas.html', username=username, admin=admin, valoraciones=valoraciones)
    return render_template('resenas.html', valoraciones=valoraciones, admin=admin)
    
@app.route('/mipanel')
def mipanel():
    if 'users' in session:
        username = session['users']
        admin = session.get('admin', False)
        return render_template('templates_paneles/panel_usuario.html', username=username, admin=admin)
    return redirect(url_for('templates_paneles/panel_usuario.html'))

@app.route('/getReservas', methods=['GET'])
def get_reservas():
    try:
        if 'user_id' not in session:
            return jsonify({'message': 'Usuario no autenticado'}), 401
        user_id = session['user_id']
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT id, dia, hora, datetime, servicio FROM reservas WHERE usuario_id=%s", (user_id,))
        reservas = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify({'reservas': reservas})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


        
@app.route('/changePassword', methods=['POST'])
def change_password():
    data = request.get_json()
    current_password = data['currentPassword']
    new_password = data['newPassword']
    new_password = hashlib.md5(new_password.encode()).hexdigest()
    user_id = session['user_id']
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT password FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    hashed_current_password = hashlib.md5(current_password.encode()).hexdigest()
    if user and user[0] == hashed_current_password:
            cursor.execute("UPDATE users SET password=%s WHERE id=%s", (new_password, user_id))
            connection.commit()
            return jsonify({'message': 'Password updated successfully'})
    else:
            return jsonify({'message': 'Current password is incorrect'}), 400
    
@app.route('/getCurrentEmail', methods=['GET'])
def get_current_email():
    user_id = session['user_id']
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT email FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    if user:
        return jsonify({'currentEmail': user[0]})
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/changeEmail', methods=['POST'])
def change_email():
    data = request.get_json()
    new_email = data['newEmail']
    user_id = session['user_id']
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET email=%s WHERE id=%s", (new_email, user_id))
    connection.commit()
    return jsonify({'message': 'Email updated successfully'})

@app.route('/login', methods=['POST'])
def login():
    email = request.form['loginEmail']
    password = request.form['loginPassword']
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, password, admin FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    if user and hashlib.md5(password.encode()).hexdigest() == user[2]:
        session['users'] = user[1]
        session['user_id'] = user[0]
        session['admin'] = user[3]  
        print("Sesión después del login:", session) 
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'error': 'Invalid email or password'})




@app.route('/register', methods=['POST'])
def register():
    name = request.form['registerName']
    email = request.form['registerEmail']
    password = request.form['registerPassword']
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    try:
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Registration successful'})
    except IntegrityError:
        return jsonify({'error': 'Email already exists'})


@app.route('/logout')
def logout():
    session.pop('users', None)
    return redirect(url_for('index'))

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_id = session.get('user_id')
    user_requests = chatbot_requests.get(user_id, {})
    today = date.today().isoformat()
    if user_requests.get(today, 0) >= 3:
        return jsonify({'error': 'Has alcanzado el límite de solicitudes de chatbot para hoy'}), 429

    data = request.json
    opcion1 = data.get('opcion1')
    opcion2 = data.get('opcion2')
    pregunta = f"El usuario tiene una cabeza {opcion1} y cabello {opcion2}. Dado su tipo de cabeza y cabello, ¿cuál sería el corte de cabello más adecuado para él? Por favor, responde con un solo tipo de corte de cabello, por ejemplo: 'Buzz Cut'."    
    respuesta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": pregunta}
        ],
        temperature=0.5,
        max_tokens=100
    )
    user_requests[today] = user_requests.get(today, 0) + 1
    chatbot_requests[user_id] = user_requests
    return jsonify({'respuesta': respuesta['choices'][0]['message']['content'].strip()})

@app.route('/reservarcita', methods=['POST'])
def reservarcita():
    if 'user_id' not in session:
        return jsonify(success=False, message="No hay ninguna sesión iniciada")

    user_id = session['user_id']
    data = request.get_json()
    if 'datetime' not in data or 'servicio' not in data:
        return jsonify(success=False, message="Faltan datos necesarios (fecha, hora o servicio)")

    datetime_str = data['datetime']
    servicio = data['servicio']
    datetime_obj = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

    days_in_spanish = {
        'Monday': 'Lunes',
        'Tuesday': 'Martes',
        'Wednesday': 'Miércoles',
        'Thursday': 'Jueves',
        'Friday': 'Viernes',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }

    day_of_week = days_in_spanish[datetime_obj.strftime("%A")]
    hour_of_day = datetime_obj.strftime("%H:%M")

    conn = connect_db()
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO reservas (dia, hora, datetime, usuario_id, servicio) VALUES (%s, %s, %s, %s, %s)",
                    (day_of_week, hour_of_day, datetime_str, user_id, servicio))
        if cur.rowcount > 0:
            conn.commit()
            return jsonify(success=True)
        else:
            return jsonify(success=False, message="No se pudo realizar la reserva")
    except Exception as e:
        return jsonify(success=False, message=str(e))
    finally:
        cur.close()
        conn.close()

@app.route('/contacto', methods=['GET', 'POST'])
def contacto_form():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        asunto = request.form.get('asunto')
        mensaje = request.form.get('mensaje')

        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO correocontacto (nombre, email, telefono, asunto, mensaje) 
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, email, telefono, asunto, mensaje))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify(success=True, message="Mensaje enviado")
    else:
        return render_template('contacto.html')
    
@app.route('/valoraciones', methods=['GET', 'POST'])
def valoraciones_form():
    if request.method == 'POST':
        nombre = request.form.get('name')
        email = session.get('email')
        valoracion = request.form.get('rating')
        comentario = request.form.get('review')
        print(valoracion)

        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO valoraciones (nombre, email, valoracion, comentario) 
            VALUES (%s, %s, %s, %s)
        """, (nombre, email, valoracion, comentario))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify(success=True, message="Valoración enviada")
    else:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM valoraciones")
        valoraciones = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('valoraciones.html', valoraciones=valoraciones)
    
@app.route('/panel_administrador', methods=['GET'])
def panel_administrador():
    print("Contenido de la sesión en /panel_administrador:", session)
    if 'admin' in session and session['admin']:
        username = session['users']
        
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("SELECT id, name, email FROM users")
        users = cursor.fetchall()

        cursor.execute("SELECT id, usuario_id, datetime, servicio FROM reservas")
        reservas = cursor.fetchall()

        cursor.execute("SELECT nombre, email, telefono, asunto, mensaje FROM correocontacto")
        correos = cursor.fetchall()

        cursor.execute("SELECT nombre, email, valoracion, comentario FROM valoraciones")
        valoraciones = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template('templates_paneles/panel_administrador.html', username=username, admin=True, users=users, reservas=reservas, correos=correos, valoraciones=valoraciones)
    else:
        return "No tienes permiso para acceder a esta página."

@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('panel_administrador'))

@app.route('/delete_reserva/<int:id>', methods=['POST'])
def delete_reserva(id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM reservas WHERE id = %s", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('panel_administrador'))

@app.route('/delete_valoracion/<nombre>/<email>/<valoracion>', methods=['POST'])
def delete_valoracion(nombre, email, valoracion):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM valoraciones WHERE nombre = %s AND email = %s AND valoracion = %s", (nombre, email, valoracion))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('panel_administrador'))

@app.route('/delete_contacto/<nombre>/<email>/<telefono>', methods=['POST'])
def delete_contacto(nombre, email, telefono):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM correocontacto WHERE nombre = %s AND email = %s AND telefono = %s", (nombre, email, telefono))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('panel_administrador'))

@app.route('/cancelar_reserva/<int:id>', methods=['DELETE'])
def cancelar_reserva(id):
    try:
        if 'user_id' not in session:
            return jsonify({'message': 'Usuario no autenticado'}), 401
        user_id = session['user_id']
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM reservas WHERE id=%s AND usuario_id=%s", (id, user_id))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Reserva eliminada con éxito'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/getAllReservas', methods=['GET'])
def get_all_reservas():
    try:
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT datetime FROM reservas")
        reservas = cursor.fetchall()
        reservas_dict = {reserva[0].strftime("%Y-%m-%d %H:%M"): True for reserva in reservas}
        return jsonify(reservas_dict)
    except Exception as e:
        print(f"Error al obtener reservas: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
        
if __name__ == '__main__':
    app.run(debug=True)
