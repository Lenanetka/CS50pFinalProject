import pytest
import project
import os
from word import Word

def test_set_words_csv():
    path = "test/test_words.csv"
    project.set_words_csv(path)
    assert project.WORDS_CSV == path

def test_set_words_csv_error():
    with pytest.raises(ValueError):
        project.set_words_csv("")
    with pytest.raises(ValueError):
        project.set_words_csv("words")
    with pytest.raises(ValueError):
        project.set_words_csv("words.txt")
    with pytest.raises(AttributeError):
        project.set_words_csv(123)

def test_load_words():
    project.set_words_csv("test/test.csv")
    word_cat = Word({"word": "cat", "added": "2022-10-30", "learned": "2022-11-24"})
    word_dog = Word({"word": "dog", "added": "2023-01-01", "learned": ""})
    word_spider = Word({"word": "spider", "added": "test", "learned": "test"})
    project.load_words()
    assert len(project.words_known) == 2
    print(project.words_known)
    assert project.words_known[0] == word_spider
    assert project.words_known[1] == word_cat 
    assert len(project.words_unknown) == 1
    print (project.words_unknown)
    assert project.words_unknown[0] == word_dog

def test_load_words_empty():
    project.set_words_csv("test/empty.csv")
    project.load_words()
    assert len(project.words_known) == 0
    assert len(project.words_unknown) == 0

def test_load_words_non_existed():
    project.set_words_csv("test/non_existed.csv")
    project.load_words()
    assert len(project.words_known) == 0
    assert len(project.words_unknown) == 0

def test_save_words():
    original_path = "test/test.csv"
    save_path = "test/save.csv"
    try:
        os.remove(save_path)
    except FileNotFoundError:
        pass

    project.set_words_csv(original_path)
    project.load_words()
    project.set_words_csv(save_path)
    project.save_words()
    
    word_cat = Word({"word": "cat", "added": "2022-10-30", "learned": "2022-11-24"})
    word_dog = Word({"word": "dog", "added": "2023-01-01", "learned": ""})
    word_spider = Word({"word": "spider", "added": "test", "learned": "test"})
    project.load_words()
    assert len(project.words_known) == 2
    print(project.words_known)
    assert project.words_known[0] == word_spider
    assert project.words_known[1] == word_cat 
    assert len(project.words_unknown) == 1
    print (project.words_unknown)
    assert project.words_unknown[0] == word_dog

def test_add_word():
    words_unknown_before = len(project.words_unknown)
    words_known_before = len(project.words_known)
    project.add_word("unique")
    assert len(project.words_unknown) == words_unknown_before + 1
    assert project.words_unknown[0] == "unique"
    assert len(project.words_known) == words_known_before

def test_add_word_duplicate():
    words_unknown_before = len(project.words_unknown)
    words_known_before = len(project.words_known)
    project.add_word("duplicate")
    project.add_word("duplicate")
    assert len(project.words_unknown) == words_unknown_before + 1
    assert project.words_unknown[0] == "duplicate"
    assert len(project.words_known) == words_known_before

def test_learn_word():
    project.add_word("learn")
    assert "learn" in project.words_unknown
    assert "learn" not in project.words_known

    project.learn_word(project.words_unknown[0])
    assert "learn" not in project.words_unknown
    assert "learn" in project.words_known

def test_forget_word():
    project.add_word("forget")
    project.learn_word(project.words_unknown[0])
    assert "forget" not in project.words_unknown
    assert "forget" in project.words_known

    project.forget_word(project.words_known[0])
    assert "forget" in project.words_unknown
    assert "forget" not in project.words_known

def test_delete_word_unknown():
    project.add_word("delete unknown")
    assert "delete unknown" in project.words_unknown
    project.delete_word_unknown(project.words_unknown[0])
    assert "delete unknown" not in project.words_unknown

def test_delete_word_known():
    project.add_word("delete known")
    project.learn_word(project.words_unknown[0])
    assert "delete known" in project.words_known
    project.delete_word_known(project.words_known[0])
    assert "delete known" not in project.words_known