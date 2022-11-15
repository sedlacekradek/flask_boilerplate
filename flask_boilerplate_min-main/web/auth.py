from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


### auth functions ###
# @auth.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":


# @auth.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for("views.home"))