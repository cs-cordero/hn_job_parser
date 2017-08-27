
import datetime
from collections import deque


VALID_MONTHS = set([
    'january', 'february', 'march', 'april', 'may', 'june',
    'july', 'august', 'september', 'october', 'november', 'december'
])

def validate_args(args):
    """
    Validates the args passed into the command line tool

    Args:
        argparse.NameSpace() object from argparse.parse_args()
    Returns:
        A dict with the needed arguments, validated
    Throws:
        Exception if invalid strings are provided
    """
    keyword_order, keywords, cleaned_query = validate_search_terms(args.search)
    date = validate_date(args.date)
    output = validate_output(args.output)


    return {
        'keywords': keywords,
        'keyword_order': keyword_order,
        'query': cleaned_query,
        'date': date,
        'output': output
    }

def validate_search_terms(terms):
    """
    Parses the search terms character by character

    Args:
        A list of the search terms
    Returns:
        A tuple of all keywords in order
        A deduped set of all keywords
        A string representing a cleaned version of the search string
    Throws:
        Error if there are unbalanced parentheses
        Error if there are no valid keywords
    """
    search_terms = deque(map(lambda word: word.lower(), terms))
    parens_balancer = 0

    keywords = []
    cleaned_query = deque()

    while search_terms:
        search_term_to_parse = search_terms.popleft()
        keyword_holder = ''

        if search_term_to_parse in ('and', 'or', 'not'):
            if last_added_term_is_concatenation and not \
               (search_term_to_parse == 'not' and cleaned_query[-1] == 'and'):
                cleaned_query.pop()
            cleaned_query.append(search_term_to_parse)
            continue

        for char in search_term_to_parse:
            if char == '(':
                cleaned_query.append('(')
                parens_balancer += 1

            elif char == ')':
                if parens_balancer <= 0:
                    raise Exception("Found an extra ) without a ( to begin a"
                                    "grouping")

                parens_balancer -= 1
                if keyword_holder:
                    cleaned_query.append('{}')
                    keywords.append(keyword_holder)
                    keyword_holder = ''

                elif last_added_term_is_concatenation(cleaned_query):
                    cleaned_query.pop()

                cleaned_query.append(')')

            else:
                keyword_holder += char
        else:
            if keyword_holder:
                # if the word follows a ), append the implicit 'or'
                if len(cleaned_query) > 0 and cleaned_query[-1] == ')':
                    cleaned_query.append('or')

                # append the word
                cleaned_query.append('{}')

                # append an implicit "or" to follow the word, unless it is the
                # last term in the searchs tring
                if search_terms:
                    cleaned_query.append('or')
                keywords.append(keyword_holder)

    if parens_balancer > 0:
        raise Exception("Search query has an unbalanced parenthesis. Missing"
                        "one or more )'s to end the group.")

    if not keywords:
        raise Exception('Invalid search. No keywords found.')
    
    return tuple(keywords), set(keywords), ' '.join(cleaned_query)

def last_added_term_is_concatenation(query_list):
    """
    Takes the under-construction query string and determines whether the
    last added element is "and", "or", or "not"
    """
    if len(query_list) <= 0:
        return False
    last_query_element = query_list[-1].lower()
    return last_query_element in ('and', 'or', 'not')

def validate_date(date):
    """
    Takes the date provided in the CLI and makes sure it is a correct date

    Args:
        date : as given from argparser
    Returns:
        date : concatenated into a string, after validation
    """
    month, year = date[0].lower(), int(date[1])
    date = ' '.join(date)
    latest_valid_year = datetime.datetime.now().year
    if (month not in VALID_MONTHS or
        (year < 2010 or year > latest_valid_year)):
        raise Exception('Invalid date given: {}'.format(date))
    return date

def validate_output(output_path):
    """
    Converts 'default_loc' to './out.csv' and makes sure any passed in argument
    has a .csv file extension
    """
    if output_path == 'default_loc' or not output_path:
        output_path = './out.csv'

    if output_path[-4:] != '.csv':
        output_path += '.csv'

    return output_path
