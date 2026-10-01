from flask import render_template, redirect, request, session, flash
from app import app, bcrypt
from app.models.user import User

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/libros')
    return render_template('users/index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')

    hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
    user_data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': hashed_password
    }
    user_id = User.save(user_data)

    session['user_id'] = user_id
    session['user_name'] = request.form['first_name']
    return redirect('/libros')

@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email({'email': request.form['email']})
    if not user or not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Credenciales inválidas.", "login_error")
        return redirect('/')

    session['user_id'] = user.id
    session['user_name'] = user.first_name
    return redirect('/libros')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')