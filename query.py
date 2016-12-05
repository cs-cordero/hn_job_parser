#!/usr/bin/python3

"""
This script will query the ycombinator Who is Hiring page for search results
based on given keywords that the user can provide.  The script also has some
default keyword searches.
"""

import sys
import requests
import json
import datetime
import re
from bs4 import BeautifulSoup as bs

def search_HN():
    """
    This function will send to HackerNews a search request for "Who is Hiring
    (current_month current_year)".  It will then search through the search
    results and find the correct HackerNews item page and return its item ID.
    """

    # Set up the query
    current_month = datetime.datetime.now().strftime('%B %Y')
    query = 'http://hn.algolia.com/api/v1/search?query=Whois+Hiring+(' \
            + current_month \
            + ')&tags=story'
    query = re.sub(r'\s+', r'+', query)

    # Send query and search for the item ID
    print('Searching HackerNews for Who is Hiring pages for {}'
          .format(current_month))
    r = requests.get(query).text
    j = json.loads(r)

    # Search through the hits for the correct title
    for hit in j['hits']:
        if hit['title'] == 'Ask HN: Who is hiring? (' + current_month + ')':
            print('Found item ID!: {}'.format(hit['objectID']))
            return hit['objectID']

    # Return None if unable to find the correct title anywhere.
    print('Unable to Locate for {}'.format(current_month))
    return None

def pull_comments(hn_id):
    query = 'https://news.ycombinator.com/item?id=%s' % hn_id
    r = requests.get(query).text
    soup = BeautifulSoup(r, 'html.parser')

def main():
    # hn_id = search_HN()
    hn_id = '13080280'
    if hn_id is None: return False
    pull_comments(hn_id)

if __name__ == '__main__':
    main()

"""
Hacker News Search API
http://hn.algolia.com/api/v1/search?query=(QUERY GOES HERE)&tags=story
Returns a JSON object that we can load to find the ID.
JSON object has a key called "hits" that we can iterate over.
key --> 'title'  gets us the story title.
key --> 'objectID'  gets us the item number.
"""