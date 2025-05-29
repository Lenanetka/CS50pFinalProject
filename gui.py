import dearpygui.dearpygui as dpg
import project

def run():
    project.load_words()
    dpg.create_context()
    dpg.create_viewport(title='Repeat Pronunciation', width=1000, height=600)

    layout()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

    project.save_words()

def layout():
    with dpg.window(no_title_bar=True, width=1000, height=600, pos=(0, 0)):
        with dpg.child_window(autosize_x=True, height=40):
            with dpg.group(horizontal=True):
                add_word_input()
        with dpg.child_window(tag="tables_container", autosize_x=True, autosize_y=True):
            with dpg.group(horizontal=True):
                unknown_words_table()
                known_words_table()

def add_word_input():
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
    with dpg.group():
        dpg.add_text("Listen to the pronunciation until you memorize")
        with dpg.child_window(width=480, horizontal_scrollbar=True):
            with dpg.table():
                dpg.add_table_column(label="Known", width_fixed=True, init_width_or_weight=40, width_stretch=False) 
                dpg.add_table_column(label="Word") 
                dpg.add_table_column(label="Learning", width_fixed=True, init_width_or_weight=75, width_stretch=False) 
                dpg.add_table_column(label="", width_fixed=True, init_width_or_weight=60, width_stretch=False) 
                dpg.add_table_column(label="", width_fixed=True, init_width_or_weight=60, width_stretch=False)

                for w in project.words_unknown:
                    with dpg.table_row():
                        dpg.add_checkbox(label="", default_value=False, callback=learn_word, user_data=w)
                        dpg.add_text(w.word)
                        dpg.add_text(w.learning_period)
                        dpg.add_button(label="Listen", callback=listen_word, user_data=w)
                        dpg.add_button(label="Delete", callback=delete_word_unknown, user_data=w)

def known_words_table():
    with dpg.group():
        dpg.add_text("You have memorized the pronunciation of these words")
        with dpg.child_window(width=480, horizontal_scrollbar=True):
            with dpg.table():
                dpg.add_table_column(label="Known", width_fixed=True, init_width_or_weight=40, width_stretch=False) 
                dpg.add_table_column(label="Word") 
                dpg.add_table_column(label="Learning", width_fixed=True, init_width_or_weight=75, width_stretch=False) 
                dpg.add_table_column(label="", width_fixed=True, init_width_or_weight=60, width_stretch=False)
                dpg.add_table_column(label="", width_fixed=True, init_width_or_weight=60, width_stretch=False)  

                for w in project.words_known:
                    with dpg.table_row():
                        dpg.add_checkbox(label="", default_value=True, callback=forget_word, user_data=w)
                        dpg.add_text(w.word)
                        dpg.add_text(w.learning_period)
                        dpg.add_button(label="Listen", callback=listen_word, user_data=w)
                        dpg.add_button(label="Delete", callback=delete_word_known, user_data=w) 

def refresh_tables():
    if dpg.does_item_exist("tables_container"):
        dpg.delete_item("tables_container", children_only=True)
        with dpg.group(horizontal=True, parent="tables_container"):
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
    project.listen_word(user_data.word)