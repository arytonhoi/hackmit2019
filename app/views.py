from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound
from bs4 import BeautifulSoup
import requests
from .utils import text_from_html
from counter_point.nlp.article import Article

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
    page = requests.get(article)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find('h1').get_text()
    article_text = text_from_html(requests.get(article).content)
    print("###########")
    print(soup.findAll(text=True))
    # print(article_text)

    positive_list = []
    neutral_list = []
    negative_list = []

    a = Article(article, title, article_text)
    print(a.news_source)
    a.print_topic_info()
    
    try:
        return render_template('results.html', url=article, article_trunc=('%.60s' % article), positive_list=positive_list, neutral_list=neutral_list, negative_list=negative_list)
    except TemplateNotFound:
        abort(404)