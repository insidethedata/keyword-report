import pytest
import keyword_report
from unittest.mock import patch, mock_open


def test_extract_file_empty_string():
    with pytest.raises(ValueError):
        keyword_report.extract_file("")


@patch("builtins.open", new_callable=mock_open, read_data="data")
def test_extract_file_read(mock_open):
    assert keyword_report.extract_file("test") == "data"


@patch("keyword_report.glob")
@patch("keyword_report.extract_file")
def test_import_folder_response(mock_extract_file, mock_glob):
    mock_glob.glob.return_value = ["testfile"]
    mock_extract_file.return_value = "text"
    assert keyword_report.import_folder('test', "*.txt") == {
        "testfile": "text"
    }


@patch("keyword_report.keywords")
def test_get_keywords(mock_keywords):
    doc_dict = {"doc": "this is a test"}
    mock_keywords.return_value = ["this", "is", "a test"]
    assert keyword_report.get_keywords(doc_dict, 10) == {"this", "is", "test"}


def test_get_stems():
    doc_dict = {"doc": "this is a test about testing functions"}
    assert keyword_report.get_stems(doc_dict, ["functions", "test"]) == {
        'test': {'testing', 'test'},
        'function': {'functions'}
    }


def test_sets_to_lists():
    test_object = {"test": {"test", "test2", "test3"}, "testing": {1, 2, 3}}
    response = keyword_report.sets_to_lists(test_object)
    assert isinstance(response, dict)
    assert "test" in response.keys()
    assert sorted(response["test"]) == ["test", "test2", "test3"]
    assert "testing" in response.keys()
    assert sorted(response["testing"]) == [1, 2, 3]


def test_build_output():
    doc_dict = {
        "doc":
        "this is a test about testing functions. This is a second sentence about functionality"
    }
    stems = {"test": {"test"}, "function": {"functions"}}
    assert keyword_report.build_output(doc_dict, stems) == [{
        'stem':
        'test',
        'sentence_count':
        1,
        'words': ['test'],
        'sentences': {
            'doc': ['this is a test about testing functions.']
        },
        'documents': ['doc']
    }, {
        'stem':
        'function',
        'sentence_count':
        2,
        'words': ['functions'],
        'sentences': {
            'doc': [
                'this is a test about testing functions.',
                'This is a second sentence about functionality'
            ]
        },
        'documents': ['doc']
    }]


def test_highlight_keywords():
    sentence = "This is a sentence for testing"
    keywords_list = ['sentence', 'testing']
    assert keyword_report.highlight_keywords(
        sentence, keywords_list
    ) == '<p class="sentence">This is a <span class="highlight">sentence</span> for <span class="highlight">testing</span></p>'


def test_generate_table(snapshot):
    output_object = [{
        'stem': 'test',
        'sentence_count': 1,
        'words': ['test'],
        'sentences': {
            'doc': ['this is a test about testing functions.']
        },
        'documents': ['doc']
    }]
    snapshot_restponse = keyword_report.generate_table(output_object, ['doc'])
    snapshot.assert_match(snapshot_restponse)