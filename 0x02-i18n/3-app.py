#!/usr/bin/env python3
"""
3-app
"""
from flask import Flask, render_template, request
from flask_babel import Babel, gettext
app = Flask(__name__)


class Config:
    """
    configs languages
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """
    func
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """
    default func
    """
    return render_template('3-index.html')


if __name__ == '__main__':
    app.run(debug=True)
