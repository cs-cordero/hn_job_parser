# Hacker News Job Parser

This Hacker News Job Parser tool pulls job listings from the latest month's Hacker News "Who is hiring" post.  The program accepts custom keyword searches and can also specify the Month Year to pull the job listings from.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

```
pip install requests
pip install beautifulsoup
```

### Usage
```
    python hnparser.py [optional-arguments]

    Optional Arguments:
    --keywords [space-delimited keywords]
    --date [Month Year in MMMM YYYY format]
    --filepath [your-filepath-here]
```

## To-Do
*   Deploy to pip for people to use!
*   Allow for keyword AND searching, i.e., 'junior' and 'python' together, not just separately.
*   Should I allow for the user to output to a different file instead of a .txt?
*   Clean output and make prettier?

## Authors

* **Christopher Sabater Cordero** - [cs-cordero](https://github.com/cs-cordero)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.


## Acknowledgments

* [Hacker News](https://news.ycombinator.com/)