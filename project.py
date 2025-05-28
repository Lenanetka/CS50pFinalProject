from word import Word
import gui

words_unknown = []
words_known = []

def main():
    gui.run()

def load_words():
    global words_known, words_unknown
    words: list = Word.read_from_csv()

    words_known = filter(lambda word: word.is_known, words)
    words_known = sorted(words_known, key=lambda word: word.learned, reverse=True)

    words_unknown = filter(lambda word: not word.is_known, words)
    words_unknown = sorted(words_unknown, key=lambda word: word.added, reverse=True)

    print("Words loaded successfully.")

def save_words():
    global words_known, words_unknown
    words = words_unknown + words_known
    Word.save_to_csv(words)
    print("Words saved successfully.")

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
    if word is None or word.strip() == "":
        return
    global words_unknown
    w = Word(word)
    words_unknown.insert(0, w)
    print (f"Word '{word}' added to unknown words.")

def learn_word(word: str):
    global words_known, words_unknown
    w = find_word_unknown(word)
    if w is not None:
        words_unknown.remove(w)
        w.learn()
        words_known.insert(0, w.learn())
    print(f"Word '{word}' moved to known words.")

def forget_word(word: str):
    global words_known, words_unknown
    w = find_word_known(word)
    if w is not None:
        words_known.remove(w)
        words_unknown.insert(0, w.forget())
    print(f"Word '{word}' moved to unknown words.")

def delete_word_unknown(word: Word):
    print(word)
    global words_unknown
    if word in words_unknown:
        words_unknown.remove(word)
        print(f"Word '{word.word}' deleted.")
    else:
        print(f"Word '{word.word}' not found in unknown words.")
        

def delete_word_known(word: Word):
    global words_known
    if word in words_known:
        words_known.remove(word)
        print(f"Word '{word.word}' deleted.")
    else:
        print(f"Word '{word.word}' not found in known words.")

if __name__ == "__main__":
    main()
