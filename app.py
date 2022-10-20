"""Blogly application."""
# from django.shortcuts import render
from flask import Flask, request, redirect, render_template
from sqlalchemy import null
from models import db, connect_db, User, DEFAULT_IMAGE_URL


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

# Shows up even when calling tests.py
# print("***app.running")


@app.get("/")
def show_homepg():
    """redirects to the user list page"""
    return redirect("/users")


@app.get("/users")
def show_user_listings():
    """ renders page with user list from database """
    users = User.query.all()
    # TODO: ADD ORDER TO QUERY
    return render_template("users_listing.html", users=users)


@app.get("/users/new")
def show_add_user_form():
    """ shows form for adding new user to the database """
    return render_template("new_user_form.html")


@app.post("/users/new")
def add_new_user():
    """    Add a new user to the database """
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')

    # TODO: CHECK FOR NONE, TO TRIGGER DEFAULT
    img_url = request.form.get('img_url')

    if not img_url:
        img_url = DEFAULT_IMAGE_URL

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        img_url=img_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.get("/users/<int:user_id>")
def show_user_details(user_id):
    """Show detail page for a specific user"""
    user = User.query.get_or_404(user_id)

    return render_template("user_details.html", user=user)


@app.get("/users/<int:user_id>/edit")
def show_edit_user_pg(user_id):
    """shows form for editing user information"""

    user = User.query.get_or_404(user_id)

    return render_template("edit_user_form.html", user=user)


@app.post("/users/<int:user_id>/edit")
def process_edit_user_form(user_id):
    """updates user information with form input"""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    img_url = request.form.get('img_url')

    if not img_url:
        img_url = DEFAULT_IMAGE_URL

    user = User.query.get_or_404(user_id)

    user.first_name = first_name
    user.last_name = last_name
    user.img_url = img_url

    db.session.commit()

    return redirect("/users")


@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """permanently deletes user from the database"""
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
