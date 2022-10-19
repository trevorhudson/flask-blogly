"""Blogly application."""
# from django.shortcuts import render
from flask import Flask, request, redirect, render_template
from models import db, connect_db, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

# create flask app


@app.get("/")
def show_homepg():
    return redirect("/users")


@app.get("/users")
def show_user_listings():

    users = User.query.all()
    return render_template("users_listing.html", users=users)
