from functools import wraps

from flask import url_for, current_app, request, Response, Blueprint
from flask_restplus import Api
from bs4 import BeautifulSoup
from bs4.element import Comment


def add_basic_auth(blueprint: Blueprint, username, password, realm='api'):
    """
    Add HTTP Basic Auth to a blueprint.
    Note this is only for casual use!
    """

    @blueprint.before_request
    def basic_http_auth(*args, **kwargs):
        auth = request.authorization
        if auth is None or auth.password != password or auth.username != username:
            return Response('Please login', 401, {'WWW-Authenticate': f'Basic realm="{realm}"'})


def check_auth(username, password):
    """
    This function is called to check if a username /
    password combination is valid.
    """
    return username == current_app.config['DOC_USERNAME'] and password == current_app.config['DOC_PASSWORD']


def authenticate():
    """
    Sends a 401 response that enables basic auth
    """
    return Response('Not Authorized', 401, {'WWW-Authenticate': 'Basic realm="api"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


class PatchedApi(Api):

    @property
    def specs_url(self):
        """Monkey patch for HTTPS"""
        scheme = 'https' if self.is_prod() else 'http'
        return url_for(self.endpoint('specs'), _external=True, _scheme=scheme)

    @staticmethod
    def is_prod():
        return not current_app.config['TESTING']

    def _register_apidoc(self, app):
        app.view_functions['doc'] = requires_auth(app.view_functions['doc'])
        return super()._register_apidoc(app)

    def handle_error(self, e):
        if current_app.config['TESTING'] or current_app.config['APP_ENVIRONMENT'] == 'development':
            print(e)
        super().handle_error(e)

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = list(filter(tag_visible, texts))
    left_bound = 0
    right_bound = len(visible_texts)
    for i in range(len(visible_texts)):
        if len(visible_texts[i]) > 35:
            left_bound = i
            break

    for j in range(len(visible_texts)):
        if len(visible_texts[len(visible_texts) - j - 1]) > 50:
            right_bound = len(visible_texts) - j - 1
            break
    # print("##############")
    # print(left_bound)
    # print(right_bound)
    visible_texts = visible_texts[left_bound:right_bound]
    # print(list(visible_texts))
    return u" ".join(t.strip() for t in visible_texts)