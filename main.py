from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from psycopg2 import connect, IntegrityError, sql
import openai
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
    
@app.route('/galeria')
def galeria():
        return render_template('galeria.html')

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
        
if __name__ == '__main__':
    app.run(debug=True)
