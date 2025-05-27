from word import Word

words_unknown = []
words_known = []

def main():
    load_words()
    print("Words loaded successfully.")

    add_word("example")
    learn_word("example")
    forget_word("example")
    delete_word("example")

    print(f"Unknown words ({len(words_unknown)}):")
    for word in words_unknown:
        print(word)
    print(f"Known words ({len(words_known)}):")
    for word in words_known:
        print(word)

    input("Press Enter to save and quit...")
    save_words()

def load_words():
    global words_known, words_unknown
    words: list = Word.read_from_csv()

    words_known = filter(lambda word: word.is_known, words)
    words_known = sorted(words_known, key=lambda word: word.word)
    words_known = sorted(words_known, key=lambda word: word.learned, reverse=True)
    
    words_unknown = filter(lambda word: not word.is_known, words)
    words_unknown = sorted(words_unknown, key=lambda word: word.word)
    words_unknown = sorted(words_unknown, key=lambda word: word.added, reverse=True)

def save_words():
    global words_known, words_unknown
    words = words_unknown + words_known
    Word.save_to_csv(words)

def find_word_known(word: str) -> Word:
    global words_known
    for w in words_known:
        if w.word == word:
            return w
    return None

def find_word_unknown(word: str) -> Word:
    global words_unknown
    for w in words_unknown:
        if w.word == word:
            return w
    return None

def add_word(word: str):
    if find_word_known(word) or find_word_unknown(word):
        return
    global words_unknown
    w = Word(word)
    words_unknown.insert(0, w)

def learn_word(word: str):
    global words_known, words_unknown
    w = find_word_unknown(word)
    if w is not None:
        words_unknown.remove(w)
        w.learn()
        words_known.insert(0, w.learn())

def forget_word(word: str):
    global words_known, words_unknown
    w = find_word_known(word)
    if w is not None:
        words_known.remove(w)
        words_unknown.insert(0, w.forget())

def delete_word(word: str):
    global words_known, words_unknown
    w = find_word_known(word)
    if w is not None:
        words_known.remove(w)
    w = find_word_unknown(word)
    if w is not None:
        words_unknown.remove(w)
        return

if __name__ == "__main__":
    main()
