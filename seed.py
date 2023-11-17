"""Seed file to make sample data for blogly db."""

from models import User, Post, db
from app import app
from datetime import datetime

# Create all tables
with app.app_context():
    db.drop_all()
    db.create_all()

    # If table isn't empty, empty it
    User.query.delete()

    # Add pets
    Alan = User(first_name='Alan', last_name='Aida',
                image_url="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=1200&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fHByb2ZpbGUlMjBpbWFnZXN8ZW58MHx8MHx8fDA%3D")
    Joel = User(first_name='Joel', last_name='Burton',
                image_url="https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=1200&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8cHJvZmlsZSUyMGltYWdlc3xlbnwwfHwwfHx8MA%3D%3D")
    Jane = User(first_name='Jane', last_name='Smith',
                image_url="https://images.unsplash.com/photo-1502823403499-6ccfcf4fb453?w=1200&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8cHJvZmlsZSUyMGltYWdlc3xlbnwwfHwwfHx8MA%3D%3D")

    # Add new objects to session, so they'll persist
    db.session.add(Alan)
    db.session.add(Joel)
    db.session.add(Jane)

    # Commit--otherwise, this never gets saved!
    db.session.commit()

    # Fetch all users
    all_users = User.query.all()

    # Clear existing data from the posts table
    Post.query.delete()

    # Loop through each user and create a post
    for user in all_users:
        post1 = Post(title=f"First Post by {user.first_name}",
                     content=f"This is a post by {user.full_name()}.",
                     created_at=datetime.now(),
                     user_id=user.id)
        post2 = Post(title=f"Second Post by {user.first_name}",
                     content=f"This is the second post by {user.full_name()}.",
                     user_id=user.id)
        post3 = Post(title=f"Third Post by {user.first_name}",
                     content=f"This is the third post by {user.full_name()}.",
                     user_id=user.id)
        # Add the post to the session in each loop for each user
        db.session.add_all([post1, post2, post3])

    # Commit to save all the posts
    db.session.commit()
