from PyQt5.QtWidgets import QTextEdit
from spellchecker import SpellChecker

spell = SpellChecker()


def spellcheck_text(control):
    def wrapper(_):
        text = control.toPlainText()
        text = text.replace("red", "<span style=\"color: #FFFF00\">red</span>")
        control.setHtml(text)

    return wrapper


def extract_text_area_value(control: QTextEdit, func):
    def wrapper():
        value = control.toPlainText()
        func(value)

    return wrapper


def set_answer_index(func, question_index, property_name, index):
    def wrapper():
        func(question_index, property_name, index)

    return wrapper
