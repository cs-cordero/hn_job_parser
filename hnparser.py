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

# Declare Constants Used
VERSION = '0.1'
BOILERPLATE = (
    'HackerNews \'Who is hiring?\' Parser\n'
    'Created by: Christopher Sabater Corder\n'
    'Version %s' % (VERSION)
)
VALID_MONTHS = {
    'JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE',
    'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER'
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


def pull_comments(hn_id, keywords):
    """
    This function will take a HackerNews item id and pull the HTML from it.
    It will then parse the HTML for top-level comments and extract the
    author and text body and store it into a dictionary to be output later.

    Inputs:     (String) HackerNews Item ID
                (List) Search Keywords
    Outputs:    (Dict) Tuples of Author-Body keyed by a unique counter 
    """

    # Scrape data from Hacker News website
    query = 'https://news.ycombinator.com/item?id=%s' % hn_id
    r = requests.get(query).text
    soup = BeautifulSoup(r, 'html.parser')
    comments = soup.find_all('tr', {'class': 'athing comtr '})

    relevant_comments = {}
    parser_id = 0
    for comment in soup.find_all('tr', {'class': 'athing comtr '}):
        # if not the top level comment, skip to next comment.
        if not comment.find('img', {'width': 0}):
            continue

        # extract relevant information
        try:
            author = comment.find('a', {'class': 'hnuser'}).get_text().strip()
            body = comment.find('span', {'class': 'c00'}).get_text().strip()
        except AttributeError:
            continue
        if body.endswith('reply'):
            body = body[:-5]

        # xando is a well-known user who parses the same thread for
        # a different service. His post is not a true job listing.
        if author == 'xando':
            continue

        # search string for keywords
        for keyword in keywords:
            if keyword.upper() in body.upper():
                relevant_comments[parser_id] = [author, body]
                parser_id += 1
                continue

    return relevant_comments


def parse_arguments(argv):
    """
    Function parses the user-provided arguments, if any.

    Inputs:     (List) Sys.Argv
    Outputs:    (List) Search Keywords
                (String) Month for Search in MMMM YYYY format.
                (String) Output filepath
    """
    keywords = ['junior', 'python']
    current_month = datetime.datetime.now().strftime('%B %Y')
    filepath = ('./hn_parser_%s.txt'
                % re.sub(r'\s+', r'_', current_month.lower()))

    args = ' '.join(argv[1:])
    for command in re.findall(r'--[\w\s]+', args):
        command = command.split()
        if command[0] == '--keywords':
            keywords = command[1:]
        elif command[0] == '--date':
            if command[1].upper() in VALID_MONTHS and len(command[2]) == 4:
                current_month = '%s %s' % (command[1].title(), command[2])
            else:
                raise Exception
        elif command[0] == '--filepath':
            if command[1].endswith('.txt'):
                filepath = command[1]
            else:
                filepath = command[1] + '.txt'

    return keywords, current_month, filepath


def main(argv):
    """
    Main driver of the script, calls other functions and produces the
    desired output.

    Inputs:     (List) Sys.argv
                Possible '--' commands are the following:
                --keywords (space-separated keywords)
                --date (Month for Search in MMMM YYYY format)
                --filepath
    Outputs:    (.txt) Outputs a text dump of the data pull, stored in the
                same folder as this program by default.
    """
    keywords, current_month, filepath = parse_arguments(argv)
    hn_id = search_HN(current_month)
    if hn_id is None:
        return False
    comments = pull_comments(hn_id, keywords)

    # write to document
    with open(filepath, 'w') as outfile:
        outfile.write(BOILERPLATE.encode('utf-8') + '\n')
        outfile.write('Month Searched: %s\n' % current_month)
        outfile.write('Keywords Used: %s\n\n' % ', '.join(keywords))
        for key in comments:
            outfile.write('>>>> %s: \n' % key)
            outfile.write(comments[key][0].encode('utf-8') + ' --- \n')
            outfile.write(comments[key][1].encode('utf-8') + '\n\n')

    print('File created at %s' % filepath)


if __name__ == '__main__':
    main(sys.argv)
