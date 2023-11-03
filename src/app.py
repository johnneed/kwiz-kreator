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

    def receive(self, message):
        match message:
            case "trivia_loaded":
                self.__update_trivia_list()
            case "trivia_updated":
                pass
            case "quiz_added":
                self.__update_trivia_list()
            case "quiz_selected":
                self.__display_selected_quiz()
            case "quiz_updated":
                self.__update_trivia_list()
            case "selected_quiz_cleared":
                self.__set_quiz_enabled(False)
            case "selected_quiz_dirty_status_changed":
                pass
            case "trivia_dirty_status_changed":
                pass
            case "selected_quiz_dirty_changed":
                self.saveQuizButton.setEnabled(self.app_state.selected_quiz_is_dirty)
            case _:
                pass

    def __set_quiz_enabled(self, is_enabled=True):
        self.scrollAreaWidgetContents_2.setEnabled(is_enabled)

    def __update_trivia_list(self):
        trivia = self.app_state.get_trivia()
        selected_quiz = self.app_state.get_selected_quiz()
        selected_quiz_id = selected_quiz.id if selected_quiz else None
        self.listWidget.clear()
        if len(trivia.quizzes) > 0:
            for idx, quiz in enumerate(trivia.quizzes):
                list_item = QListWidgetItem(quiz.title)
                list_item.setData(1, quiz.id)
                self.listWidget.addItem(list_item)
                if quiz.id == selected_quiz_id:
                    self.listWidget.setCurrentRow(idx)
            if selected_quiz_id is None:
                self.app_state.set_selected_quiz_by_id(trivia.quizzes[0].id)
                self.listWidget.setCurrentRow(0)
            self.scrollAreaWidgetContents_2.setEnabled(True)
        else:
            self.app_state.clear_selected_quiz()

    def __select_quiz(self):
        quiz_id = self.listWidget.currentItem().data(1)
        self.app_state.set_selected_quiz_by_id(quiz_id)

    def __add_new_quiz(self):
        first_friday = self.app_state.get_trivia().get_first_available_friday().strftime("%Y/%m/%d")
        quiz = Quiz(title="New Quiz", subtitle="", publish_date=first_friday, author="", questions=[])
        self.app_state.add_quiz(quiz)
        self.app_state.set_selected_quiz_is_dirty(False)

    def subscribe(self):
        self.app_state.subscribe(self)

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
        self.saveQuizButton.clicked.connect(self.app_state.save_selected_quiz)
        self.resetQuizButton.clicked.connect(self.app_state.reset_selected_quiz)
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


    def __create_new_trivia(self):
        new_trivia = Trivia(quizzes=[Quiz(title="New Quiz")])
        self.app_state.set_trivia(new_trivia)
        self.opened_file_name = None
        self.actionSave.setEnabled(False)
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
                self.actionSave.setEnabled(True)
            except Exception as e:
                QMessageBox.about(self, "Error", "That does not look like a valid Trail Trivia file\n\n " + str(e))

    def save_file_as(self):
        trivia_data = self.app_state.get_trivia().to_json()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name = QFileDialog.getSaveFileName(self, "Save Trivia File", "",
                                                "JSON Files (*.json)",
                                                options=options)

        if file_name[0]:
            full_path = file_name[0] + ".json" if not file_name[0].endswith(".json") else file_name[0]
            try:
                with open(full_path, 'w') as outfile:
                    json.dump(trivia_data, outfile)
                    outfile.close()
                self.opened_file_name = full_path
                self.actionSave.setEnabled(True)
                self.app_state.set_trivia_is_dirty(False)
            except Exception as e:
                QMessageBox.about(self, "Error", "Unable to save file\n\n " + str(e))

    def save_file(self):
        if self.opened_file_name is not None:
            with open(self.opened_file_name, 'w') as outfile:
                json.dump(self.app_state.get_trivia().to_json(), outfile)
                outfile.close()
            self.app_state.set_trivia_is_dirty(False)
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

    def about(self):
        QMessageBox.about(
            self,
            "About Kwiz Kreator",
            "<p>A UI for creating Trail Trivia files</p>"
            "<p>Play Trail Trivia at https://gmcburlington.org/trail-trivia/</p>"
        )
