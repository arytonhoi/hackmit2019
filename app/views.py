from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound

sample_page = Blueprint('sample_page', 'sample_page', template_folder='templates')
home_page = Blueprint('home_page', 'home_page', template_folder='templates')
results_page = Blueprint('results_page', 'results_page', template_folder='templates')

@sample_page.route('/sample')
def get_sample():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)

@sample_page.route('/home')
def get_test():
    try:
        return render_template('home.html')
    except TemplateNotFound:
        abort(404)

@sample_page.route('/results', methods=['POST'])
def get_results():
    article = request.form['article']
    
    try:
        return render_template('results.html', article=article)
    except TemplateNotFound:
        abort(404)