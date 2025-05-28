import dearpygui.dearpygui as dpg
import sys
import project
import threading
import subprocess
import pyttsx3

def run():
    project.load_words()

    dpg.create_context()
    dpg.create_viewport(title='Repeat Pronunciation', width=1000, height=600)

    add_word_input()
    unknown_words_table()
    known_words_table()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

    project.save_words()

def add_word_input():
    with dpg.window(label="Enter new word", no_title_bar=True, no_resize=True, pos=(0,0)):
        with dpg.group(horizontal=True):
            dpg.add_input_text(
                tag="input_word",
                hint="Add new word",
                width=400,
                on_enter=True,
                callback=add_word
            )
            dpg.add_button(
                label="Add", 
                callback=add_word,
                width=50
            )

def unknown_words_table():
    with dpg.window(label="Unknown words", tag="unknown_words_window", no_title_bar=True, no_resize=True, width=500, height=500, pos=(0,70)):
        with dpg.table():

            dpg.add_table_column(label="Known", width_fixed=True, init_width_or_weight=40, width_stretch=False) 
            dpg.add_table_column(label="Word") 
            dpg.add_table_column(label="Learning", width_fixed=True, init_width_or_weight=75, width_stretch=False) 
            dpg.add_table_column(label="", width_fixed=True, init_width_or_weight=60, width_stretch=False) 
            dpg.add_table_column(label="", width_fixed=True, init_width_or_weight=60, width_stretch=False)

            for w in project.words_unknown:
                with dpg.table_row():
                    dpg.add_checkbox(label="", default_value=False, callback=learn_word, user_data=w.word)
                    dpg.add_text(w.word)
                    dpg.add_text(w.learning_period)
                    dpg.add_button(label="Listen", callback=listen_word, user_data=w)
                    dpg.add_button(label="Delete", callback=delete_word_unknown, user_data=w)

def known_words_table():
    with dpg.window(label="Known words", tag="known_words_window", no_title_bar=True, no_resize=True, width=500, height=500, pos=(500,70)):
        with dpg.table():

            dpg.add_table_column(label="Known", width_fixed=True, init_width_or_weight=40, width_stretch=False) 
            dpg.add_table_column(label="Word") 
            dpg.add_table_column(label="Learning", width_fixed=True, init_width_or_weight=75, width_stretch=False) 
            dpg.add_table_column(label="", width_fixed=True, init_width_or_weight=60, width_stretch=False)
            dpg.add_table_column(label="", width_fixed=True, init_width_or_weight=60, width_stretch=False)  

            for w in project.words_known:
                with dpg.table_row():
                    dpg.add_checkbox(label="", default_value=True, callback=forget_word, user_data=w.word)
                    dpg.add_text(w.word)
                    dpg.add_text(w.learning_period)
                    dpg.add_button(label="Listen", callback=listen_word, user_data=w)
                    dpg.add_button(label="Delete", callback=delete_word_known, user_data=w) 

def refresh_tables():
    if dpg.does_item_exist("unknown_words_window"):
        dpg.delete_item("unknown_words_window")
    if dpg.does_item_exist("known_words_window"):
        dpg.delete_item("known_words_window")
    unknown_words_table()
    known_words_table()

def add_word(sender, app_data, user_data):
    value = dpg.get_value("input_word")
    project.add_word(value)
    dpg.set_value("input_word", "")
    refresh_tables()

def learn_word(sender, app_data, user_data):
    project.learn_word(user_data)
    refresh_tables()

def forget_word(sender, app_data, user_data):
    project.forget_word(user_data)
    refresh_tables()

def delete_word_unknown(sender, app_data, user_data):
    project.delete_word_unknown(user_data)
    refresh_tables()
        
def delete_word_known(sender, app_data, user_data):
    project.delete_word_known(user_data)
    refresh_tables()

def listen_word(sender, app_data, user_data):
    if sys.platform == "darwin":
        # macOS
        print("Using subprocess for text-to-speech on macOS")
        subprocess.run(["say", user_data.word])
    else:
        # Windows/Linux
        print("Using pyttsx3 for text-to-speech on Windows/Linux")
        engine = pyttsx3.init()
        def speak():
            engine.say(user_data.word)
            engine.runAndWait()
        threading.Thread(target=speak, daemon=True).start()