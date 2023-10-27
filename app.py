from flask import Flask, render_template, request, redirect, session , flash 
from flask_mysqldb import MySQL
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'perfil'
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql = MySQL(app)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST' and 'usuario' in request.form and 'contrasena' in request.form:
        nombreusu = request.form['usuario']
        contrasena = request.form['contrasena']
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuario WHERE nombreusu=%s and contrasena=%s", (nombreusu, contrasena))
        account = cursor.fetchone()  # Utiliza fetchone para obtener una sola fila
        cursor.close()  # Cierra el cursor después de usarlo
        
        if account:
            session['logeado'] = True
            session['id'] = account['idusu']
            return render_template('inicio.html')  
        else:   
            flash('Nombre de usuario o contraseña incorrectos')
        
    return render_template('login.html')

    
@app.route("/correo", methods=['GET', 'POST'])
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
            return render_template('contraseña.html', correo=user['correo'])
        else:
            flash("Correo no encontrado")
        
    return render_template('correo.html')

@app.route('/actualizar_contraseña', methods=['POST'])
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
    
    

        
 


@app.route('/registrar', methods=['GET', 'POST'])
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
        else:
            return render_template('registrar.html')
    return render_template('registrar.html')


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuario WHERE idusu = %s", (id,))
        data = cursor.fetchone()
        cursor.close()

        if data:
            return render_template('editar.html', data=data)
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

    return render_template('editar.html', id=id)

@app.route('/eliminar/<int:idusu>', methods=['GET', 'POST'])
def eliminar(idusu):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuario WHERE idusu = %s", (idusu,))
        data = cursor.fetchone()
        cursor.close()

        if data:
            return render_template('eliminar.html', data=data)
        else:
            return "No encontrado"

    elif request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM usuario WHERE idusu = %s", (idusu,))
        mysql.connection.commit()
        cursor.close()
        return "Datos eliminados"
       
@app.route("/registro_vehiculo", methods=['GET', 'POST'])
def vehiculo():
    if request.method == 'POST':
        modelo = request.form["modelo"]
        marca = request.form["marca"]
        color = request.form["color"]
        placa = request.form["placa"]
        cilindraje = request.form["cilindraje"]
        kilometraje = request.form["kilometraje"]
        referencia = request.form["referencia"]
        tipo_combustible = request.form["tipo_combustible"]

        if modelo and marca and color and placa and cilindraje and kilometraje and referencia and tipo_combustible:
            cursor = mysql.connection.cursor()
            sql = ("INSERT INTO vehiculo (modelo, marca, color, placa, cilindraje, kilometraje, referencia, tipo_conbustible) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
            data = (modelo, marca, color, placa, cilindraje, kilometraje, referencia, tipo_combustible)
            cursor.execute(sql, data)
            mysql.connection.commit()
            cursor.close()
            return "vehiculo registrado "
    return render_template('rvehiculo.html')

@app.route("/editar_vehiculo/<int:id_vehiculo>", methods=['GET', 'POST'])
def editar_vehiculo(id_vehiculo):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM vehiculo WHERE id_vehiculo=%s", (id_vehiculo ,))
        data = cursor.fetchone()
        cursor.close()
        
        if data:
            return render_template('editarvehiculo.html', data=data)
        else:
            return "No se encontró el vehículo"
    elif request.method == 'POST':
        modelo = request.form["modelo"]
        marca = request.form["marca"]
        color = request.form["color"]
        placa = request.form["placa"]
        cilindraje = request.form["cilindraje"]
        kilometraje = request.form["kilometraje"]
        referencia = request.form["referencia"]
        tipo_combustible = request.form["tipo_combustible"]

        cursor = mysql.connection.cursor()
        sql = ("UPDATE vehiculo SET modelo=%s, marca=%s, color=%s, placa=%s, cilindraje=%s, kilometraje=%s, referencia=%s, tipo_conbustible=%s "
               "WHERE id_vehiculo =%s")
        data = (modelo, marca, color, placa, cilindraje, kilometraje, referencia, tipo_combustible, id_vehiculo)
        cursor.execute(sql, data)
        mysql.connection.commit()
        cursor.close()
        return "Datos actualizados"
    return render_template('editarvehiculo.html')

@app.route('/eliminar_vehiculo/<int:id_vehiculo>', methods=['GET', 'POST'])
def eliminar_vehiculo(id_vehiculo):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM vehiculo WHERE id_vehiculo = %s", (id_vehiculo,))
        data = cursor.fetchone()
        cursor.close()

        if data:
            return render_template('eliminar vehiculo.html', data=data)
        else:
            return "No encontrado"

    elif request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM vehiculo WHERE id_vehiculo = %s", (id_vehiculo,))
        mysql.connection.commit()
        cursor.close()
        return "Datos eliminados"
    
@app.route('/editar_orden/<int:id_orden>', methods=['GET', 'POST'])
def editar_orden(id_orden):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM orden_trabajo WHERE id_orden=%s", (id_orden,))
        data = cursor.fetchone()
        cursor.close()
        
        if data:
            return render_template('editarorden.html', data=data)
        else:
            return "No se encontró la orden de trabajo"
    elif request.method == 'POST':
        descripcion = request.form["descripcion"]
        radio = request.form["radio"]
        antena = request.form["antena"]
        encendedor = request.form["encendedor"]
        tapetes = request.form["tapetes"]
        soat = request.form["soat"]
        grua = request.form["grua"]
        estado_llantas = request.form["estado_llantas"]
        llave_pernos = request.form["llave_pernos"]
        llanta_repuesto = request.form["llanta_repuesto"]
        tapa_gasolina = request.form["tapa_gasolina"]
        kit_carretera = request.form["kit_carretera"]
        copas = request.form["copas"]
        tarjeta_de_propiedad = request.form["tarjeta_de_propiedad"]
        estado_proceso = request.form["estado_proceso"]
        periodo_de_tiempo_ini = request.form["periodo_de_tiempo_ini"]
        periodo_de_tiempo_fin = request.form["periodo_de_tiempo_fin"]
        herramientas = request.form["herramientas"]
     
        cursor = mysql.connection.cursor()
        sql = ("UPDATE orden_trabajo SET descripcion=%s, radio=%s, antena=%s, encendedor=%s, tapetes=%s, soat=%s, grua=%s, estado_llantas=%s, llave_pernos=%s, llanta_repuesto=%s, tapa_gasolina=%s, kit_carretera=%s, copas=%s, tarjeta_de_propiedad=%s, estado_proceso=%s, periodo_de_tiempo_ini=%s, periodo_de_tiempo_fin=%s, herramientas=%s WHERE id_orden=%s")
        data = (descripcion, radio, antena, encendedor, tapetes, soat, grua, estado_llantas, llave_pernos, llanta_repuesto, tapa_gasolina, kit_carretera, copas, tarjeta_de_propiedad, estado_proceso, periodo_de_tiempo_ini, periodo_de_tiempo_fin, herramientas, id_orden)
        cursor.execute(sql, data)
        mysql.connection.commit()
        cursor.close()
        
        return "Datos actualizados"
    return render_template('editarorden.html')  


if __name__ == '__main__':
    app.secret_key="daniel_forero"
    app.run(debug=True , host='0.0.0.0', port=5000 , threaded=True) 