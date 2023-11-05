from flask import Flask, render_template, request, redirect, session , flash 
from flask_mysqldb import MySQL
from route.usuario import usuario 
from route.vehiculo import vehiculo1
from route.orden import ORDEN

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





app.register_blueprint(ORDEN)
app.register_blueprint(vehiculo1)
app.register_blueprint(usuario)
if __name__ == '__main__':
    app.secret_key="daniel_forero"
    app.run(debug=True , host='0.0.0.0', port=5000 , threaded=True) 






    

    

        
 

       

    
