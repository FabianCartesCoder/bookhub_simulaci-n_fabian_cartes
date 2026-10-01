import re
from flask import flash
from app.config.mysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DB = 'bookhub_db'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DB).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate_register(user):
        is_valid = True

        if len(user.get('first_name', '').strip()) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "register_first_name")
            is_valid = False

        if len(user.get('last_name', '').strip()) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "register_last_name")
            is_valid = False

        if not EMAIL_REGEX.match(user.get('email', '')):
            flash("Formato de correo electrónico inválido.", "register_email")
            is_valid = False
        else:
            existing_user = User.get_by_email({'email': user['email']})
            if existing_user:
                flash("El correo electrónico ya está registrado.", "register_email")
                is_valid = False

        if len(user.get('password', '')) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "register_password")
            is_valid = False

        if user.get('password') != user.get('confirm_password'):
            flash("Las contraseñas no coinciden.", "register_confirm")
            is_valid = False

        return is_valid