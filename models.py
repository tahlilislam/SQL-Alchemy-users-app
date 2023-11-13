"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


DEFAULT_IMAGE_URL = "https://images.unsplash.com/photo-1634896941598-b6b500a502a7?w=1200&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fGF2YXRhciUyMGltYWdlfGVufDB8fDB8fHww"


class User(db.Model):
    """User"""

    __tablename__ = "users"

    def __repr__(self):
        u = self
        return f"<User id = {u.id} first_name = {u.first_name} last_name = {u.last_name} image_url = {u.image_url}>"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                          nullable=False)
    image_url = db.Column(db.Text,
                          nullable=False,
                          default=DEFAULT_IMAGE_URL)
    
    def full_name(self):
        """Return full name of user."""
        return f"{self.first_name} {self.last_name}"

# class Pet(db.Model):
#     """Pet."""
#     __tablename__ = "pets"

#     @classmethod
#     def get_by_species(cls, species):
#         return cls.query.filter_by(species=species).all()

#     @classmethod
#     def get_all_hungry(cls):
#         return cls.query.filter(Pet.hunger > 20).all()

#     def __repr__(self):
#         p = self
#         return f"<Pet id = {p.id} name = {p.name} species ={p.species} hunger = {p.hunger}>"

#     id = db.Column(db.Integer,
#                    primary_key=True,
#                    autoincrement=True)
#     name = db.Column(db.String(50),
#                      nullable=False,
#                      unique=True)
#     species = db.Column(db.String(30), nullable=True)

#     hunger = db.Column(db.Integer, nullable=False, default=20)

#     def greet(self):
#         return f"Hi, I am {self.name} the {self.species}"

#     def feed(self, amt=20):
#         """Update hunger based off of amt"""
#         self.hunger -= amt
#         self.hunger = max(self.hunger, 0)
