"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)
app.debug = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# For use in python shell without having to type app context continously
# first run app then...
# ctx = app.app_context()
# ctx.push()  # Push the context to make it current
# ctx.pop() #for cleanup before exiting

connect_db(app)
with app.app_context():
    # db.create_all()

    @app.route("/")
    def home_page():
        """Shows list of Users"""
        return redirect("/users")

    @app.route("/users")
    def users_page():

        all_users = User.query.order_by(User.last_name, User.first_name).all()

        return render_template("index.html", users=all_users)

    @app.route('/users/new', methods=["GET"])
    def users_new_form():
        """Show a form to create a new user"""

        return render_template('new.html')

    @app.route("/users/new", methods=["POST"])
    def users_new():
        """Handle form submission for creating a new user"""

        new_user = User(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            image_url=request.form['image_url'] or None)

        db.session.add(new_user)
        db.session.commit()

        return redirect("/users")

    @app.route("/users/<int:user_id>")
    def user_detail_page(user_id):
        """Show details of a user."""

        user = User.query.get_or_404(user_id)
        posts = user.posts
        return render_template("show.html", user=user, posts=posts)

    @app.route('/users/<int:user_id>/edit')
    def users_edit(user_id):
        """Show a form to edit an existing user"""

        user = User.query.get_or_404(user_id)
        return render_template('edit.html', user=user)

    @app.route('/users/<int:user_id>/edit', methods=["POST"])
    def users_update(user_id):
        """Handle form submission for updating an existing user"""

        user = User.query.get_or_404(user_id)
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['image_url']

        db.session.add(user)
        db.session.commit()

        return redirect("/users")

    @app.route('/users/<int:user_id>/delete', methods=["POST"])
    def users_destroy(user_id):
        """Handle form submission for deleting an existing user"""

        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

        return redirect("/users")

    # User's Post (blog) routes

    @app.route('/users/<int:user_id>/posts/new')
    def posts_new(user_id):
        user = User.query.get_or_404(user_id)

        return render_template('/posts/new.html', user = user)
    

    @app.route('/users/<int:user_id>/posts/new',  methods=["POST"])
    def posts_add(user_id):
        user = User.query.get_or_404(user_id)
        new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user_id=user.id)

        db.session.add(new_post)
        db.session.commit()
        flash(f"New Post '{new_post.title}' added.")
        # Need to update flash messaging...................

        return redirect(f"/users/{user_id}")


    @app.route('/posts/<int:post_id>')
    def posts_show(post_id):
        """Show a page with info on a specific post"""
        post = Post.query.get_or_404(post_id)
        return render_template('posts/show.html', post=post)

    @app.route('/posts/<int:post_id>/edit')
    def posts_edit(post_id):
        """Show a form for editing the title and content of a post"""
        post = Post.query.get_or_404(post_id)
        return render_template('posts/edit.html', post=post)
    
    @app.route('/posts/<int:post_id>/edit', methods=["POST"])
    def posts_update(post_id):
        """Handle form submission for updating an existing post"""
        post = Post.query.get_or_404(post_id)
        post.title = request.form['title']
        post.content= request.form['content']

        db.session.add(post)
        db.session.commit()
        # Need to update flash messaging...................
        flash(f"Post '{post.title}' edited.")

        return redirect(f"/users/{post.user_id}")
    
    @app.route('/posts/<int:post_id>/delete', methods=["POST"])
    def delete_post(post_id):
        """Handles form submission and deletes existing post from the User"""
        post = Post.query.get_or_404(post_id)

        db.session.delete(post)
        db.session.commit()
        # Need to update flash messaging...................
        flash(f"Post '{post.title}' deleted.")

        return redirect (f"/users/{post.user_id}")



