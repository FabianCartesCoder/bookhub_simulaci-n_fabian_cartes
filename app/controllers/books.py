from flask import render_template, redirect, request, session, flash
from app import app
from app.models.book import Book

@app.route('/libros')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    user_books = Book.get_by_user(session['user_id'])
    community_books = Book.get_community_books(session['user_id'])
    return render_template('books/dashboard.html', user_books=user_books, community_books=community_books)

@app.route('/libros/nuevo')
def new_book():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('books/new.html')

@app.route('/libros/crear', methods=['POST'])
def create_book():
    if 'user_id' not in session:
        return redirect('/')

    if not Book.validate_book(request.form):
        return redirect('/libros/nuevo')

    data = {
        'title': request.form['title'],
        'author': request.form['author'],
        'genre': request.form['genre'],
        'publication_date': request.form['publication_date'],
        'description': request.form['description'],
        'user_id': session['user_id']
    }
    Book.save(data)
    return redirect('/libros')

@app.route('/libros/<int:id>')
def show_book(id):
    if 'user_id' not in session:
        return redirect('/')

    book = Book.get_by_id(id)
    if not book:
        return redirect('/libros')

    favorited_users = Book.get_favorited_users(id)
    is_favorited = any(u['id'] == session['user_id'] for u in favorited_users)

    return render_template('books/show.html', book=book, favorited_users=favorited_users, is_favorited=is_favorited)

@app.route('/libros/editar/<int:id>')
def edit_book(id):
    if 'user_id' not in session:
        return redirect('/')

    book = Book.get_by_id(id)
    if not book or book.user_id != session['user_id']:
        return redirect('/libros')

    return render_template('books/edit.html', book=book)

@app.route('/libros/actualizar/<int:id>', methods=['POST'])
def update_book(id):
    if 'user_id' not in session:
        return redirect('/')

    book = Book.get_by_id(id)
    if not book or book.user_id != session['user_id']:
        return redirect('/libros')

    if not Book.validate_book(request.form):
        return redirect(f'/libros/editar/{id}')

    data = {
        'id': id,
        'title': request.form['title'],
        'author': request.form['author'],
        'genre': request.form['genre'],
        'publication_date': request.form['publication_date'],
        'description': request.form['description'],
        'user_id': session['user_id']
    }
    Book.update(data)
    return redirect('/libros')

@app.route('/libros/eliminar/<int:id>')
def delete_book(id):
    if 'user_id' not in session:
        return redirect('/')

    Book.delete(id, session['user_id'])
    return redirect('/libros')

@app.route('/libros/favorito/<int:id>', methods=['POST'])
def add_favorite(id):
    if 'user_id' not in session:
        return redirect('/')

    Book.add_favorite(session['user_id'], id)
    return redirect(f'/libros/{id}')

@app.route('/favoritos')
def favorites():
    if 'user_id' not in session:
        return redirect('/')

    favorite_books = Book.get_user_favorites(session['user_id'])
    return render_template('books/favorites.html', books=favorite_books)