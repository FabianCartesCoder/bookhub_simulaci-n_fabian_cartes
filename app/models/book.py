from datetime import datetime
from flask import flash
from app.config.mysqlconnection import connectToMySQL

DB = 'bookhub_db'

class Book:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.author = data['author']
        self.genre = data['genre']
        self.publication_date = data['publication_date']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator_name = data.get('creator_name', '')
        self.favorites_count = data.get('favorites_count', 0)

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO books (title, author, genre, publication_date, description, user_id)
            VALUES (%(title)s, %(author)s, %(genre)s, %(publication_date)s, %(description)s, %(user_id)s);
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def get_by_user(cls, user_id):
        query = """
            SELECT b.*, COUNT(f.user_id) AS favorites_count
            FROM books b
            LEFT JOIN favorites f ON b.id = f.book_id
            WHERE b.user_id = %(user_id)s
            GROUP BY b.id
            ORDER BY b.created_at DESC;
        """
        results = connectToMySQL(DB).query_db(query, {'user_id': user_id})
        books = []
        if results:
            for row in results:
                books.append(cls(row))
        return books

    @classmethod
    def get_community_books(cls, user_id):
        query = """
            SELECT b.*, 
                   CONCAT(u.first_name, ' ', u.last_name) AS creator_name,
                   COUNT(f.user_id) AS favorites_count
            FROM books b
            JOIN users u ON b.user_id = u.id
            LEFT JOIN favorites f ON b.id = f.book_id
            WHERE b.user_id != %(user_id)s
            GROUP BY b.id
            ORDER BY b.created_at DESC;
        """
        results = connectToMySQL(DB).query_db(query, {'user_id': user_id})
        books = []
        if results:
            for row in results:
                books.append(cls(row))
        return books

    @classmethod
    def get_by_id(cls, book_id):
        query = """
            SELECT b.*, CONCAT(u.first_name, ' ', u.last_name) AS creator_name
            FROM books b
            JOIN users u ON b.user_id = u.id
            WHERE b.id = %(id)s;
        """
        results = connectToMySQL(DB).query_db(query, {'id': book_id})
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_favorited_users(cls, book_id):
        query = """
            SELECT u.id, u.first_name, u.last_name
            FROM favorites f
            JOIN users u ON f.user_id = u.id
            WHERE f.book_id = %(book_id)s;
        """
        return connectToMySQL(DB).query_db(query, {'book_id': book_id})

    @classmethod
    def get_user_favorites(cls, user_id):
        query = """
            SELECT b.*, CONCAT(u.first_name, ' ', u.last_name) AS creator_name
            FROM favorites f
            JOIN books b ON f.book_id = b.id
            JOIN users u ON b.user_id = u.id
            WHERE f.user_id = %(user_id)s
            ORDER BY f.created_at DESC;
        """
        results = connectToMySQL(DB).query_db(query, {'user_id': user_id})
        books = []
        if results:
            for row in results:
                books.append(cls(row))
        return books

    @classmethod
    def add_favorite(cls, user_id, book_id):
        query = "INSERT IGNORE INTO favorites (user_id, book_id) VALUES (%(user_id)s, %(book_id)s);"
        return connectToMySQL(DB).query_db(query, {'user_id': user_id, 'book_id': book_id})

    @classmethod
    def update(cls, data):
        query = """
            UPDATE books
            SET title = %(title)s, author = %(author)s, genre = %(genre)s,
                publication_date = %(publication_date)s, description = %(description)s
            WHERE id = %(id)s AND user_id = %(user_id)s;
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def delete(cls, book_id, user_id):
        query = "DELETE FROM books WHERE id = %(id)s AND user_id = %(user_id)s;"
        return connectToMySQL(DB).query_db(query, {'id': book_id, 'user_id': user_id})

    @staticmethod
    def validate_book(data):
        is_valid = True

        if len(data.get('title', '').strip()) < 2:
            flash("El título debe tener al menos 2 caracteres.", "book_title")
            is_valid = False

        if len(data.get('author', '').strip()) < 2:
            flash("El autor debe tener al menos 2 caracteres.", "book_author")
            is_valid = False

        if not data.get('genre'):
            flash("Debes seleccionar un género.", "book_genre")
            is_valid = False

        pub_date_str = data.get('publication_date', '')
        if not pub_date_str:
            flash("La fecha de publicación es obligatoria.", "book_date")
            is_valid = False
        else:
            try:
                pub_date = datetime.strptime(pub_date_str, '%Y-%m-%d').date()
                if pub_date > datetime.now().date():
                    flash("La fecha de publicación no puede ser una fecha futura.", "book_date")
                    is_valid = False
            except ValueError:
                flash("Formato de fecha inválido.", "book_date")
                is_valid = False

        if len(data.get('description', '').strip()) < 10:
            flash("La descripción debe tener al menos 10 caracteres.", "book_description")
            is_valid = False

        return is_valid