"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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


class Post(db.Model):
    """User's Posts on the blog"""

    __tablename__ = "posts"

    def __repr__(self):
        p = self
        return f"<post id = {p.id}, title = {p.title}, content = {p.content}, created_at ={p.created_at}, user_id = {p.user_id}>"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.Text, nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)

    author = db.relationship('User', backref='posts')

    tags = db.relationship('Tag',
                           secondary = 'post_tags',
                           backref = 'posts')

class Tag(db.Model):
    """Tags for a post"""

    __tablename__ = "tags"

    def __repr__(self):
        return f"<tag id = {self.id}, tag name = {self.name}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable = False, unique = True)

class PostTag(db.Model):
    """Relationship table between a post and a tag"""

    __tablename__ = "post_tags"

    post_id = db.Column (db.Integer, db.ForeignKey('posts.id'), primary_key = True)
    tag_id = db.Column (db.Integer, db.ForeignKey('tags.id'), primary_key = True)





# class Employee(db.Model):
#     """Employee."""

#     __tablename__ = "employees"

#     id = db.Column(db.Integer,
#                    primary_key=True,
#                    autoincrement=True)
#     name = db.Column(db.Text, nullable=False, unique=True)
#     state = db.Column(db.Text, nullable=False, default='CA')
#     dept_code = db.Column(
#         db.Text,
#         db.ForeignKey('departments.dept_code'))

#     dept = db.relationship('Department')

#     # direct navigation: emp -> employeeproject & back
#     assignments = db.relationship('EmployeeProject',
#                                   backref='employee')

#     # direct navigation: emp -> project & back
#     projects = db.relationship('Project',
#                                secondary='employees_projects',
#                                backref='employees')

#     def __repr__(self):
#         e = self
#         return f"<Employee {e.id} {e.name} {e.state}>"

# class Department(db.Model):
#     """Department. A department has many employees."""

#     __tablename__ = "departments"

#     dept_code = db.Column(db.Text, primary_key=True)
#     dept_name = db.Column(db.Text,
#                           nullable=False,
#                           unique=True)
#     phone = db.Column(db.Text)

#     employees = db.relationship('Employee')

#     def __repr__(self):
#         return f"<Department {self.dept_code} {self.dept_name}>"


# class Project(db.Model):
#     """Project. Employees can be assigned to this."""

#     __tablename__ = "projects"

#     proj_code = db.Column(db.Text, primary_key=True)
#     proj_name = db.Column(db.Text,
#                           nullable=False,
#                           unique=True)

#     # direct navigation: proj -> employeeproject & back
#     # only a sql alchemy python side construct, not in table, schema, database
#     assignments = db.relationship('EmployeeProject',
#                                   backref='project')

#     def __repr__(self):
#         return f"<Project {self.proj_code} {self.proj_name}>"


# class EmployeeProject(db.Model):
#     """Mapping of an employee to a project."""

#     __tablename__ = "employees_projects"

#     emp_id = db.Column(db.Integer,
#                        db.ForeignKey("employees.id"),
#                        primary_key=True)
#     proj_code = db.Column(db.Text,
#                           db.ForeignKey("projects.proj_code"),
#                           primary_key=True)
#     role = db.Column(db.Text)
