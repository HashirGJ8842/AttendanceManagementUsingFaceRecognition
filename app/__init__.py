from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm, AdminRegister
import calendar
from flask_pymongo import PyMongo
import Employee as emp
from Employee import Employee

app = Flask(__name__)
app.config['SECRET_KEY'] = '8924989289289289'
