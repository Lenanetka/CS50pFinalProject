from word import Word
import gui
import audio

WORDS_CSV = "words.csv"
words_unknown = []
words_known = []

def main():
    gui.run()

def set_words_csv(path: str):
    global WORDS_CSV
    path = path.strip()
    if path == "":
        raise ValueError("File path cannot be empty.")
    if path[-4:] != ".csv":
        raise ValueError("File extension must be'.csv'.")
    WORDS_CSV = path
    print(f"Words CSV file path set to: {path}")

def load_words():
    global words_known, words_unknown, WORDS_CSV
    words: list = Word.read_from_csv(WORDS_CSV)
    words_known = filter(lambda word: word.is_known, words)
    words_known = sorted(words_known, key=lambda word: word.learned, reverse=True)
    words_unknown = filter(lambda word: not word.is_known, words)
    words_unknown = sorted(words_unknown, key=lambda word: word.added, reverse=True)
    print("Words loaded successfully.")

def save_words():
    global words_known, words_unknown
    words = words_unknown + words_known
    Word.save_to_csv(words, WORDS_CSV)
    print("Words saved successfully.")

def add_word(text: str):
    text = Word.sanitize(text)
    if text == "":
        return
    global words_known, words_unknown
    words = words_unknown + words_known
    for w in words:
        if w.word == text:
            return
    words_unknown.insert(0, Word(text))
    print (f"Word '{text}' added to unknown words.")

def learn_word(word: Word):
    global words_known, words_unknown
    if word in words_unknown:
        words_unknown.remove(word)
        words_known.insert(0, word.learn())
    print(f"Word '{word}' moved to known words.")

def forget_word(word: Word):
    global words_known, words_unknown
    if word in words_known:
        words_known.remove(word)
        words_unknown.insert(0, word.forget())
    print(f"Word '{word}' moved to unknown words.")

def listen_word(text: str):
    audio.download_audio(text)
    audio.play_audio(text)

def delete_word_unknown(word: Word):
    global words_unknown
    if word in words_unknown:
        words_unknown.remove(word)
        print(f"Word '{word}' deleted.")
        audio.delete_audio(word.word)
    else:
        print(f"Word '{word}' not found in unknown words.")      

def delete_word_known(word: Word):
    global words_known
    if word in words_known:
        words_known.remove(word)
        print(f"Word '{word}' deleted.")
        audio.delete_audio(word.word)
    else:
        print(f"Word '{word}' not found in known words.")

if __name__ == "__main__":
    main()
