from flask import Flask,render_template,request, redirect, url_for
from flask_mysqldb import MySQL
from config import config
app=Flask(__name__)

conexion=MySQL(app)
app.secret_key = "mysecretkey" # aqui inicializamos una sesion con nuestra aplicacion del servidor ya que cada aplicación web de Flask contiene una clave secreta que se utiliza para firmar cookies de sesión para protegerse contra la manipulación de datos de cookies.
   


@app.route('/')
def inicio():
    try:
     cursor = conexion.connection.cursor()
     cursor.execute("SELECT * FROM curso")
     registros=cursor.fetchall()
     cursor.close()
     return render_template("index.html",total_registros=registros)
    
    except Exception as e:
        return "Error"


#Agregar Nuevo Cursos
@app.route('/agregar',methods=['POST'])
def agregar_curso():
    try:
        if request.method=="POST":
            codigo = request.form['codigo']
            nombre_curso = request.form['nombre_curso'].title()
            creditos = request.form['creditos']
            profesor= request.form['profesor'].title()
            paralelo = request.form['paralelo'].upper()
            estado = request.form['estado'].title()
            cursor = conexion.connection.cursor()
            cursor.execute("INSERT INTO curso (codigo, nombre, creditos,profesor,paralelo,estado) VALUES (%s,%s,%s,%s,%s,%s)", (codigo, nombre_curso, creditos,profesor,paralelo,estado))
            conexion.connection.commit()
            return redirect(url_for('inicio'))
    except Exception as e:
        return"<h2>Código ya existente, no se puede duplicar.</h2>"




#Obtener un Solo Curso para poder editarlo
@app.route('/editar/<codigo>',methods=['GET'])
def obtener_un_curso_para_actualizarlo(codigo):
    try:
        cursor = conexion.connection.cursor()
        cursor.execute("SELECT * FROM curso WHERE codigo=%s",(codigo))
        registro=cursor.fetchall()
        cursor.close()
        return render_template("editar.html",registro_unico=registro[0])
    except Exception as e:
        return"<h2>No se pudo Acceder al Curso  para Actualizarlo</h2>"






#Editar Curso
@app.route('/actualizar/<codigo>',methods=['POST']) #uso el metodo POST para actualizar la informacion porque estoy recibiendo lo datos de un formulario mediante el metodo POST
def actualizar_curso(codigo):
    try:
        if request.method=="POST":
            nombre = request.form['nombre'].title()
            creditos = request.form['creditos']
            profesor= request.form['profesor'].title()
            paralelo = request.form['paralelo'].upper()
            estado = request.form['estado'].title()
            cursor = conexion.connection.cursor() 
            cursor.execute("UPDATE curso SET nombre=%s, creditos=%s,profesor=%s,paralelo=%s,estado=%s WHERE codigo=%s",(nombre,creditos,profesor,paralelo,estado,codigo))
            conexion.connection.commit()
            return  redirect(url_for('inicio'))
        else:
            return "No se pudo Actualizar el Curso"
    except Exception as e:
        return"<h2>Curso Inexistente</h2>"     


#Eliminar Curso
@app.route('/eliminar/<codigo>')
def eliminar_curso(codigo):
    try:
        cursor = conexion.connection.cursor()
        cursor.execute("DELETE FROM curso WHERE codigo={0}".format(codigo))
        conexion.connection.commit()
        return redirect(url_for('inicio'))
    
    except Exception as e:
        return"<h2>No Se pudo Eliminar el Curso</h2>"

def pagina_no_econtrada():
    return "<h1>Pagina no encontrada</h1>"

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_econtrada)
    app.run(port=4000)
