# Keyword report generator
This application is a simple keyword report generator.
It leverages the `gensim` library for natural language processing
and keyword extraction.

## How it works
The application scans files in a `data` folder and derives the 10 (up to 10)
most important keywords within each document. Keywords are determined using
the TextRank algorithm which is a variation of the PageRank algorithm
developed by Google.

Keywords are determined on a per document basis with the highest weighted
words making up the first 10 etc. This ensures that important words for each
document are identified as opposed to just words which are important across
every document.

The keywords are lemmatised meaning that two words which share the same stem
are treated as the same word. For example `work` and `worked`.

Once up to 10 keywords have been determined per document, word stems are 
extracted and all documents are scanned for occurrences of words that are
derived from these stems.

Finally, a report is generated identifying which collection of words were present
in which document, counting sentence occurrences and listing by document, which
sentences the words occurred in.

## Dependencies
The application requires python 3.8 and pipenv. 

If you don't have don't already have pipenv as part of your
python environment, it can be installed as follows:

### MacOS
```
$ brew install pipenv
```
### Debian
```
$ sudo apt install pipenv
```
### Windows
```
$ pip install --user pipenv
```

## Installation
To install the dependencies, after cloning the repository, 
initialise the pipenv environment and then install dependent packages:

```
$ pipenv shell
$ pipenv install
```

## Usage
Input text files are detected in the `data` folder where files have
the extension `*.txt`.

The application can be run as follows:
```
$ pipenv run keyword_report
```

An output file named `summary.html` will be generated in the same folder 
which can be opened in any modern web-browser.

## Testing
Testing requires `pytest` and can be run with the following scripts:

- `pipenv run test` - to run the basic test suite
- `pipenv run snapshot-update` - to update the snapshot

Snapshots are used to test the final rendered output and must be updated on
a change to the render logic. This has been done with the `snapshottest`
library.