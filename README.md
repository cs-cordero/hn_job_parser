# Hacker News Job Parser

This Hacker News Job Parser CLI tool pulls job listings from the latest month's Hacker News "Who is Hiring" post.  [Here](https://news.ycombinator.com/item?id=14901313) is an example of such a post.

Instead of CTRL+F'ing through the entire thread with different key word searches, this tool can perform complex, google-like search queries against all top-level comments in the thread and return a CSV file with all relevant comments listed.  For example, if you're interested in all comments with mentions of 'Python' and 'Junior' (for you junior devs out there), you could pass into the CLI the terms "python and junior" and voila, it will find all comments with both search terms listed.  If you want to only find comments with the words "New York City", you could do so as well.

See below for usage descriptions.


### Prerequisites

This CLI uses BeautifulSoup, Pandas, and Requests. Other dependencies are provided in the `requirements.txt` file.  Clone this repository to your computer and then run the following command to have pip install everything for you.


```
pip install -r requirements.txt
```

### Usage
```
    python hn-job-parser/hn-job-parser.py [arguments]

    Optional Arguments:
        --search [space-delimited keywords]
        --date [Month Year in MMMM YYYY format]
        --output [your-filepath-here]

    Examples:
        python hn-job-parser/hn-job-parser.py --search python and junior
        python hn-job-parser/hn-job-parser.py --search python and "new york"
        python hn-job-parser/hn-job-parser.py --search python and ("new york" or NY or NYC)
        (if in bash:)
        python hn-job-parser/hn-job-parser.py --search python and \("new york" or NY or NYC\)
```

The `--search` argument provides the following features:
* Search Term Concatenators:  `AND`, `OR`, `NOT`
* Search Term Groupers:  `(` `)` -- note that depending on your CLI, you may need to escape these characters.  For example, in bash, you would use `\(` and `\)`.
* You can group multiple word 'terms' together with quotations "", e.g., "New York City"

## Authors

* **Christopher Sabater Cordero** - [cs-cordero](https://github.com/cs-cordero)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.


## Acknowledgments

* [Hacker News](https://news.ycombinator.com/)
