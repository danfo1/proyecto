from flask import Flask, render_template, request, redirect, session , flash , Blueprint
import os
from flask_mysqldb import MySQL


ORDEN=Blueprint('ORDEN',__name__)
template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir,  'templates')

app = Flask(__name__, template_folder=template_dir)
mysql = MySQL(app)


@ORDEN.route('/orden.editar_orden/<int:id_orden>', methods=['GET', 'POST'])
def editar_orden(id_orden):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM orden_trabajo WHERE id_orden=%s", (id_orden,))
        data = cursor.fetchone()
        cursor.close()
        
        if data:
            return render_template('orden/editarorden.html', data=data)
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
    return render_template('orden/editarorden.html')  
app.register_blueprint(ORDEN)
if __name__ == '__main__':
    app.run(debug=True)