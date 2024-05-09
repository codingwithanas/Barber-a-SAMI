from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from psycopg2 import connect, IntegrityError, sql
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)
db_user = 'fl0user'
db_password = 'QX2Bg8JoaRvG'
db_host = 'ep-lively-lake-a1dxbq16.ap-southeast-1.aws.neon.fl0.io'
db_name = 'dbanasimario'
db_port = '5432'

db_url = f"postgres://fl0user:QX2Bg8JoaRvG@ep-lively-lake-a1dxbq16.ap-southeast-1.aws.neon.fl0.io:5432/dbanasimario?sslmode=require"

def connect_db():
    return connect(db_url)

# API key de OpenAI

@app.route('/')
def index():
    print(session)
    if 'users' in session:
        username = session['users']
        return render_template('index.html', username=username)
    return render_template('index.html')

@app.route('/estils')
def estils():
    if 'users' in session:
        username = session['users']
        return render_template('estils.html', username=username)

@app.route('/reservar')
def reservar():
    print(session)
    if 'users' in session:
        username = session['users']
        return render_template('reservar.html', username=username)
    return render_template('reservar.html')

@app.route('/servicios')
def servicios():
    print(session)
    if 'users' in session:
        username = session['users']
        return render_template('servicios.html', username=username)
    return render_template('servicios.html')
    
@app.route('/galeria')
def galeria():
        return render_template('galeria.html')

@app.route('/contact')
def contacto():
    print(session)
    if 'users' in session:
        username = session['users']
        return render_template('contacto.html', username=username)
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
        return render_template('resenas.html', username=username, valoraciones=valoraciones)
    
    return render_template('resenas.html', valoraciones=valoraciones)
    
@app.route('/mipanel')
def mipanel():
    if 'users' in session:
        username = session['users']
        return render_template('templates_paneles/panel_usuario.html', username=username)
    return redirect(url_for('templates_paneles/panel_usuario.html'))
@app.route('/getReservas', methods=['GET'])
def get_reservas():
    try:
        if 'user_id' not in session:
            return jsonify({'message': 'Usuario no autenticado'}), 401
        user_id = session['user_id']
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT dia, hora FROM reservas WHERE usuario_id=%s", (user_id,))
        reservas = cursor.fetchall()
        if reservas:
            return jsonify({'reservas': reservas})
        else:
            return jsonify({'message': 'No hay reservas'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/changePassword', methods=['POST'])
def change_password():
    data = request.get_json()
    current_password = data['currentPassword']
    new_password = data['newPassword']
    user_id = session['user_id']
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT password FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    if user and user[0] == current_password:
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
    cursor.execute("SELECT id, name FROM users WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    if user:
        session['users'] = user[1]
        session['user_id'] = user[0]
        print(session)
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'error': 'Invalid email or password'})

@app.route('/register', methods=['POST'])
def register():
    name = request.form['registerName']
    email = request.form['registerEmail']
    password = request.form['registerPassword']
    try:
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
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
    data = request.json
    opcion1 = data.get('opcion1')
    opcion2 = data.get('opcion2')

    pregunta = f"El usuario está buscando un nuevo corte de cabello y está eligiendo entre dos estilos específicos: {opcion1} y {opcion2}. Dadas estas opciones, ¿cuál crees que sería el mejor corte de cabello para alguien con cabello?"
    
    respuesta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": pregunta}
        ],
        temperature=0.5,
        max_tokens=100
    )

    return jsonify({'respuesta': respuesta['choices'][0]['message']['content'].strip()})

@app.route('/reservarcita', methods=['POST'])
def reservarcita():
    if 'user_id' not in session:
        return jsonify(success=False, message="No hay ninguna sesión iniciada")

    user_id = session['user_id']
    data = request.get_json()
    print(data)
    if 'day' not in data or 'hour' not in data:
        return jsonify(success=False, message="Faltan datos necesarios (día u hora)")

    day = data['day']
    hour = data['hour']

    conn = connect_db()
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO Reservas (dia, hora, usuario_id) VALUES (%s, %s, %s)", (day, hour, user_id))
        if cur.rowcount > 0:
            conn.commit()
            return jsonify(success=True)
        else:
            return jsonify(success=False, message="No se encontró el usuario")
    except Exception as e:
        print(e)
        return jsonify(success=False, message="No se pudo realizar la reserva")
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

if __name__ == '__main__':
    app.run(debug=True)
