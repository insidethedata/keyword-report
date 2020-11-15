from typing import List, Dict, Set
from gensim.summarization import keywords
from gensim.summarization.textcleaner import clean_text_by_word, clean_text_by_sentences, tokenize_by_word
from gensim.summarization.syntactic_unit import SyntacticUnit
from html5print import HTMLBeautifier

import glob
import os

#


def extract_file(file_name: str = "") -> str:
    """
    Extract file data

    Parameters
    ----------
    file_name: str
        File to import

    Returns
    -------
    result: str
        Content of the file
    """

    if len(file_name) < 1:
        raise ValueError("Empty filename")

    try:
        with open(os.path.join(os.getcwd(), file_name), 'r',
                  encoding='utf-8') as f:
            file_data: str = f.read()

        return file_data

    except:
        raise FileNotFoundError(f"Error reading file {file_name}")


def import_folder(folder_name: str = "",
                  file_mask: str = "*.txt") -> Dict[str, str]:
    """
    Extract file data

    Parameters
    ----------
    folder_name: str
        Folder to import

    Returns
    -------
    result: Dict[str,str]
        Dictionary containing keys relating to files in the folder
        and values set to content of the files
    """

    if len(folder_name) < 1:
        raise ValueError("Empty folder_name")

    output: Dict[str, str] = {}

    for filename in glob.glob(os.path.join(folder_name, file_mask)):
        output[filename] = extract_file(filename)

    return output


def get_keywords(doc_dict: Dict[str, str], words: int = 10) -> Set[str]:
    """
    Extracts keywords from document dictionary

    Parameters
    ----------
    doc_dict: Dict[str,str]
        Dictionary of text documents
    words: int
        Number of keywords to extract per document
        (default 10)
    
    Returns
    -------
    result: Set[str]
        Set containing lists of keywords
    """

    if len(doc_dict) < 1:
        raise ValueError("No documents to scan")

    keywords_set: Set(str) = set()

    for v in doc_dict.values():
        keywords_set.update(
            set(keywords(v, words=words, lemmatize=True, split=True)))

    # Take only the last element where there are spaces in the items
    keywords_set = set([x.split(" ")[-1:][0] for x in keywords_set])

    return keywords_set


def get_stems(doc_dict: Dict[str, str],
              keywords_set: Set[str]) -> Dict[str, Set[str]]:
    """
    Generates a list of stems with associated words

    Parameters
    ----------
    doc_dict: Dict[str,str]
        Dictionary of text documents
    keywords_set: Set[str]
        Set of keywords to generate stems dict for
    
    Returns
    -------
    result: Dict[str,Set[str]
        Dictionary containing lists of stems and their
        associated words
    """

    if len(doc_dict) < 1:
        raise ValueError("No documents to scan")

    output: Dict[str, Set[str]] = {}

    for v in doc_dict.values():
        tokens: Dict = clean_text_by_word(v)
        filtered_tokens: List[str] = [
            k for k in tokens.keys() if k in keywords_set
        ]
        stems: Set[str] = set()
        for word in filtered_tokens:
            stems.add(tokens[word].token)

        for stem in stems:

            word_list = set()
            for t in tokens.keys():
                if tokens[t].token == stem:
                    word_list.add(tokens[t].text)

            if stem not in output.keys():
                output[stem] = word_list
            else:
                output[stem].update(word_list)

    return output


def sets_to_lists(input_object: Dict):
    """
    Converts sets to lists from a dictionary
    """
    for attrib in input_object.keys():
        if isinstance(input_object[attrib], set):
            input_object[attrib] = list(input_object[attrib])

    return input_object


def build_output(doc_dict: Dict[str, str],
                 stems: Dict[str, Set[str]]) -> List[Dict]:
    """
    Builds output list of word report objects

    Parameters
    ----------
    doc_dict: Dict[str, str]
        Documents to scan
    stems: Dict[str, Set[str]]
        Dictionary of stems to scan for

    Returns
    -------
    result: List[Dict]
        Output data object for report generation
    """

    output: List[Dict] = []

    # Build extracted sentences
    sentences: Dict[str, List[SyntacticUnit]] = {}
    for doc in doc_dict.keys():
        sentences[doc] = clean_text_by_sentences(doc_dict[doc])

    for stem in stems.keys():
        entry: Dict = {}
        entry["stem"] = stem
        entry["sentence_count"] = 0
        entry["words"] = stems[stem]
        entry["sentences"] = {}
        entry["documents"] = set()

        for doc in doc_dict.keys():
            for sentence in sentences[doc]:
                if stem in sentence.token.split(" "):
                    entry["sentence_count"] += 1
                    if doc not in entry["sentences"].keys():
                        entry["sentences"][doc] = []
                    entry["sentences"][doc].append(sentence.text)
                    entry["documents"].add(doc)

        entry = sets_to_lists(entry)

        output.append(entry)

    return output


def highlight_keywords(sentence: str, keywords_list: List[str]) -> str:
    """
    Generates a sentence block with keywords highlighted

    Parameters
    ----------
    sentence: str
        Input string to highlight
    keyword_list: List[str]
        List contraining keywords to highlight

    Returns
    -------
    result: str
        Output html string
    """

    words = sentence.split(" ")
    for i in range(len(words)):
        if any(item in keywords_list for item in tokenize_by_word(words[i])):
            words[i] = f'<span class="highlight">{words[i]}</span>'

    output_str: str = '<p class="sentence">' + " ".join(words) + "</p>"
    return output_str


def generate_table(output_object: List, doc_list: List[str]) -> str:
    """
    Generates an html table from a report object
    Parameters
    ----------
    output_object: List
        Data object to generate report from
    doc_list: List[str]
        List of documents that were scanned
        
    Returns
    -------
    result: str
        Output html string
    """

    doc_list = sorted(doc_list)

    header: str = """
    <html>
        <head>
        <link rel="stylesheet" href="styling.css">
    </head>
    <body>
        <h1>Keyword extraction</h1>
        <h2>Documents scanned:</h2>
        <ol>
    """

    doc_list_str: str = ""
    for item in doc_list:
        doc_list_str += f'<li><a href="{item}">{item}</a></li>'

    table_header: str = """
    </ol>
    <h2>Keyword list</h2>
    <table class="data-table">
        <tr>
            <th>Word stem (Words)</th>
            <th>Total sentence occurances</th>
            <th>Documents</th>
            <th>Sentences containing the words</th>
        </tr>
    """

    table_items: List[str] = []

    for entry in output_object:
        word_list: str = ", ".join(entry["words"])
        entry_doc_list: str = '<ul class="doclist">' + "\n".join(
            map(lambda x: f"<li>{x}</li>", sorted(
                entry["documents"]))) + "</ul>"

        sentence_map_keys = sorted(entry["sentences"].keys())

        sentence_list: str = ""
        for k in sentence_map_keys:
            sentence_list += f"<h3>{k}</h3>\n" + "\n".join(
                map(lambda x: highlight_keywords(x, entry["words"]),
                    entry["sentences"][k]))

        # sentence_list: str = "\n".join(entry["sentences"])
        entry_output: str = f"""
        <tr>
            <td><span class = "highlight">{entry["stem"]}</span> ({word_list})</td>
            <td>{entry["sentence_count"]}</td>
            <td>{entry_doc_list}</td>
            <td>{sentence_list}</td>
        </tr>
        """
        table_items.append(entry_output)

    footer: str = """
    </table>
    </body>
    """

    output_str = header + doc_list_str + table_header + "\n".join(
        table_items) + footer

    return output_str


def main():

    # Import data and extract key information
    doc_dict: Dict[str, str] = import_folder('data', '*.txt')
    keywords_set: Set(str) = get_keywords(doc_dict)
    stems: Dict[str, Set[str]] = get_stems(doc_dict, keywords_set)

    # Generate report object and sort by occurances
    output = build_output(doc_dict, stems)
    output = sorted(output, key=lambda x: x["sentence_count"], reverse=True)

    # Generate report
    output_html = generate_table(output, sorted(doc_dict.keys()))

    # Reformat HTML for pretty printing
    output_html = HTMLBeautifier.beautify(output_html, indent=2)

    # Save report
    with open("summary.html", "w+", encoding='utf-8') as f:
        f.write(output_html)


if __name__ == "__main__":
    main()