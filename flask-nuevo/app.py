from flask import Flask, flash, render_template, redirect, url_for, request, session
from dao.DAOEmpleado import DAOEmpleado
from dao.DAOUsuario import DAOUsuario

""" INICION DE RUTAS GENERALES """
app= Flask(__name__)
app.secret_key="Tec123"
db = DAOUsuario()
db2 = DAOEmpleado()
ruta='/usuario'

@app.route('/')
def inicio():
    return render_template('index.html')

""" FIN DE RUTAS GENERALES """

""" INICIO DE RUTAS DE USUARIO """

@app.route('/usuario/')
# @app.route('/usuario/')
def index():
    datos = db.read(None)

    return render_template('/usuario/index.html', data = datos)


@app.route('/añadir/')
def añadir():
    return render_template('/usuario/añadir.html')

@app.route('/añadirusuario/', methods = ['POST', 'GET'])
def añadirusuario():
    if request.method == 'POST' and request.form['save']:
        if db.insert(request.form):
            flash("Nuevo usuario creado")
        else:
            flash("ERROR, al crear usuario")

        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))



@app.route('/editar/<id>/')
def editar(id):
    datos = db.read(id);

    if len(datos) == 0:
        return redirect(url_for('index'))
    else:
        session['update'] = id
        return render_template('usuario/editar.html', data = datos)

@app.route('/editarusuario/', methods = ['POST'])   
def editarusuario():
    if request.method == 'POST' and request.form['update']:

        if db.update(session['update'], request.form):
            flash('Se actualizo correctamente')
        else:
            flash('ERROR en actualizar')

        session.pop('update', None)

        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))



@app.route('/eliminar/<id>/')
def eliminar(id):
    datos = db.read(id);

    if len(datos) == 0:
        return redirect(url_for('index'))
    else:
        session['delete'] = id
        return render_template('usuario/eliminar.html', data = datos)

@app.route('/eliminarusuario/', methods = ['POST'])
def eliminarusuario():
    if request.method == 'POST' and request.form['delete']:

        if db.delete(session['delete']):
            flash('Usuario eliminado')
        else:
            flash('ERROR al eliminar')
        session.pop('delete', None)

        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


""" INICIO DE RUTAS DE EMPLEADO """
@app.route('/empleado/')
# @app.route('/usuario/')
def indexe():
    datos2 = db.read(None)
    return render_template('/empleado/index.html', data = datos2)





if __name__ == '__main__':
    app.run(port=3000, host="0.0.0.0",debug=True)
