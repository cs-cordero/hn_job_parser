
import pandas as pd
from bs4 import BeautifulSoup, NavigableString

def get_top_level_comments(html):
    """
    Gets the top level comments from a HackerNews thread.

    Assumes that all comments have two classes: 'athing' and 'comtr'
    Assumes that top level comments are distinguished by having an s.gif img
    with a width of 0

    Args:
        html : html text from a request.get call
    Returns:
        A Pandas DataFrame of the top level comments
    """
    soup = BeautifulSoup(html, 'html.parser')
    all_comments = soup.select('tr.athing.comtr')
    top_comments = filter(lambda x: x.find('img')['width'] == '0', all_comments)
    return pd.DataFrame([extract_data(comment) for comment in top_comments])

def extract_data(hn_comment):
    """
    Gets the data from an HN comment

    Args:
        hn_comment : an html tag containing a hn comment parsed by BeautifulSoup

    Returns:
        A dict with all the pertinent information
    """
    full_comment = list(hn_comment.find(class_='comment').span.children)

    user = hn_comment.find(class_='hnuser').text
    body = full_comment[-1].text
    title = ''.join(element.text
                    if not isinstance(element, NavigableString)
                    else element
                    for element in full_comment[:-1])

    body = body.replace('\n', ' ').strip()
    title = title.replace('\n', ' ').strip()

    return { 'user': user, 'title': title, 'body': body }
