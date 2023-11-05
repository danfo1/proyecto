from flask import Flask, render_template, request, redirect, session , flash , Blueprint
import os
from flask_mysqldb import MySQL


usuario=Blueprint('usuario',__name__)
template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir,  'templates')

app = Flask(__name__, template_folder=template_dir)
mysql = MySQL(app)


        

@usuario.route("/correo", methods=['GET', 'POST'])
def correo():
    if request.method == 'POST':
        correo = request.form.get('correo')
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuario WHERE correo = %s", (correo,))
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            session['logeado'] = True
            session['correo'] = user['correo']
            return render_template('usuario/contraseña.html', correo=user['correo'])
        else:
            flash("Correo no encontrado")
        
    return render_template('usuario/correo.html')

@usuario.route('/actualizar_contraseña', methods=['POST'])
def actualizar_contraseña():
    if 'logeado' in session and session['logeado']:
        contrasena_nueva = request.form.get('contrasena_nueva')
        confirmar_contrasena = request.form.get('confirmar_contrasena')

        # Validar que la "Contraseña Nueva" y la "Confirmar Contraseña" coincidan
        if contrasena_nueva != confirmar_contrasena:
            flash("Error al actualizar la contraseña. Las contraseñas no coinciden.", 'error')
            return redirect('/correo')  # Redirige de vuelta a la página de inicio de sesión o recuperación de contraseña

        correo = session.get('correo')
        cursor = mysql.connection.cursor()
        sql = ("UPDATE usuario SET contrasena = %s WHERE correo = %s")
        data = (contrasena_nueva, correo)
        cursor.execute(sql, data)
        mysql.connection.commit()
        cursor.close()
        session.clear()
        flash("Contraseña actualizada con éxito", 'success')
    
    return redirect('/correo')
    

@usuario.route('/usuario.registrar', methods=['GET', 'POST'])
def registrarse():
    if request.method == 'POST':
        nombres = request.form["nombres"]
        apellidos = request.form["apellidos"]
        tipo_documento = request.form["tipo_documento"]
        num_documento = request.form["num_documento"]  
        correo = request.form["correo"]
        telefono = request.form["telefono"]
        telefono_respaldo = request.form["telefono_respaldo"]
        estado = request.form["estado"]
        contrasena = request.form["contrasena"]
        nombreusu = request.form["usuario"]
        rol = request.form["rol"]
        
        if nombres and apellidos and tipo_documento and num_documento and correo and telefono and telefono_respaldo and estado and contrasena and nombreusu and rol:
            cursor = mysql.connection.cursor()
            sql = "INSERT INTO usuario (nombres, apellidos, tipo_documento, num_documento, correo, telefono, telefeno_respaldo, estado, contrasena, nombreusu, fk_id_rol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (nombres, apellidos, tipo_documento, num_documento, correo, telefono, telefono_respaldo, estado, contrasena, nombreusu, rol)
            cursor.execute(sql, data)
            mysql.connection.commit()
            cursor.close() 
            return "Usuario registrado con éxito."
        if not all([nombres, apellidos, tipo_documento, num_documento, correo, telefono, estado, contrasena, nombreusu]):
            return "Por favor, complete todos los campos obligatorios."
        
        return render_template('usuario/registrar.html')

    return render_template('usuario/registrar.html')



@usuario.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuario WHERE idusu = %s", (id,))
        data = cursor.fetchone()
        cursor.close()

        if data:
            return render_template('usuario/editar.html', data=data)
        else:
            return "No encontrado"
    elif request.method == 'POST':
        nombres = request.form.get('nombres')
        apellidos = request.form.get('apellidos')
        tipo_documento = request.form.get('tipo_documento')
        num_documento = request.form.get('num_documento')
        correo = request.form.get('correo')
        telefono = request.form.get('telefono')
        telefeno_respaldo = request.form.get('telefeno_respaldo')
        estado = request.form.get('estado')
        contrasena = request.form.get('contrasena')
        nombreusu = request.form.get('nombreusu')
        rol = request.form.get('rol')
        
        cursor = mysql.connection.cursor()
        sql = ("UPDATE usuario SET nombres = %s, apellidos = %s, tipo_documento = %s, num_documento = %s, correo = %s, telefono = %s, telefeno_respaldo = %s, estado = %s, contrasena = %s, nombreusu = %s WHERE idusu = %s")
        data = (nombres, apellidos, tipo_documento, num_documento, correo, telefono, telefeno_respaldo , estado, contrasena, nombreusu, rol)
        cursor.execute(sql, data)
        mysql.connection.commit()
        cursor.close()
        return "Datos actualizados con éxito."

    return render_template('usuario/editar.html', id=id)

@usuario.route('/eliminar/<int:idusu>', methods=['GET', 'POST'])
def eliminar(idusu):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuario WHERE idusu = %s", (idusu,))
        data = cursor.fetchone()
        cursor.close()

        if data:
            return render_template('usuario/eliminar.html', data=data)
        else:
            return "No encontrado"

    elif request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM usuario WHERE idusu = %s", (idusu,))
        mysql.connection.commit()
        cursor.close()
        return "Datos eliminados"
app.register_blueprint(usuario)
if __name__ == '__main__':
    app.run(debug=True)