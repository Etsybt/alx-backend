#!/usr/bin/env python3
"""
6-app
"""
from typing import Dict, Optional
from flask import Flask, render_template, request, g
from flask_babel import Babel


class AppConfig:
    """Application configuration class."""

    DEBUG = True
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(AppConfig)
app.url_map.strict_slashes = False

babel = Babel(app)

user_data = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Optional[Dict]:
    """Fetch user by ID from request arguments.

    Returns:
        Optional[Dict]: User details if found, otherwise None.
    """
    user_id = request.args.get('login_as')
    if user_id:
        return user_data.get(int(user_id))
    return None


@app.before_request
def before_request_handler() -> None:
    """Set up user context before handling the request."""
    g.user = get_user()


@babel.localeselector
def select_locale() -> str:
    """Determine the best locale based on various inputs.

    Returns:
        str: The locale to use.
    """
    locale_from_url = request.args.get('locale')
    if locale_from_url in app.config['LANGUAGES']:
        return locale_from_url
    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user['locale']
    return request.accept_languages.best_match(
        app.config['LANGUAGES']) or app.config['BABEL_DEFAULT_LOCALE']


@app.route('/')
def home() -> str:
    """Render the homepage.

    Returns:
        str: Rendered HTML for the homepage.
    """
    return render_template("6-index.html")


if __name__ == "__main__":
    app.run()
