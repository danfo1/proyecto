from flask import Flask, render_template, request, redirect, session , flash , Blueprint
import os
from flask_mysqldb import MySQL
vehiculo1=Blueprint('vehiculo',__name__)
template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir,  'templates')

app = Flask(__name__, template_folder=template_dir)
mysql = MySQL(app)



@vehiculo1.route("/vehiculo.registro_vehiculo", methods=['GET', 'POST'])
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
    return render_template('vehiculo/rvehiculo.html')


@vehiculo1.route("/vehiculo.editar_vehiculo/<int:id_vehiculo>", methods=['GET', 'POST'])
def editar_vehiculo(id_vehiculo):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM vehiculo WHERE id_vehiculo=%s", (id_vehiculo ,))
        data = cursor.fetchone()
        cursor.close()
        
        if data:
            return render_template('vehiculo/editarvehiculo.html', data=data)
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
    return render_template('vehiculo/editarvehiculo.html')

@vehiculo1.route('/vehiculo.eliminar_vehiculo/<int:id_vehiculo>', methods=['GET', 'POST'])
def eliminar_vehiculo(id_vehiculo):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM vehiculo WHERE id_vehiculo = %s", (id_vehiculo,))
        data = cursor.fetchone()
        cursor.close()

        if data:
            return render_template('vehiculo/eliminar_vehiculo.html', data=data)
        else:
            return "No encontrado"

    elif request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM vehiculo WHERE id_vehiculo = %s", (id_vehiculo,))
        mysql.connection.commit()
        cursor.close()
        return "Datos eliminados"
    
app.register_blueprint(vehiculo1)
if __name__ == '__main__':
    app.run(debug=True)
    