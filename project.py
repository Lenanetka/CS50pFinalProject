from word import Word
import dearpygui.dearpygui as dpg

words_unknown = []
words_known = []

def main():
    load_words()

    dpg.create_context()

    dpg.create_viewport(title='Repeat Pronunciation', width=1000, height=600)
    with dpg.viewport_menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="Save", callback=lambda s, a, u: save_words())
            dpg.add_menu_item(label="Exit", callback=lambda s, a, u: dpg.stop_dearpygui()) 

    add_word_input()
    unknown_words_table()
    known_words_table()   

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
    
    save_words()

def add_word_input():
    with dpg.window(label="Enter new word", no_title_bar=True, no_resize=True, pos=(0,20)):
        with dpg.group(horizontal=True):
            dpg.add_input_text(
                tag="input_word",
                hint="Add new word",
                width=400,
                on_enter=True,
                callback=lambda s, a, u: (add_word(dpg.get_value(u)), dpg.set_value(u, "")),
                user_data="input_word"
            )
            dpg.add_button(label="Add", callback=lambda s, a, u: (add_word(dpg.get_value("input_word")), dpg.set_value("input_word", "")), width=50)

def unknown_words_table():
    
    global words_unknown
    with dpg.window(label="Unknown words", tag="unknown_words_window", no_title_bar=True, no_resize=True, width=500, height=500, pos=(0,70)):
        with dpg.table(header_row=False):

            for _ in range(5):
                dpg.add_table_column() 

            with dpg.table_row():
                dpg.add_text("Known")
                dpg.add_text("Word")
                dpg.add_text("Added")
                dpg.add_text("Period")
                dpg.add_text("Delete")

            for w in words_unknown:
                with dpg.table_row():
                    dpg.add_checkbox(label="", default_value=False, callback=learn_word, user_data=w.word)
                    dpg.add_text(w.word)
                    dpg.add_text(w.added.isoformat() if w.added else "")
                    dpg.add_text(w.learning_period)
                    dpg.add_button(label="Delete", callback=delete_word_unknown, user_data=w)

def known_words_table():
    global words_known
    with dpg.window(label="Known words", tag="known_words_window", no_title_bar=True, no_resize=True, width=500, height=500, pos=(500,70)):
        with dpg.table(header_row=False):

            for _ in range(6):
                dpg.add_table_column()

            with dpg.table_row():
                dpg.add_text("Known")
                dpg.add_text("Word")
                dpg.add_text("Added")
                dpg.add_text("Learned")
                dpg.add_text("Period")
                dpg.add_text("Delete")

            for w in words_known:
                with dpg.table_row():
                    dpg.add_checkbox(label="", default_value=True, callback=forget_word, user_data=w.word)
                    dpg.add_text(w.word)
                    dpg.add_text(w.added.isoformat() if w.added else "")
                    dpg.add_text(w.learned.isoformat() if w.learned else "")
                    dpg.add_text(w.learning_period)    
                    dpg.add_button(label="Delete", callback=delete_word_known, user_data=w) 

def refresh_tables():
    if dpg.does_item_exist("unknown_words_window"):
        dpg.delete_item("unknown_words_window")
    if dpg.does_item_exist("known_words_window"):
        dpg.delete_item("known_words_window")
    unknown_words_table()
    known_words_table()

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
    global words_unknown
    w = Word(word)
    words_unknown.insert(0, w)
    print (f"Word '{word}' added to unknown words.")
    refresh_tables()

def learn_word(sender, app_data, user_data: str):
    global words_known, words_unknown
    w = find_word_unknown(user_data)
    if w is not None:
        words_unknown.remove(w)
        w.learn()
        words_known.insert(0, w.learn())
    print(f"Word '{user_data}' moved to known words.")
    refresh_tables()

def forget_word(sender, app_data, user_data: str):
    global words_known, words_unknown
    w = find_word_known(user_data)
    if w is not None:
        words_known.remove(w)
        words_unknown.insert(0, w.forget())
    print(f"Word '{user_data}' moved to unknown words.")
    refresh_tables()

def delete_word_unknown(sender, app_data, user_data: Word):
    print(user_data)
    global words_unknown
    if user_data in words_unknown:
        words_unknown.remove(user_data)
        print(f"Word '{user_data.word}' deleted.")
        refresh_tables()
    else:
        print(f"Word '{user_data.word}' not found in unknown words.")
        

def delete_word_known(sender, app_data, user_data: Word):
    global words_known
    if user_data in words_known:
        words_known.remove(user_data)
        print(f"Word '{user_data.word}' deleted.")
        refresh_tables()
    else:
        print(f"Word '{user_data.word}' not found in known words.")

if __name__ == "__main__":
    main()
