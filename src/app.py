import json
from functools import partial

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import (
    QMainWindow, QMessageBox, QFileDialog, QListWidgetItem
)

from . import Quiz
from .app_state import AppState
from .models import Trivia
from .ui import Ui_MainWindow


# from autocorrect import Speller
class App(QMainWindow, Ui_MainWindow):

    # spell = Speller(lang='en')
    def __init__(self, parent=None):
        super().__init__(parent)
        self.app_state = AppState()
        self.setupUi(self)
        self.connect_signals_slots()
        self.subscribe()
        self.scrollAreaWidgetContents_2.setEnabled(False)
        self.opened_file_name = None

    def subscribe(self):
        self.app_state.subscribe(self)

    def receive(self, message):
        match message:
            case "trivia_loaded":
                self.__update_trivia_list()
                self.__set_menu_state()
            case "trivia_updated":
                self.__set_menu_state()
            case "quiz_added":
                self.__update_trivia_list()
                self.__set_menu_state()
            case "quiz_selected":
                self.__display_selected_quiz()
                self.__set_menu_state()
            case "quiz_updated":
                self.__update_trivia_list()
                self.__set_menu_state()
            case "selected_quiz_cleared":
                self.__set_menu_state()
            case "dirty_changed":
                self.__set_menu_state()
            case "quiz_updated":
                self.__update_trivia_list()
                self.__set_menu_state()
            case _:
                pass

    def connect_signals_slots(self):
        self.actionNew.triggered.connect(self.__create_new_trivia)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionNew_Quiz.triggered.connect(self.__add_new_quiz)
        self.actionSave.triggered.connect(self.save_file)
        self.actionSave_As.triggered.connect(self.save_file_as)
        # self.action_Find_Replace.triggered.connect(self.findAndReplace)
        self.actionAbout.triggered.connect(self.about)
        self.listWidget.itemSelectionChanged.connect(self.__select_quiz)
        # Quiz Controls
        self.titleLineEdit.textChanged.connect(partial(self.app_state.set_selected_quiz_property, 'title'))
        self.subtitleLineEdit.textChanged.connect(partial(self.app_state.set_selected_quiz_property, 'subtitle'))
        self.authorLineEdit.textChanged.connect(partial(self.app_state.set_selected_quiz_property, 'author'))
        self.publishOnDateEdit.dateChanged.connect(
            lambda q_date: self.app_state.set_selected_quiz_property('publish_date', q_date.toString('yyyy/MM/dd')))
        # Question 1
        self.q1QuestionTextEdit.textChanged.connect(partial(self.app_state.set_question_property, 0, 'question_text'))
        self.q1AnswerTextEdit.textChanged.connect(partial(self.app_state.set_question_property, 0, 'answer_text'))
        self.q1ImageUrlLineEdit.textChanged.connect(partial(self.app_state.set_question_property, 0, 'answer_image'))
        self.q1ImageCaptionLineEdit.textChanged.connect(
            partial(self.app_state.set_question_property, 0, 'answer_image_caption'))
        question_1_choice_radios = [self.q1ChoiceRadioButton_1, self.q1ChoiceRadioButton_2, self.q1ChoiceRadioButton_3,
                                    self.q1ChoiceRadioButton_4]
        for idx, radio in enumerate(question_1_choice_radios):
            radio.toggled.connect(lambda _: self.app_state.set_question_property(0, 'correct_answer_index', idx))

        self.q1Choice1LineEdit_2.textChanged.connect(partial(self.app_state.set_choice_text, 0, 0, 'text'))
        self.q1Choice1LineEdit_2.textChanged.connect(partial(self.app_state.set_choice_text, 0, 1, 'text'))
        self.q1Choice1LineEdit_3.textChanged.connect(partial(self.app_state.set_choice_text, 0, 2, 'text'))
        self.q1Choice1LineEdit_4.textChanged.connect(partial(self.app_state.set_choice_text, 0, 3, 'text'))
        # Question 2
        self.q2QuestionTextEdit.textChanged.connect(partial(self.app_state.set_question_property, 0, 'question_text'))
        self.q2AnswerTextEdit.textChanged.connect(partial(self.app_state.set_question_property, 0, 'answer_text'))
        self.q2ImageUrlLineEdit.textChanged.connect(partial(self.app_state.set_question_property, 0, 'answer_image'))
        self.q2ImageCaptionLineEdit.textChanged.connect(
            partial(self.app_state.set_question_property, 0, 'answer_image_caption'))
        question_1_choice_radios = [self.q2ChoiceRadioButton_1, self.q2ChoiceRadioButton_2, self.q2ChoiceRadioButton_3,
                                    self.q2ChoiceRadioButton_4]
        for idx, radio in enumerate(question_1_choice_radios):
            radio.toggled.connect(lambda _: self.app_state.set_question_property(0, 'correct_answer_index', idx))

        self.q2Choice1LineEdit_2.textChanged.connect(partial(self.app_state.set_choice_text, 0, 0, 'text'))
        self.q2Choice1LineEdit_2.textChanged.connect(partial(self.app_state.set_choice_text, 0, 1, 'text'))
        self.q2Choice1LineEdit_3.textChanged.connect(partial(self.app_state.set_choice_text, 0, 2, 'text'))
        self.q2Choice1LineEdit_4.textChanged.connect(partial(self.app_state.set_choice_text, 0, 3, 'text'))
        # Question 3
        self.q3QuestionTextEdit.textChanged.connect(partial(self.app_state.set_question_property, 0, 'question_text'))
        self.q3AnswerTextEdit.textChanged.connect(partial(self.app_state.set_question_property, 0, 'answer_text'))
        self.q3ImageUrlLineEdit.textChanged.connect(partial(self.app_state.set_question_property, 0, 'answer_image'))
        self.q3ImageCaptionLineEdit.textChanged.connect(
            partial(self.app_state.set_question_property, 0, 'answer_image_caption'))
        question_1_choice_radios = [self.q3ChoiceRadioButton_1, self.q3ChoiceRadioButton_2, self.q3ChoiceRadioButton_3,
                                    self.q3ChoiceRadioButton_4]
        for idx, radio in enumerate(question_1_choice_radios):
            radio.toggled.connect(lambda _: self.app_state.set_question_property(0, 'correct_answer_index', idx))

        self.q3Choice1LineEdit_2.textChanged.connect(partial(self.app_state.set_choice_text, 0, 0, 'text'))
        self.q3Choice1LineEdit_2.textChanged.connect(partial(self.app_state.set_choice_text, 0, 1, 'text'))
        self.q3Choice1LineEdit_3.textChanged.connect(partial(self.app_state.set_choice_text, 0, 2, 'text'))
        self.q3Choice1LineEdit_4.textChanged.connect(partial(self.app_state.set_choice_text, 0, 3, 'text'))
        # Question 4
        self.q4QuestionTextEdit.textChanged.connect(partial(self.app_state.set_question_property, 0, 'question_text'))
        self.q4AnswerTextEdit.textChanged.connect(partial(self.app_state.set_question_property, 0, 'answer_text'))
        self.q4ImageUrlLineEdit.textChanged.connect(partial(self.app_state.set_question_property, 0, 'answer_image'))
        self.q4ImageCaptionLineEdit.textChanged.connect(
            partial(self.app_state.set_question_property, 0, 'answer_image_caption'))
        question_1_choice_radios = [self.q4ChoiceRadioButton_1, self.q4ChoiceRadioButton_2, self.q4ChoiceRadioButton_3,
                                    self.q4ChoiceRadioButton_4]
        for idx, radio in enumerate(question_1_choice_radios):
            radio.toggled.connect(lambda _: self.app_state.set_question_property(0, 'correct_answer_index', idx))

        self.q4Choice1LineEdit_2.textChanged.connect(partial(self.app_state.set_choice_text, 0, 0, 'text'))
        self.q4Choice1LineEdit_2.textChanged.connect(partial(self.app_state.set_choice_text, 0, 1, 'text'))
        self.q4Choice1LineEdit_3.textChanged.connect(partial(self.app_state.set_choice_text, 0, 2, 'text'))
        self.q4Choice1LineEdit_4.textChanged.connect(partial(self.app_state.set_choice_text, 0, 3, 'text'))
        # Question 1
        self.q5QuestionTextEdit.textChanged.connect(partial(self.app_state.set_question_property, 0, 'question_text'))
        self.q5AnswerTextEdit.textChanged.connect(partial(self.app_state.set_question_property, 0, 'answer_text'))
        self.q5ImageUrlLineEdit.textChanged.connect(partial(self.app_state.set_question_property, 0, 'answer_image'))
        self.q5ImageCaptionLineEdit.textChanged.connect(
            partial(self.app_state.set_question_property, 0, 'answer_image_caption'))
        question_1_choice_radios = [self.q5ChoiceRadioButton_1, self.q5ChoiceRadioButton_2, self.q5ChoiceRadioButton_3,
                                    self.q5ChoiceRadioButton_4]
        for idx, radio in enumerate(question_1_choice_radios):
            radio.toggled.connect(lambda _: self.app_state.set_question_property(0, 'correct_answer_index', idx))

        self.q5Choice1LineEdit_2.textChanged.connect(partial(self.app_state.set_choice_text, 0, 0, 'text'))
        self.q5Choice1LineEdit_2.textChanged.connect(partial(self.app_state.set_choice_text, 0, 1, 'text'))
        self.q5Choice1LineEdit_3.textChanged.connect(partial(self.app_state.set_choice_text, 0, 2, 'text'))
        self.q5Choice1LineEdit_4.textChanged.connect(partial(self.app_state.set_choice_text, 0, 3, 'text'))

    def __update_trivia_list(self):
        trivia = self.app_state.get_trivia()
        self.listWidget.clear()
        if len(trivia.quizzes) == 0:
            self.app_state.clear_selected_quiz()
            return
        for idx, quiz in enumerate(trivia.quizzes):
            list_item = QListWidgetItem(quiz.title)
            list_item.setData(1, quiz.id)
            self.listWidget.addItem(list_item)

    def __select_quiz(self):
        quiz_id = self.listWidget.currentItem().data(1)
        if self.app_state.is_dirty:
            reply = QMessageBox.question(self, 'Message',
                                         "You have unsaved changes. Do you want to save them?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.app_state.update_trivia_with_selected_quiz()
        if quiz_id is None:
            return
        self.app_state.set_selected_quiz_by_id(quiz_id)

    def __add_new_quiz(self):
        first_friday = self.app_state.get_trivia().get_first_available_friday().strftime("%Y/%m/%d")
        quiz = Quiz(title="New Quiz", subtitle="", publish_date=first_friday, author="", questions=[])
        self.app_state.add_quiz(quiz)

    def __create_new_trivia(self):
        new_trivia = Trivia(quizzes=[Quiz(title="New Quiz")])
        self.app_state.set_trivia(new_trivia)
        self.opened_file_name = None
        self.listWidget.setCurrentRow(0)

    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self,
                                                   "QFileDialog.getOpenFileName()",
                                                   "",
                                                   "JSON Files (*.json)",
                                                   options=options)
        if file_name:
            try:
                with open(file_name) as json_file:
                    data = json.load(json_file)
                    trivia = Trivia.from_json(data)
                    self.app_state.set_trivia(trivia)
                self.opened_file_name = file_name
            except Exception as e:
                QMessageBox.about(self, "Error", "That does not look like a valid Trail Trivia file\n\n " + str(e))

    def save_file_as(self):
        original_file_path = self.opened_file_name or ""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name = QFileDialog.getSaveFileName(self, "Save Trivia File", original_file_path,
                                                "JSON Files (*.json)",
                                                options=options)

        if file_name[0]:
            full_path = file_name[0] + ".json" if not file_name[0].endswith(".json") else file_name[0]
            if self.app_state.is_dirty:
                self.app_state.update_trivia_with_selected_quiz()
            trivia_data = self.app_state.get_trivia().to_json()
            try:
                with open(full_path, 'w') as outfile:
                    json.dump(trivia_data, outfile)
                    outfile.close()
                self.opened_file_name = full_path
                self.app_state.set_dirty(False)
            except Exception as e:
                QMessageBox.about(self, "Error",
                                  "<p>Unable to save to file " + full_path + "</p><p>" + str(e) + "</p>")

    def save_file(self):
        if self.opened_file_name is not None:
            if self.app_state.is_dirty:
                self.app_state.update_trivia_with_selected_quiz()
            trivia_data = self.app_state.get_trivia().to_json()
            with open(self.opened_file_name, 'w') as outfile:
                json.dump(trivia_data, outfile)
                outfile.close()
            self.app_state.set_dirty(False)

    def __display_selected_quiz(self):
        quiz = self.app_state.get_selected_quiz()
        if quiz:
            title = quiz.title
            self.titleLineEdit.setText(title)
            self.subtitleLineEdit.setText(quiz.subtitle)
            self.publishOnDateEdit.setDate(QDate.fromString(quiz.publish_date, 'yyyy/MM/dd'))
            self.authorLineEdit.setText(quiz.author)
            # Update Question 1
            self.q1QuestionTextEdit.setText(quiz.questions[0].question_text)
            self.q1AnswerTextEdit.setText(quiz.questions[0].answer_text)
            self.q1ImageUrlLineEdit.setText(quiz.questions[0].answer_image)
            self.q1ImageCaptionLineEdit.setText(quiz.questions[0].answer_image_caption)
            self.q1Choice1LineEdit_1.setText(quiz.questions[0].choices[0].text)
            self.q1Choice1LineEdit_2.setText(quiz.questions[0].choices[1].text)
            self.q1Choice1LineEdit_3.setText(quiz.questions[0].choices[2].text)
            self.q1Choice1LineEdit_4.setText(quiz.questions[0].choices[3].text)
            [self.q1ChoiceRadioButton_1, self.q1ChoiceRadioButton_2, self.q1ChoiceRadioButton_3,
             self.q1ChoiceRadioButton_4][quiz.questions[0].correct_answer_index].setChecked(True)
            # Update Question 2
            self.q2QuestionTextEdit.setText(quiz.questions[1].question_text)
            self.q2AnswerTextEdit.setText(quiz.questions[1].answer_text)
            self.q2ImageUrlLineEdit.setText(quiz.questions[1].answer_image)
            self.q2ImageCaptionLineEdit.setText(quiz.questions[1].answer_image_caption)
            self.q2Choice1LineEdit_1.setText(quiz.questions[1].choices[0].text)
            self.q2Choice1LineEdit_2.setText(quiz.questions[1].choices[1].text)
            self.q2Choice1LineEdit_3.setText(quiz.questions[1].choices[2].text)
            self.q2Choice1LineEdit_4.setText(quiz.questions[1].choices[3].text)
            [self.q2ChoiceRadioButton_1, self.q2ChoiceRadioButton_2, self.q2ChoiceRadioButton_3,
             self.q2ChoiceRadioButton_4][quiz.questions[1].correct_answer_index].setChecked(True)
            # Update Question 3
            self.q3QuestionTextEdit.setText(quiz.questions[2].question_text)
            self.q3AnswerTextEdit.setText(quiz.questions[2].answer_text)
            self.q3ImageUrlLineEdit.setText(quiz.questions[2].answer_image)
            self.q3ImageCaptionLineEdit.setText(quiz.questions[2].answer_image_caption)
            self.q3Choice1LineEdit_1.setText(quiz.questions[2].choices[0].text)
            self.q3Choice1LineEdit_2.setText(quiz.questions[2].choices[1].text)
            self.q3Choice1LineEdit_3.setText(quiz.questions[2].choices[2].text)
            self.q3Choice1LineEdit_4.setText(quiz.questions[2].choices[3].text)
            [self.q3ChoiceRadioButton_1, self.q3ChoiceRadioButton_2, self.q3ChoiceRadioButton_3,
             self.q3ChoiceRadioButton_4][quiz.questions[2].correct_answer_index].setChecked(True)
            # Update Question 4
            self.q4QuestionTextEdit.setText(quiz.questions[3].question_text)
            self.q4AnswerTextEdit.setText(quiz.questions[3].answer_text)
            self.q4ImageUrlLineEdit.setText(quiz.questions[3].answer_image)
            self.q4ImageCaptionLineEdit.setText(quiz.questions[3].answer_image_caption)
            self.q4Choice1LineEdit_1.setText(quiz.questions[3].choices[0].text)
            self.q4Choice1LineEdit_2.setText(quiz.questions[3].choices[1].text)
            self.q4Choice1LineEdit_3.setText(quiz.questions[3].choices[2].text)
            self.q4Choice1LineEdit_4.setText(quiz.questions[3].choices[3].text)
            [self.q4ChoiceRadioButton_1, self.q4ChoiceRadioButton_2, self.q4ChoiceRadioButton_3,
             self.q4ChoiceRadioButton_4][quiz.questions[3].correct_answer_index].setChecked(True)
            # Update Question 5
            self.q5QuestionTextEdit.setText(quiz.questions[4].question_text)
            self.q5AnswerTextEdit.setText(quiz.questions[4].answer_text)
            self.q5ImageUrlLineEdit.setText(quiz.questions[4].answer_image)
            self.q5ImageCaptionLineEdit.setText(quiz.questions[4].answer_image_caption)
            self.q5Choice1LineEdit_1.setText(quiz.questions[4].choices[0].text)
            self.q5Choice1LineEdit_2.setText(quiz.questions[4].choices[1].text)
            self.q5Choice1LineEdit_3.setText(quiz.questions[4].choices[2].text)
            self.q5Choice1LineEdit_4.setText(quiz.questions[4].choices[3].text)
            [self.q5ChoiceRadioButton_1, self.q5ChoiceRadioButton_2, self.q5ChoiceRadioButton_3,
             self.q5ChoiceRadioButton_4][quiz.questions[4].correct_answer_index].setChecked(True)
        else:
            pass

    def __set_menu_state(self):
        has_quizzes = len(self.app_state.get_trivia().quizzes) > 0
        self.actionNew_Quiz.setEnabled(has_quizzes)
        self.actionSave.setEnabled(has_quizzes and self.app_state.is_dirty)
        self.actionSave_As.setEnabled(has_quizzes)
        self.scrollAreaWidgetContents_1.setEnabled(has_quizzes)
        quiz_is_selected = self.app_state.get_selected_quiz() is not None
        self.scrollAreaWidgetContents_2.setEnabled(quiz_is_selected)

    def about(self):
        QMessageBox.about(
            self,
            "About Kwiz Kreator",
            "<p>An editor for creating Trail Trivia files.</p>"
            "<p>Play Trail Trivia at:</p>"
            "<p><a src='https://gmcburlington.org/trail-trivia/'>https://gmcburlington.org/trail-trivia/</a></p>"
        )
