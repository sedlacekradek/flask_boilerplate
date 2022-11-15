from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User
from . import db

views = Blueprint("views", __name__)


### view functions ###
# @views.route("/")
# @views.route("/home")
# @login_required
# def home():
#     return render_template("home.html", user=current_user)