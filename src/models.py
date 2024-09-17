from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user' 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    favoritos = db.relationship('Favoritos', backref='user')

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class Personajes(db.Model):
    __tablename__ = 'personajes' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    lightsaber_user = db.Column(db.Boolean(), unique=False, nullable=False)

    favoritos = db.relationship('Favoritos', backref='personajes')

    def __repr__(self):
        return '<Personajes %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lightsaber_user": self.lightsaber_user
        }

class Planetas(db.Model):
    __tablename__ = 'planetas' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    favoritos = db.relationship('Favoritos', backref='planetas')

    def __repr__(self):
        return '<Planetas %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

class Favoritos(db.Model):
    __tablename__ = 'favoritos' 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planeta_id = db.Column(db.Integer, db.ForeignKey('planetas.id'))
    personaje_id = db.Column(db.Integer, db.ForeignKey('personajes.id'))

    def __repr__(self):
        return '<Favoritos %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planeta_id": self.planeta_id,
            "personaje_id": self.personaje_id
        }











