from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

sample_page = Blueprint('sample_page', 'sample_page', template_folder='templates')
test_page = Blueprint('test_page', 'test_page', template_folder='templates')


@sample_page.route('/sample')
def get_sample():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)

@sample_page.route('/test')
def get_test():
    try:
        return render_template('test.html')
    except TemplateNotFound:
        abort(404)