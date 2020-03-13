"""
Yelp Fusion API code sample.
This program demonstrates the capability of the Yelp Fusion API
by using the Search API to query for businesses by a search term and location,
and the Business API to query additional information about the top result
from the search query.
Please refer to http://www.yelp.com/developers/v3/documentation for the API
documentation.
This program requires the Python requests library, which you can install via:
`pip install -r requirements.txt`.
Sample usage of the program:
`python sample.py --term="bars" --location="San Francisco, CA"`
"""
from __future__ import print_function

import argparse
from flask import *
import json
import pprint
import requests
import sys
import urllib

# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode

app = Flask(__name__)

# Yelp Fusion no longer uses OAuth as of December 7, 2017.
# You no longer need to provide Client ID to fetch Data
# It now uses private keys to authenticate requests (API Key)
# You can find it on
# https://www.yelp.com/developers/v3/manage_app
API_KEY= '7wb8rb94s7h-bl963f5jPrTn7kDfLjlFChxHi47pXgAFKeh0pY2LgK1XKMJR4SjoFZ-jf611wc03EL4sacQNg15WjtuAlo42wElVouniKMIzSZhIAwYuPsCrmXRPXnYx'


# API constants, you shouldn't have to change these.
API_HOST = ' https://cors-anywhere.herokuapp.com/https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.


# Defaults for our simple example.
DEFAULT_TERM = 'lunch'
DEFAULT_LOCATION = 'Houston, Texas'
SEARCH_LIMIT = 20

@app.route('/')
def hello_world():
    return render_template('index.html', name=None)

def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()

@app.route('/search/<term>/<location>/<search_limit>')
def search(term, location, search_limit):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': search_limit
    }
    return request(API_HOST, SEARCH_PATH, API_KEY, url_params=url_params)


@app.route('/get_business/<business_id>')
def get_business(business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, API_KEY)


# def query_api(term, location):
#     """Queries the API by the input values from the user.
#     Args:
#         term (str): The search term to query.
#         location (str): The location of the business to query.
#     """
#     response = search(API_KEY, term, location)

#     businesses = response.get('businesses')

#     if not businesses:
#         print(u'No businesses for {0} in {1} found.'.format(term, location))
#         return

#     business_id = businesses[0]['id']

#     print(u'{0} businesses found, querying business info ' \
#         'for the top result "{1}" ...'.format(
#             len(businesses), business_id))
#     response = get_business(API_KEY, business_id)

#     print(u'Result for business "{0}" found:'.format(business_id))
#     pprint.pprint(response, indent=2)

# query_api(DEFAULT_TERM, DEFAULT_LOCATION)

# def main():
#     parser = argparse.ArgumentParser()

#     parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
#                         type=str, help='Search term (default: %(default)s)')
#     parser.add_argument('-l', '--location', dest='location',
#                         default=DEFAULT_LOCATION, type=str,
#                         help='Search location (default: %(default)s)')

#     input_values = parser.parse_args()

#     try:
#         query_api(input_values.term, input_values.location)
#     except HTTPError as error:
#         sys.exit(
#             'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
#                 error.code,
#                 error.url,
#                 error.read(),
#             )
#         )
        
