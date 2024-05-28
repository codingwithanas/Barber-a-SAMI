import datetime
from datetime import date, timedelta
from flask import Flask, flash, request, jsonify, render_template, session, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from psycopg2 import connect, IntegrityError, sql
from werkzeug.utils import secure_filename
import openai
from config import OPENAI_API_KEY, Config
import os
import hashlib
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.from_object(Config)

openai.api_key = OPENAI_API_KEY
mail = Mail(app)
serializer = URLSafeTimedSerializer(app.secret_key)

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db_user = 'fl0user'
db_password = 'QX2Bg8JoaRvG'
db_host = 'ep-lively-lake-a1dxbq16.ap-southeast-1.aws.neon.fl0.io'
db_name = 'dbanasimario'
db_port = '5432'
db_url = f"postgres://fl0user:QX2Bg8JoaRvG@ep-lively-lake-a1dxbq16.ap-southeast-1.aws.neon.fl0.io:5432/dbanasimario?sslmode=require"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

chatbot_requests = {}

def connect_db():
    return connect(db_url)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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
    return render_template('estils.html', username=username)

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    email = request.form.get('forgotPasswordEmail')
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        token = serializer.dumps(email, salt='password-reset-salt')
        reset_url = url_for('reset_password', token=token, _external=True)
        msg = Message('Restablecimiento de Contraseña', sender=app.config['MAIL_USERNAME'], recipients=[email])
        msg.body = f'Para restablecer tu contraseña, haz clic en el siguiente enlace: {reset_url}'
        mail.send(msg)
        return jsonify({'message': 'Correo de restablecimiento de contraseña enviado'})
    else:
        return jsonify({'error': 'Correo no encontrado'}), 404

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        return jsonify({'error': 'El enlace de restablecimiento de contraseña es inválido o ha expirado.'}), 400

    if request.method == 'POST':
        new_password = request.form.get('newPassword')
        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
        
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("UPDATE users SET password = %s WHERE email = %s", (hashed_password, email))
        conn.commit()
        cur.close()
        conn.close()

        return render_template('index.html')

    return render_template('reset_password.html', token=token)

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
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SET TIME ZONE 'Europe/Madrid';")

    filter_type = request.args.get('filter', 'recent')

    if filter_type == 'recent':
        cur.execute("SELECT id, imagen, descripcion, fecha, autor FROM galeria ORDER BY fecha DESC")
    elif filter_type == 'oldest':
        cur.execute("SELECT id, imagen, descripcion, fecha, autor FROM galeria ORDER BY fecha ASC")
    else:
        cur.execute("SELECT id, imagen, descripcion, fecha, autor FROM galeria")

    imagenes = cur.fetchall()
    cur.close()
    conn.close()

    madrid_tz = datetime.timezone(datetime.timedelta(hours=2))  # Madrid timezone (UTC+2)
    imagenes = [(id, imagen, descripcion, fecha.replace(tzinfo=madrid_tz), autor) for id, imagen, descripcion, fecha, autor in imagenes]

    if 'users' in session:
        username = session['users']
        admin = session.get('admin', False)
        return render_template('galeria.html', username=username, admin=admin, imagenes=imagenes, filter_type=filter_type, datetime=datetime)
    return render_template('galeria.html', imagenes=imagenes, filter_type=filter_type, datetime=datetime)

@app.route('/edit_description/<int:image_id>', methods=['POST'])
def edit_description(image_id):
    new_description = request.form.get('newDescription')
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE galeria SET descripcion = %s WHERE id = %s", (new_description, image_id))
        conn.commit()
        flash('Descripción actualizada con éxito.', 'success')
    except Exception as e:
        flash(f'Error al actualizar la descripción: {str(e)}', 'danger')
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('panel_administrador'))

@app.route('/contact')
def contacto():
    print(session)
    if 'users' in session:
        username = session['users']
        admin = session.get('admin', False)
        return render_template('contacto.html', username=username, admin=admin)
    return render_template('contacto.html')
    
def load_prohibited_words():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT word FROM prohibited_words")
    words = cur.fetchall()
    cur.close()
    conn.close()
    return [word[0] for word in words]

prohibited_words = load_prohibited_words()


def contains_prohibited_words(comment):
    prohibited_words = load_prohibited_words()
    comment_lower = comment.lower()
    for word in prohibited_words:
        if word in comment_lower:
            return True
    return False

@app.route('/resenas', methods=['GET', 'POST'])
def resenas():
    if request.method == 'POST':
        nombre = request.form.get('name')
        valoracion = request.form.get('rating')
        comentario = request.form.get('review')
        servicio = request.form.get('service')

        if len(nombre) > 30:
            flash('El nombre no puede exceder los 30 caracteres.', 'danger')
            return redirect(url_for('resenas'))

        if len(comentario) > 100:
            flash('El comentario no puede exceder los 100 caracteres.', 'danger')
            return redirect(url_for('resenas'))

        if contains_prohibited_words(nombre) or contains_prohibited_words(comentario):
            flash('Tu comentario o nombre contiene palabras inapropiadas y no puede ser publicado.', 'danger')
            return redirect(url_for('resenas'))

        try:
            valoracion = int(valoracion)
            if valoracion < 1:
                valoracion = 1
        except ValueError:
            flash('Valor de valoración inválido', 'danger')
            return redirect(url_for('resenas'))

        timestamp = datetime.datetime.now()

        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO valoraciones (nombre, valoracion, comentario, servicio, timestamp) 
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, valoracion, comentario, servicio, timestamp))
        conn.commit()
        cur.close()
        conn.close()

        msg = Message('Nueva Reseña', sender=app.config['MAIL_USERNAME'], recipients=['barberiasami7@gmail.com'])
        msg.body = f'Un nuevo usuario ha realizado una reseña:\n\nNombre: {nombre}\nValoración: {valoracion}\nComentario: {comentario}\nServicio: {servicio}\nFecha: {timestamp}'
        mail.send(msg)

        flash('Tu reseña ha sido publicada y se ha enviado una notificación.', 'success')
        return redirect(url_for('resenas'))

    filter_type = request.args.get('filter', 'recent')

    conn = connect_db()
    cur = conn.cursor()
    
    if filter_type == 'high_rating':
        cur.execute("SELECT nombre, valoracion, comentario, servicio, timestamp FROM valoraciones ORDER BY valoracion DESC")
    elif filter_type == 'low_rating':
        cur.execute("SELECT nombre, valoracion, comentario, servicio, timestamp FROM valoraciones ORDER BY valoracion ASC")
    elif filter_type == 'recent':
        cur.execute("SELECT nombre, valoracion, comentario, servicio, timestamp FROM valoraciones ORDER BY timestamp DESC")
    elif filter_type == 'oldest':
        cur.execute("SELECT nombre, valoracion, comentario, servicio, timestamp FROM valoraciones ORDER BY timestamp ASC")
    else:
        cur.execute("SELECT nombre, valoracion, comentario, servicio, timestamp FROM valoraciones")
    
    valoraciones = cur.fetchall()
    cur.close()
    conn.close()

    if 'users' in session:
        username = session['users']
        admin = session.get('admin', False)
        return render_template('resenas.html', username=username, admin=admin, valoraciones=valoraciones, datetime=datetime, filter_type=filter_type)
    
    return render_template('resenas.html', valoraciones=valoraciones, datetime=datetime, filter_type=filter_type)

@app.route('/panel_administrador', methods=['GET', 'POST'])
def panel_administrador():
    if 'admin' not in session or not session['admin']:
        return redirect(url_for('index'))

    conn = connect_db()
    cur = conn.cursor()

    if request.method == 'POST':
        if 'new_prohibited_word' in request.form:
            new_word = request.form.get('new_prohibited_word').lower()
            try:
                cur.execute("INSERT INTO prohibited_words (word) VALUES (%s)", (new_word,))
                conn.commit()
                flash(f'Palabra prohibida "{new_word}" añadida con éxito.', 'success')
            except IntegrityError:
                flash(f'La palabra "{new_word}" ya existe.', 'danger')
        
        elif 'image' in request.files:
            file = request.files['image']
            description = request.form.get('description')
            autor = session['users'] 

            if file.filename == '':
                flash('No se seleccionó ninguna imagen', 'danger')
                return redirect(url_for('panel_administrador'))

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                cur.execute("INSERT INTO galeria (imagen, descripcion, autor) VALUES (%s, %s, %s)", (filename, description, autor))
                conn.commit()
                flash('Imagen subida exitosamente', 'success')
            else:
                flash('Solo se permiten archivos con extensiones .jpeg/.jpg/.png/.gif', 'danger')

    cur.execute("SELECT id, name, email, admin, last_name, phone, sex FROM users")
    users = cur.fetchall()
    cur.execute("SELECT id, word FROM prohibited_words")
    prohibited_words_list = cur.fetchall()
    cur.execute("SELECT id, usuario_id, datetime, servicio FROM reservas")
    reservas = cur.fetchall()
    cur.execute("SELECT nombre, email, telefono, asunto, mensaje FROM correocontacto")
    correos = cur.fetchall()
    cur.execute("SELECT nombre, valoracion, comentario FROM valoraciones")
    valoraciones = cur.fetchall()
    cur.execute("SELECT id, imagen, descripcion FROM galeria")
    imagenes = cur.fetchall()

    cur.close()
    conn.close()

    if 'users' in session:
        username = session['users']
        admin = session.get('admin', False)
        return render_template('templates_paneles/panel_administrador.html', 
                               username=username, 
                               admin=admin,
                               prohibited_words=prohibited_words_list,
                               users=users,
                               reservas=reservas,
                               correos=correos,
                               valoraciones=valoraciones,
                               imagenes=imagenes)
    return redirect(url_for('index'))

@app.route('/edit_user/<int:id>', methods=['POST'])
def edit_user(id):
    if 'admin' not in session or not session['admin']:
        return redirect(url_for('index'))
    
    name = request.form['editUserName']
    last_name = request.form['editUserLastName']
    email = request.form['editUserEmail']
    phone = request.form['editUserPhone']
    sex = request.form['editUserSex']
    
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            UPDATE users 
            SET name = %s, last_name = %s, email = %s, phone = %s, sex = %s 
            WHERE id = %s
        """, (name, last_name, email, phone, sex, id))
        conn.commit()
        cur.close()
        conn.close()
        flash('Usuario actualizado con éxito', 'success')
    except Exception as e:
        flash(f'Error al actualizar el usuario: {str(e)}', 'danger')
    
    return redirect(url_for('panel_administrador'))

@app.route('/delete_image/<int:id>', methods=['POST'])
def delete_image(id):
    if 'admin' not in session or not session['admin']:
        return redirect(url_for('index'))

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT imagen FROM galeria WHERE id = %s", (id,))
    imagen = cur.fetchone()
    
    if imagen:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], imagen[0]))
        cur.execute("DELETE FROM galeria WHERE id = %s", (id,))
        conn.commit()
        flash('Imagen eliminada exitosamente', 'success')
    else:
        flash('Imagen no encontrada', 'danger')

    cur.close()
    conn.close()
    return redirect(url_for('panel_administrador'))

@app.route('/delete_prohibited_word/<int:id>', methods=['POST'])
def delete_prohibited_word(id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM prohibited_words WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    flash('Palabra prohibida eliminada con éxito.', 'success')
    return redirect(url_for('panel_administrador'))
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
    new_password = hashlib.sha256(new_password.encode()).hexdigest()
    user_id = session['user_id']
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT password, email, name FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    hashed_current_password = hashlib.sha256(current_password.encode()).hexdigest()

    if user and user[0] == hashed_current_password:
        cursor.execute("UPDATE users SET password=%s WHERE id=%s", (new_password, user_id))
        connection.commit()

        email = user[1]
        name = user[2]
        msg_to_user = Message('Cambio de Contraseña', sender=app.config['MAIL_USERNAME'], recipients=[email])
        msg_to_user.body = (f'Hola {name},\n\nTu contraseña ha sido cambiada exitosamente. '
                            'Si no has sido tú quien realizó este cambio, por favor restablece tu contraseña utilizando el siguiente enlace: '
                            f'{url_for("index", _external=True)}#forgotPassword\n\nGracias,\nEquipo de Barbería SAMI')
        mail.send(msg_to_user)

        return jsonify({'message': 'Contraseña actualizada correctamente'})
    else:
        return jsonify({'message': 'La contraseña actual es incorrecta'}), 400
    
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
    return jsonify({'message': 'Email actualizado correctamente'})

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
    if user and hashlib.sha256(password.encode()).hexdigest() == user[2]:
        session['users'] = user[1]
        session['user_id'] = user[0]
        session['admin'] = user[3]  
        print("Sesión después del login:", session) 
        return jsonify({'message': 'Inicio de sesión exitoso'})
    else:
        return jsonify({'error': 'Email o contraseña incorrectos'})

@app.route('/register', methods=['POST'])
def register():
    name = request.form['registerName']
    last_name = request.form['registerLastName']
    phone = request.form['registerPhone']
    email = request.form['registerEmail']
    password = request.form['registerPassword']
    sex = request.form['registerSex']
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (name, last_name, phone, email, password, sex) VALUES (%s, %s, %s, %s, %s, %s)",
                        (name, last_name, phone, email, hashed_password, sex))
        connection.commit()
        cursor.close()
        connection.close()

        admin_email = 'barberiasami7@gmail.com'
        msg_to_admin = Message('Nuevo Registro de Usuario', sender=app.config['MAIL_USERNAME'], recipients=[admin_email])
        msg_to_admin.body = f'Se ha registrado un nuevo usuario:\n\nNombre: {name} {last_name}\nEmail: {email}\nTeléfono: {phone}\nSexo: {sex}'
        mail.send(msg_to_admin)

        msg_to_user = Message('Bienvenido a Barbería SAMI', sender=app.config['MAIL_USERNAME'], recipients=[email])
        msg_to_user.body = f'Hola {name},\n\nGracias por registrarte en Barbería SAMI. ¡Esperamos verte pronto!'
        mail.send(msg_to_user)

        return jsonify({'message': 'Registro exitoso'})
    except IntegrityError:
        return jsonify({'error': 'Este email ya está registrado'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logout')
def logout():
    session.pop('users', None)
    session.clear()
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

from datetime import timedelta

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
    datetime_str = datetime_obj.strftime("%Y-%m-%d %H:%M")

    conn = connect_db()
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO reservas (dia, hora, datetime, usuario_id, servicio) VALUES (%s, %s, %s, %s, %s)",
                    (day_of_week, hour_of_day, datetime_str, user_id, servicio))
        if cur.rowcount > 0:
            conn.commit()

            username = session['users']
            msg = Message('Nueva Reserva', sender=app.config['MAIL_USERNAME'], recipients=['barberiasami7@gmail.com'])
            msg.body = f'{username} ha reservado el día {day_of_week}, {datetime_str} con servicio de {servicio}. Si está ocupado, ingrese a la web y cancele la reserva.'
            mail.send(msg)

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

        if not telefono.isdigit() or len(telefono) != 9:
            flash('El número de teléfono debe tener exactamente 9 dígitos.', 'danger')
            return render_template('contacto.html')

        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO correocontacto (nombre, email, telefono, asunto, mensaje) 
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, email, telefono, asunto, mensaje))
        conn.commit()
        cur.close()
        conn.close()

        admin_email = 'barberiasami7@gmail.com' 
        msg_to_admin = Message('Nuevo Mensaje de Contacto', sender=app.config['MAIL_USERNAME'], recipients=[admin_email])
        msg_to_admin.body = f'Un nuevo mensaje de contacto ha sido enviado:\n\nNombre: {nombre}\nEmail: {email}\nTeléfono: {telefono}\nAsunto: {asunto}\nMensaje: {mensaje}'
        mail.send(msg_to_admin)

        msg_to_user = Message('Confirmación de Contacto', sender=app.config['MAIL_USERNAME'], recipients=[email])
        msg_to_user.body = f'Se ha enviado una solicitud de contacto, pronto nos pondremos en contacto contigo.\n\nNombre: {nombre}\nAsunto: {asunto}\nMensaje: {mensaje}'
        mail.send(msg_to_user)

        flash('Tu mensaje ha sido enviado correctamente.', 'success')
        return render_template('contacto.html')
    else:
        return render_template('contacto.html')

@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('panel_administrador'))

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        return jsonify(success=False, message="Usuario no autenticado")

    user_id = session['user_id']
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT name, last_name, email FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    if not user:
        return jsonify(success=False, message="Usuario no encontrado")

    name, last_name, email = user

    try:
        cur.execute("DELETE FROM reservas WHERE usuario_id = %s", (user_id,))
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()

        admin_email = 'barberiasami7@gmail.com'
        msg_to_admin = Message('Baja de Usuario', sender=app.config['MAIL_USERNAME'], recipients=[admin_email])
        msg_to_admin.body = f'Un usuario se ha dado de baja:\n\nNombre: {name} {last_name}\nEmail: {email}'
        mail.send(msg_to_admin)

        msg_to_user = Message('Despedida de Barbería SAMI', sender=app.config['MAIL_USERNAME'], recipients=[email])
        msg_to_user.body = f'Hola {name},\n\nLamentamos que te vayas. Gracias por haber sido parte de Barbería SAMI. ¡Esperamos verte pronto de nuevo!'
        mail.send(msg_to_user)

        session.clear()
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, message=str(e))
    finally:
        cur.close()
        conn.close()

@app.route('/cancel_reservation/<int:id>', methods=['POST'])
def cancel_reservation(id):
    if 'admin' not in session or not session['admin']:
        return jsonify(success=False, message="No autorizado")

    cancel_reason = request.form.get('cancelReason')

    conn = connect_db()
    cur = conn.cursor()

    try:
        # Obtener detalles de la reserva y del usuario para el correo
        cur.execute("""
            SELECT u.email, u.name, r.dia, r.hora, r.datetime, r.servicio 
            FROM reservas r 
            JOIN users u ON r.usuario_id = u.id 
            WHERE r.id = %s
        """, (id,))
        reserva = cur.fetchone()

        if not reserva:
            return jsonify(success=False, message="Reserva no encontrada")

        user_email, user_name, dia, hora, datetime_reserva, servicio = reserva

        # Eliminar la reserva
        cur.execute("DELETE FROM reservas WHERE id = %s", (id,))
        conn.commit()

        # Enviar correo electrónico al usuario con la razón de la cancelación
        msg_to_user = Message('Cancelación de Reserva', sender=app.config['MAIL_USERNAME'], recipients=[user_email])
        msg_to_user.body = f'Hola {user_name},\n\nLamentamos informarte que tu reserva ha sido cancelada.\n\nRazón de la cancelación: {cancel_reason}\n\nDetalles de la reserva:\nDía: {dia}\nHora: {hora}\nFecha y Hora: {datetime_reserva}\nServicio: {servicio}\n\nDisculpa las molestias ocasionadas.'
        mail.send(msg_to_user)

        flash('Reserva cancelada y correo enviado al usuario.', 'success')
        return redirect(url_for('panel_administrador'))
    except Exception as e:
        flash(f'Error al cancelar la reserva: {str(e)}', 'danger')
        return redirect(url_for('panel_administrador'))
    finally:
        cur.close()
        conn.close()

@app.route('/delete_valoracion/<nombre>/<valoracion>', methods=['POST'])
def delete_valoracion(nombre, valoracion):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM valoraciones WHERE nombre = %s  AND valoracion = %s", (nombre, valoracion))
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

        cursor.execute("SELECT dia, hora, datetime, servicio FROM reservas WHERE id=%s AND usuario_id=%s", (id, user_id))
        reserva = cursor.fetchone()

        if not reserva:
            return jsonify({'message': 'Reserva no encontrada o no autorizada'}), 404

        cursor.execute("DELETE FROM reservas WHERE id=%s AND usuario_id=%s", (id, user_id))
        connection.commit()

        admin_email = 'barberiasami7@gmail.com'
        username = session['users']
        dia, hora, datetime_reserva, servicio = reserva
        msg_to_admin = Message('Cancelación de Reserva', sender=app.config['MAIL_USERNAME'], recipients=[admin_email])
        msg_to_admin.body = f'El usuario {username} ha cancelado la siguiente reserva:\n\nDía: {dia}\nHora: {hora}\nFecha y hora: {datetime_reserva}\nServicio: {servicio}'
        mail.send(msg_to_admin)

        cursor.close()
        connection.close()
        return jsonify({'message': 'Reserva eliminada con éxito'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@app.route('/assign_admin', methods=['POST'])
def assign_admin():
    user_id = request.form.get('user_id')
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET admin = TRUE WHERE id = %s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()
    flash('Usuario asignado como trabajador con éxito.', 'success')
    return redirect(url_for('panel_administrador'))

@app.route('/remove_admin', methods=['POST'])
def remove_admin():
    user_id = request.form.get('user_id')
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET admin = FALSE WHERE id = %s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()
    flash('Rol de trabajador removido con éxito.', 'success')
    return redirect(url_for('panel_administrador'))

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
