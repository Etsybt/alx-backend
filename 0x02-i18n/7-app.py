#!/usr/bin/env python3
"""
Task 7
"""
from typing import Dict, Optional
from flask import Flask, render_template, request, g
from flask_babel import Babel
import pytz


class AppConfig:
    """Application configuration settings."""

    DEBUG = True
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


# Initialize the Flask application and load configuration
app = Flask(__name__)
app.config.from_object(AppConfig)
app.url_map.strict_slashes = False

# Initialize Flask-Babel
babel = Babel(app)

# User data
user_data = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Optional[Dict]:
    """Retrieve user details by user ID from request arguments.

    Returns:
        Optional[Dict]: User information if available, otherwise None.
    """
    user_id = request.args.get('login_as')
    if user_id:
        return user_data.get(int(user_id))
    return None


@app.before_request
def before_request_handler() -> None:
    """Set up the user context before processing the request."""
    g.user = get_user()


@babel.localeselector
def select_locale() -> str:
    """Determine the best locale for the current user.

    Returns:
        str: The selected locale.
    """
    # URL parameter for locale
    locale_from_url = request.args.get('locale')
    if locale_from_url in app.config['LANGUAGES']:
        return locale_from_url

    # User setting for locale
    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user['locale']

    # Accept-Language header
    return request.accept_languages.best_match(
        app.config['LANGUAGES']) or app.config['BABEL_DEFAULT_LOCALE']


@babel.timezoneselector
def select_timezone() -> str:
    """Determine the best timezone for the current user.

    Returns:
        str: The selected timezone.
    """
    # URL parameter for timezone
    timezone_from_url = request.args.get('timezone', '').strip()
    if timezone_from_url:
        try:
            return pytz.timezone(timezone_from_url).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    # User setting for timezone
    if g.user and g.user.get('timezone'):
        try:
            return pytz.timezone(g.user['timezone']).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    # Default timezone
    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def home() -> str:
    """Render the homepage.

    Returns:
        str: Rendered HTML content.
    """
    return render_template("7-index.html")


if __name__ == "__main__":
    app.run()
