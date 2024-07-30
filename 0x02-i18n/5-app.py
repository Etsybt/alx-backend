#!/usr/bin/env python3
"""
5-app
"""
from typing import Dict, Optional
from flask import Flask, render_template, request, g
from flask_babel import Babel


class AppConfig:
    """Configuration for the Flask application."""

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


def fetch_user() -> Optional[Dict]:
    """Fetch a user based on the provided user ID
    """
    user_id = request.args.get('login_as')
    if user_id:
        return user_data.get(int(user_id))
    return None


@app.before_request
def setup_request() -> None:
    """Set up the user context before handling the request."""
    g.user = fetch_user()


@babel.localeselector
def select_locale() -> str:
    """
    Determine the best locale for the user based on the request
    """
    requested_locale = request.args.get('locale')
    if requested_locale in app.config['LANGUAGES']:
        return requested_locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def home() -> str:
    """
    Render the homepage.
    """
    return render_template("5-index.html")


if __name__ == "__main__":
    app.run()
