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

def create_article(article_url,get_topics=True):
        page = requests.get(article_url)
        soup = BeautifulSoup(page.content, 'html.parser')

        search = ['h1', '.balancedHeadline','.pg-headline','.headLine','.headline','.title','.content__title']

        title = soup.find(search).get_text() if soup.find(search) else None
        # title = soup.find_all("h1", class_="balancedHeadLine pg-headline headLine headline title").get_text()
        if not title:
            title = None
        article_text = text_from_html(requests.get(article_url).content)

        return Article(article_url, title, article_text,get_topics=get_topics)

@sample_page.route('/results', methods=['POST'])
def get_results():
    article_url = request.form['article']
    # page = requests.get(article)
    # soup = BeautifulSoup(page.content, 'html.parser')
    # if soup.find('h1'):
    #     title = soup.find('h1').get_text()
    # else:
    #     title = ""
    # article_text = text_from_html(requests.get(article).content)
    # print("###########")
    # print(soup.findAll(text=True))
    # print(article_text)
    input_article = create_article(article_url)

    # liberal_urls = []
    # neutral_list = []
    # conservative_list = []

    # a = Article(article, title, article_text)
    # print(a.news_source)
    # a.print_topic_info()

    # result_urls = a.make_gsearch_query()
    # result_articles = []
    # for url in result_urls:
    #     temp_page = requests.get(url).content
    #     temp_soup = BeautifulSoup(temp_page, 'html.parser')
    #     if temp_soup.find('h1'):
    #         temp_title = temp_soup.find('h1').get_text()
    #     else:
    #         temp_title = ""
    #     result_articles.append(Article(url, temp_title, text_from_html(temp_page)))
    
    # print(result_articles)
    
    # for article in result_articles:
    #     if article.document_sentiment.score <= 40:
    #         negative_list.append(article)
    #     elif article.document_sentiment.score >= 60:
    #         positive_list.append(article)
    #     else:
    #         neutral_list.append(article)

    liberal_urls = input_article.get_liberal_articles()
    neutral_urls = input_article.get_neutral_articles()
    conservative_urls = input_article.get_conservative_articles()

    liberal_articles = []
    neutral_articles = []
    conservative_articles = []

    for liberal_url in liberal_urls:
        liberal_articles.append(create_article(liberal_url,get_topics=False))
    for neutral_url in neutral_urls:
        neutral_articles.append(create_article(neutral_url,get_topics=False))
    for conservative_url in conservative_urls:
        conservative_articles.append(create_article(conservative_url,get_topics=False))

    try:
        # return render_template('results.html', main_article=input_article, article_trunc=('%.40s' % a.url), 
        #                 positive_list=positive_list, neutral_list=neutral_list, negative_list=negative_list)
        return render_template('results.html', main_article=input_article, 
                    liberal_articles=liberal_articles, neutral_articles=neutral_articles, conservative_articles=conservative_articles)
    except TemplateNotFound:
        abort(404)