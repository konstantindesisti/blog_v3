from bs4 import BeautifulSoup
import hashlib
import requests
from pathlib import Path


def strip_html(html_comment):
    soup = BeautifulSoup(html_comment, 'html.parser')
    text = soup.get_text()
    return text


def gravatar_url(email, size=100, default='retro', rating='g', use_ssl=True):
    """Generate a Gravatar URL based on the email provided.

    Args:
        email (str): The user's email address.
        size (int): Size of the Gravatar image (default 100px).
        default (str): Default image type if no Gravatar is found (e.g., 'retro', 'monsterid', '404').
        rating (str): Maximum rating (g, pg, r, x) allowed for the Gravatar.
        use_ssl (bool): Use SSL for the URL (https is recommended).

    Returns:
        str: The URL to the Gravatar image.
    """

    # Create an MD5 hash of the email, which is required by Gravatar.
    email_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()

    # Construct the base URL using https or http.
    protocol = 'https' if use_ssl else 'http'
    url = f'{protocol}://www.gravatar.com/avatar/{email_hash}?s={size}&d={default}&r={rating}'
    return url

