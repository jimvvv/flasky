from datatime import datatime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from .. import DB
from ..models import User

@main.route('/', methods=['GET', 'POST'])