from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String, ForeignKey

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    password: Mapped[str] = mapped_column(String(80))
    is_active: Mapped[bool]
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }

class User_favs(db.Model):
    __tablename__ = "user_favs"

    id: Mapped[int] = mapped_column(primary_key=True)
    favs_people_id: Mapped[int] = mapped_column(ForeignKey("favs_people.id"))
    favs_planets_id: Mapped[int] = mapped_column(ForeignKey("favs_planets.id"))
    
    def serialize(self):
        favs_people = db.session.execute(db.select(Favs_people).filter_by(id=self.favs_people_id)).scalar_one()
        favs_planets = db.session.execute(db.select(Favs_planets).filter_by(id=self.favs_planets_id)).scalar_one()
        return {
            "id": self.id,
            "favs_people": favs_people.serialize(),
            "favs_planets": favs_planets.serialize()
        }
    
class Planets(db.Model):
    __tablename__ = 'planets'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    climate: Mapped[str] = mapped_column(nullable=False)
    diameter: Mapped[str] = mapped_column(nullable=False)
    gravity: Mapped[str] = mapped_column(nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "gravity": self.gravity
        }

class People(db.Model):
    __tablename__ = 'people'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    birth_year: Mapped[str] = mapped_column(nullable=False)
    eye_color: Mapped[str] = mapped_column(nullable=False)
    hair_color: Mapped[str] = mapped_column(nullable=False)
    height: Mapped[int] = mapped_column(nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
            "height": self.height
        }
    
class Favs_planets(db.Model):
    __tablename__ = 'favs_planets'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    users_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    planets_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))
    
    def serialize(self):
        planet = db.session.execute(db.select(Planets).filter_by(id=self.planets_id)).scalar_one()
        return {
            "id": self.id,
            "planet": planet.serialize()
        }

class Favs_people(db.Model):
    __tablename__ = 'favs_people'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    users_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    people_id: Mapped[int] = mapped_column(ForeignKey("people.id"))

    def serialize(self):
        people = db.session.execute(db.select(People).filter_by(id=self.people_id)).scalar_one()
        return {
            "id": self.id,
            "people": people.serialize()
        }