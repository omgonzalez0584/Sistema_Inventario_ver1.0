from flask import Flask, flash, url_for, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///libros.sqlite3'
app.config['SECRET_KEY'] = 'uippc3'

db = SQLAlchemy(app)
class libros(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    materia = db.Column(db.String(50))
    autor = db.Column(db.String(200))
    cantidad = db.Column(db.Integer)
    precio = db.Column(db.String(10))

    def __init__(self, nombre, autor, materia, cantidad,precio):
        self.nombre = nombre
        self.autor = autor
        self.materia = materia
        self.cantidad = cantidad
        self.precio = precio

@app.route('/')
def mostrar_todo():
    return render_template('mostrar_todo.html', libros=libros.query.all())

@app.route('/nuevo/', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        if not request.form['nombre'] or not request.form['autor'] or not request.form['materia']:
            flash('Por favor introduzca todos los campos', 'error')
        else:
            libro = libros(request.form['nombre'],
                                     request.form['autor'],
                                     request.form['materia'],
                                     request.form['cantidad'],request.form['precio'])
            db.session.add(libro)
            db.session.commit()
            flash('Registro guardado con exito!')
            return redirect(url_for('mostrar_todo'))
    return render_template('nuevo.html')


@app.route('/eliminar/',methods =['GET','POST'])
def eliminar():
    if request.method == 'POST':
        borrar = request.form['id']
        u = libros.query.get(borrar)
        db.session.delete(u)
        db.session.commit()
        return redirect(url_for('mostrar_todo'))

@app.route('/comprar/',methods = ['GET','POST'])
def comprar():
    if request.method == 'POST':
        comprar = request.form['id']
        u = libros.query.get(comprar)
        int(u.cantidad)
        flag =  u.cantidad
        flag = int(flag) - 1
        print(flag)
        u.cantidad = flag
        db.session.commit()
        flash('Libro Vendido!')
        return redirect(url_for('mostrar_todo'))


if __name__ == '__main__':
 db.create_all()
app.run()
