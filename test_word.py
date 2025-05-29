import pytest
from datetime import date
from word import Word

def test_word_init_str():
    word = Word("test")
    assert word.word == "test"
    assert word.added == date.today()
    assert word.learned is None

def test_word_init_dict():
    word_dict = {"word": "test", "added": "2023-10-01", "learned": "2023-10-02"}
    word_from_dict = Word(word_dict)
    assert word_from_dict.word == "test"
    assert word_from_dict.added.isoformat() == "2023-10-01"
    assert word_from_dict.learned.isoformat() == "2023-10-02"

def test_word_init_error():
    with pytest.raises(ValueError):
        Word("")
    with pytest.raises(TypeError):
        Word()

def test_init_from_dict_min():
    word_dict = {"something": "test"}
    word = Word(word_dict)
    assert word.word == "test"
    assert word.added == date.today()
    assert word.learned is None

def test_init_from_dict_bad():
    word_dict = {"something": "test", "added": "1111", "learned": "1111"}
    word = Word(word_dict)
    assert word.word == "test"
    assert word.added == date.today()
    assert word.learned == date.today()

def test_word_str():
    word = Word("test")
    assert str(word) == "test"

def test_word_dictionary():
    word = Word("test", date(2023, 10, 1), date(2023, 10, 2))
    expected_dict = {
        "word": "test",
        "added": "2023-10-01",
        "learned": "2023-10-02"
    }
    assert word.dictionary() == expected_dict

def test_learn():
    word = Word("test")
    assert word.learned is None
    assert word.is_known == False
    word.learn()
    assert word.learned == date.today()
    assert word.is_known == True

def test_forget():
    word = Word("test", date(2023, 10, 1), date(2023, 10, 2))
    assert word.is_known == True
    word.forget()
    assert word.learned is None
    assert word.added == date.today()
    assert word.is_known == False

def test_learning_period():
    word = Word("test", date(2023, 10, 1), date(2023, 10, 1))
    assert word.learning_period == "0 days"
    word = Word("test", date(2023, 10, 1), date(2023, 10, 2))
    assert word.learning_period == "1 day"
    word = Word("test", date(2023, 10, 1), date(2023, 12, 29))
    assert word.learning_period == "89 days"
    word = Word("test", date(2023, 10, 1), date(2023, 12, 30))
    assert word.learning_period == "3 months"
    word = Word("test", date(2020, 1, 1), date(2022, 12, 30))
    assert word.learning_period == "36 months"
    word = Word("test", date(2020, 1, 1), date(2022, 12, 31))
    assert word.learning_period == "3 years"

def test_sanitize():
    assert Word.sanitize("word") == "word"
    assert Word.sanitize("  test with spaces  ") == "test with spaces"
    assert Word.sanitize("") == ""
    assert Word.sanitize(123) == ""
    assert Word.sanitize("word123_!@##$%^&*()_|") == "word"
    assert Word.sanitize("word-word'word") == "word-word'word"
    assert Word.sanitize("word--word''word") == "word-word'word"
    assert Word.sanitize("-word-") == "word"
    assert Word.sanitize("'word'") == "word"
    assert Word.sanitize("a" * 51) == "a" * 50
    