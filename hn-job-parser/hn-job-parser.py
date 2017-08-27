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
from bs4 import BeautifulSoup

import argparse
from collections import deque
from hackernews import HackerNews

# Declare Constants Used
VERSION = '0.3'
BOILERPLATE = (
    'HackerNews \'Who is Hiring?\' Parser\n'
    'Created by: Christopher Sabater Cordero\n'
    'Version %s' % (VERSION)
)
VALID_MONTHS = set([
    'january', 'february', 'march', 'april', 'may', 'june',
    'july', 'august', 'september', 'october', 'november', 'december'
])


def main(args):
    """ Entry point

    Inputs:     (List) Sys.argv
                Possible '--' commands are the following:
                --keywords (space-separated keywords)
                --date (Month for Search in MMMM YYYY format)
                --filepath
    Outputs:    (.txt) Outputs a text dump of the data pull, stored in the
                same folder as this program by default.
    """
    validated_args = validate_args(args)

    who_is_hiring_item_id = search_HN(validated_args['date'])
    if who_is_hiring_item_id is None:
        return False

    pull_comments(who_is_hiring_item_id, validated_args)


def validate_args(args):
    """ Validates the args passed into the command line tool

    Arguments:  argparse.NameSpace() object from argparse.parse_args()
    Returns:    a dict with the needed arguments, validated
    Throws:     Exception if invalid strings are provided
    """
    keywords = deque()
    query = deque()
    for arg in args.search:
        arg = arg.lower()
        if arg in ['and', 'or', 'not']:
            query.append(arg)
        keywords.append(arg)
    if not keywords:
        raise Exception('Invalid search given: {}'.format(' '.join(query)))


    date = ' '.join(args.date)
    year = int(args.date[1])
    latest_valid_year = datetime.datetime.now().year
    if (args.date[0].lower() not in VALID_MONTHS or
        (year < 2010 or year > latest_valid_year)):
        raise Exception('Invalid date given: {}'.format(date))

    
    output = './out.csv' if args.output == 'default_loc' else args.output

    return {
        'keywords': keywords,
        'query': query,
        'date': date,
        'output': output
    }



def search_HN(current_month):
    """
    This function will send to HackerNews a search request for "Who is Hiring
    (current_month current_year)".  It will then search through the search
    results and find the correct HackerNews item page and return its item ID.

    Inputs:     (String) Month for Search in MMMM YYYY format.
    Outputs:    (String) Hacker News Item ID
    """

    # Set up the query
    query = 'http://hn.algolia.com/api/v1/search?query=Whois+Hiring+(' \
            + current_month \
            + ')&tags=story'
    query = re.sub(r'\s+', r'+', query)

    # Send query and search for the item ID
    print('Searching HackerNews for Who is Hiring pages for %s'
          % (current_month))
    r = requests.get(query).text
    j = json.loads(r)

    # Search through the hits for the correct title
    for hit in j['hits']:
        if hit['title'] == 'Ask HN: Who is hiring? (' + current_month + ')':
            print('Found item ID!: %s' % (hit['objectID']))
            return hit['objectID']

    # Return None if unable to find the correct title anywhere.
    print('Unable to Locate for %s' % (current_month))
    return None


def pull_comments(who_is_hiring_item_id, search_args):
    """
    This function will take a HackerNews item id and pull the HTML from it.
    It will then parse the HTML for top-level comments and extract the
    author and text body and store it into a dictionary to be output later.

    Inputs:     (String) HackerNews Item ID
                (List) Search Keywords
    Outputs:    (Dict) Tuples of Author-Body keyed by a unique counter 
    """
    url_to_hn_page = 'https://news.ycombinator.com/item?id=%s' % who_is_hiring_item_id
    response = requests.get(url_to_hn_page)
    if response.status_code != 200:
        raise Exception('Received status code from HN: ', response.status_code)
    
    html = response.text
    with open('response.html', 'w') as f:
        f.write(html)


if __name__ == '__main__':
    """
    Parses the CLI arguments and runs the main() function

    Args:
        --search : A list of space-delimited keywords that use AND/OR/NOT and
                   parentheses to group the search terms.
        --output : Sets the output path
        --date   : MMM YYYY format of the month to search for jobs
    """
    parser = argparse.ArgumentParser(
        description = 'Scans HN Who is Hiring Thread'
    )
    parser.add_argument('-s', '--search',
            action='store',
            default=['python'],
            nargs='+',
            type=str,
            help='search string of space-delimited keywords. may use AND OR and NOT',
            dest='search'
    )
    parser.add_argument('-o', '--output',
            action='store',
            default='default_loc',
            type=str,
            help='filepath to where the output should go',
            dest='output'
    )
    parser.add_argument('-d', '--date',
            action='store',
            default=datetime.datetime.now().strftime('%B %Y').split(' '),
            nargs=2,
            type=str,
            help='MMM YYYY format of month to search for jobs',
            dest='date'
    )

    main(parser.parse_args())
