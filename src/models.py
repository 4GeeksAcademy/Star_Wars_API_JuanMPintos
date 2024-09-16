from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    relation_favoritos = db.relationship('Favoritos', backref='user')

class Personajes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    lightsaber_user = db.Column(db.Boolean(),unique=False, nullable=False)

    relation_favoritos = db.relationship('Favoritos', backref='personajes')


class Planetas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    relation_favoritos = db.relationship('Favoritos', backref='planetas')

class Favoritos(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    planeta_favorito = db.Column(db.String(30), db.ForeignKey('planetas.name'))
    personaje_favorito = db.Column(db.String(30), db.ForeignKey('personajes.name'))
 

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }