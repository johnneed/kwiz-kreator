import json

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import (
    QMainWindow, QMessageBox, QFileDialog, QListWidgetItem
)

from .app_state import AppState
from .lib.connect_controls import extract_text_area_value, set_answer_index
from .models import Trivia, Quiz
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
        self.titleLineEdit.textChanged.connect(self.app_state.set_selected_quiz_property('title'))
        self.subtitleLineEdit.textChanged.connect(self.app_state.set_selected_quiz_property('subtitle'))
        self.authorLineEdit.textChanged.connect(self.app_state.set_selected_quiz_property('author'))
        self.publishOnDateEdit.dateChanged.connect(
            lambda q_date: self.app_state.set_selected_quiz_property('publish_date', q_date.toString('yyyy/MM/dd')))
        # Question 1
        self.q1QuestionPlainTextEdit.textChanged.connect(extract_text_area_value(self.q1QuestionPlainTextEdit,
                                                                                 self.app_state.set_question_property(0,
                                                                                                                      'question_text')))
        self.q1AnswerPlainTextEdit.textChanged.connect(
            extract_text_area_value(self.q1AnswerPlainTextEdit, self.app_state.set_question_property(0, 'answer_text')))
        self.q1ImageUrlLineEdit.textChanged.connect(self.app_state.set_question_property(0, 'answer_image'))
        self.q1ImageCaptionLineEdit.textChanged.connect(self.app_state.set_question_property(0, 'answer_image_caption'))
        question_1_choice_radios = [self.q1ChoiceRadioButton_1, self.q1ChoiceRadioButton_2, self.q1ChoiceRadioButton_3,
                                    self.q1ChoiceRadioButton_4]
        for idx, radio in enumerate(question_1_choice_radios):
            radio.toggled.connect(
                set_answer_index(self.app_state.set_question_property, 0, 'correct_answer_index', idx))

        self.q1ChoiceLineEdit_1.textChanged.connect(self.app_state.set_choice_text(0, 0))
        self.q1ChoiceLineEdit_2.textChanged.connect(self.app_state.set_choice_text(0, 1))
        self.q1ChoiceLineEdit_3.textChanged.connect(self.app_state.set_choice_text(0, 2))
        self.q1ChoiceLineEdit_4.textChanged.connect(self.app_state.set_choice_text(0, 3))

        # Question 2
        self.q2QuestionPlainTextEdit.textChanged.connect(extract_text_area_value(self.q2QuestionPlainTextEdit,
                                                                                 self.app_state.set_question_property(1,
                                                                                                                      'question_text')))
        self.q2AnswerPlainTextEdit.textChanged.connect(
            extract_text_area_value(self.q2AnswerPlainTextEdit, self.app_state.set_question_property(1, 'answer_text')))
        self.q2ImageUrlLineEdit.textChanged.connect(self.app_state.set_question_property(1, 'answer_image'))
        self.q2ImageCaptionLineEdit.textChanged.connect(
            self.app_state.set_question_property(1, 'answer_image_caption'))
        question_2_choice_radios = [self.q2ChoiceRadioButton_1, self.q2ChoiceRadioButton_2, self.q2ChoiceRadioButton_3,
                                    self.q2ChoiceRadioButton_4]
        for idx, radio in enumerate(question_2_choice_radios):
            radio.toggled.connect(
                set_answer_index(self.app_state.set_question_property, 1, 'correct_answer_index', idx))

        self.q2ChoiceLineEdit_1.textChanged.connect(self.app_state.set_choice_text(1, 0))
        self.q2ChoiceLineEdit_2.textChanged.connect(self.app_state.set_choice_text(1, 1))
        self.q2ChoiceLineEdit_3.textChanged.connect(self.app_state.set_choice_text(1, 2))
        self.q2ChoiceLineEdit_4.textChanged.connect(self.app_state.set_choice_text(1, 3))

        # Question 3
        self.q3QuestionPlainTextEdit.textChanged.connect(extract_text_area_value(self.q3QuestionPlainTextEdit,
                                                                                 self.app_state.set_question_property(2,
                                                                                                                      'question_text')))
        self.q3AnswerPlainTextEdit.textChanged.connect(
            extract_text_area_value(self.q3AnswerPlainTextEdit, self.app_state.set_question_property(2, 'answer_text')))
        self.q3ImageUrlLineEdit.textChanged.connect(self.app_state.set_question_property(2, 'answer_image'))
        self.q3ImageCaptionLineEdit.textChanged.connect(
            self.app_state.set_question_property(2, 'answer_image_caption'))
        question_3_choice_radios = [self.q3ChoiceRadioButton_1, self.q3ChoiceRadioButton_2, self.q3ChoiceRadioButton_3,
                                    self.q3ChoiceRadioButton_4]
        for idx, radio in enumerate(question_3_choice_radios):
            radio.toggled.connect(
                set_answer_index(self.app_state.set_question_property, 2, 'correct_answer_index', idx))

        self.q3ChoiceLineEdit_1.textChanged.connect(self.app_state.set_choice_text(2, 0))
        self.q3ChoiceLineEdit_2.textChanged.connect(self.app_state.set_choice_text(2, 1))
        self.q3ChoiceLineEdit_3.textChanged.connect(self.app_state.set_choice_text(2, 2))
        self.q3ChoiceLineEdit_4.textChanged.connect(self.app_state.set_choice_text(2, 3))

        # Question 4
        self.q4QuestionPlainTextEdit.textChanged.connect(extract_text_area_value(self.q4QuestionPlainTextEdit,
                                                                                 self.app_state.set_question_property(3,
                                                                                                                      'question_text')))
        self.q4AnswerPlainTextEdit.textChanged.connect(
            extract_text_area_value(self.q4AnswerPlainTextEdit, self.app_state.set_question_property(3, 'answer_text')))
        self.q4ImageUrlLineEdit.textChanged.connect(self.app_state.set_question_property(3, 'answer_image'))
        self.q4ImageCaptionLineEdit.textChanged.connect(
            self.app_state.set_question_property(3, 'answer_image_caption'))
        question_4_choice_radios = [self.q4ChoiceRadioButton_1, self.q4ChoiceRadioButton_2, self.q4ChoiceRadioButton_3,
                                    self.q4ChoiceRadioButton_4]
        for idx, radio in enumerate(question_4_choice_radios):
            radio.toggled.connect(
                set_answer_index(self.app_state.set_question_property, 3, 'correct_answer_index', idx))

        self.q4ChoiceLineEdit_1.textChanged.connect(self.app_state.set_choice_text(3, 0))
        self.q4ChoiceLineEdit_2.textChanged.connect(self.app_state.set_choice_text(3, 1))
        self.q4ChoiceLineEdit_3.textChanged.connect(self.app_state.set_choice_text(3, 2))
        self.q4ChoiceLineEdit_4.textChanged.connect(self.app_state.set_choice_text(3, 3))

        # Question 5
        self.q5QuestionPlainTextEdit.textChanged.connect(extract_text_area_value(self.q5QuestionPlainTextEdit,
                                                                                 self.app_state.set_question_property(4,
                                                                                                                      'question_text')))
        self.q5AnswerPlainTextEdit.textChanged.connect(
            extract_text_area_value(self.q5AnswerPlainTextEdit, self.app_state.set_question_property(4, 'answer_text')))
        self.q5ImageUrlLineEdit.textChanged.connect(self.app_state.set_question_property(4, 'answer_image'))
        self.q5ImageCaptionLineEdit.textChanged.connect(
            self.app_state.set_question_property(4, 'answer_image_caption'))
        question_5_choice_radios = [self.q5ChoiceRadioButton_1, self.q5ChoiceRadioButton_2, self.q5ChoiceRadioButton_3,
                                    self.q5ChoiceRadioButton_4]
        for idx, radio in enumerate(question_5_choice_radios):
            radio.toggled.connect(
                set_answer_index(self.app_state.set_question_property, 4, 'correct_answer_index', idx))

        self.q5ChoiceLineEdit_1.textChanged.connect(self.app_state.set_choice_text(4, 0))
        self.q5ChoiceLineEdit_2.textChanged.connect(self.app_state.set_choice_text(4, 1))
        self.q5ChoiceLineEdit_3.textChanged.connect(self.app_state.set_choice_text(4, 2))
        self.q5ChoiceLineEdit_4.textChanged.connect(self.app_state.set_choice_text(4, 3))

    def __update_trivia_list(self):
        trivia = self.app_state.get_trivia()
        current_index = self.listWidget.currentRow()
        self.listWidget.clear()
        if len(trivia.quizzes) == 0:
            self.app_state.clear_selected_quiz()
            return
        for idx, quiz in enumerate(trivia.quizzes):
            list_item = QListWidgetItem(quiz.title)
            list_item.setData(1, quiz.id)
            self.listWidget.addItem(list_item)
        if current_index >= 0:
            self.listWidget.setCurrentRow(current_index)

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
            self.q1QuestionPlainTextEdit.setPlainText(quiz.questions[0].question_text)
            self.q1AnswerPlainTextEdit.setPlainText(quiz.questions[0].answer_text)
            self.q1ImageUrlLineEdit.setText(quiz.questions[0].answer_image)
            self.q1ImageCaptionLineEdit.setText(quiz.questions[0].answer_image_caption)
            self.q1ChoiceLineEdit_1.setText(quiz.questions[0].choices[0].text)
            self.q1ChoiceLineEdit_2.setText(quiz.questions[0].choices[1].text)
            self.q1ChoiceLineEdit_3.setText(quiz.questions[0].choices[2].text)
            self.q1ChoiceLineEdit_4.setText(quiz.questions[0].choices[3].text)
            [self.q1ChoiceRadioButton_1, self.q1ChoiceRadioButton_2, self.q1ChoiceRadioButton_3,
             self.q1ChoiceRadioButton_4][quiz.questions[0].correct_answer_index].setChecked(True)
            # Update Question 2
            self.q2QuestionPlainTextEdit.setPlainText(quiz.questions[1].question_text)
            self.q2AnswerPlainTextEdit.setPlainText(quiz.questions[1].answer_text)
            self.q2ImageUrlLineEdit.setText(quiz.questions[1].answer_image)
            self.q2ImageCaptionLineEdit.setText(quiz.questions[1].answer_image_caption)
            self.q2ChoiceLineEdit_1.setText(quiz.questions[1].choices[0].text)
            self.q2ChoiceLineEdit_2.setText(quiz.questions[1].choices[1].text)
            self.q2ChoiceLineEdit_3.setText(quiz.questions[1].choices[2].text)
            self.q2ChoiceLineEdit_4.setText(quiz.questions[1].choices[3].text)
            [self.q2ChoiceRadioButton_1, self.q2ChoiceRadioButton_2, self.q2ChoiceRadioButton_3,
             self.q2ChoiceRadioButton_4][quiz.questions[1].correct_answer_index].setChecked(True)
            # Update Question 3
            self.q3QuestionPlainTextEdit.setPlainText(quiz.questions[2].question_text)
            self.q3AnswerPlainTextEdit.setPlainText(quiz.questions[2].answer_text)
            self.q3ImageUrlLineEdit.setText(quiz.questions[2].answer_image)
            self.q3ImageCaptionLineEdit.setText(quiz.questions[2].answer_image_caption)
            self.q3ChoiceLineEdit_1.setText(quiz.questions[2].choices[0].text)
            self.q3ChoiceLineEdit_2.setText(quiz.questions[2].choices[1].text)
            self.q3ChoiceLineEdit_3.setText(quiz.questions[2].choices[2].text)
            self.q3ChoiceLineEdit_4.setText(quiz.questions[2].choices[3].text)
            [self.q3ChoiceRadioButton_1, self.q3ChoiceRadioButton_2, self.q3ChoiceRadioButton_3,
             self.q3ChoiceRadioButton_4][quiz.questions[2].correct_answer_index].setChecked(True)
            # Update Question 4
            self.q4QuestionPlainTextEdit.setPlainText(quiz.questions[3].question_text)
            self.q4AnswerPlainTextEdit.setPlainText(quiz.questions[3].answer_text)
            self.q4ImageUrlLineEdit.setText(quiz.questions[3].answer_image)
            self.q4ImageCaptionLineEdit.setText(quiz.questions[3].answer_image_caption)
            self.q4ChoiceLineEdit_1.setText(quiz.questions[3].choices[0].text)
            self.q4ChoiceLineEdit_2.setText(quiz.questions[3].choices[1].text)
            self.q4ChoiceLineEdit_3.setText(quiz.questions[3].choices[2].text)
            self.q4ChoiceLineEdit_4.setText(quiz.questions[3].choices[3].text)
            [self.q4ChoiceRadioButton_1, self.q4ChoiceRadioButton_2, self.q4ChoiceRadioButton_3,
             self.q4ChoiceRadioButton_4][quiz.questions[3].correct_answer_index].setChecked(True)
            # Update Question 5
            self.q5QuestionPlainTextEdit.setPlainText(quiz.questions[4].question_text)
            self.q5AnswerPlainTextEdit.setPlainText(quiz.questions[4].answer_text)
            self.q5ImageUrlLineEdit.setText(quiz.questions[4].answer_image)
            self.q5ImageCaptionLineEdit.setText(quiz.questions[4].answer_image_caption)
            self.q5ChoiceLineEdit_1.setText(quiz.questions[4].choices[0].text)
            self.q5ChoiceLineEdit_2.setText(quiz.questions[4].choices[1].text)
            self.q5ChoiceLineEdit_3.setText(quiz.questions[4].choices[2].text)
            self.q5ChoiceLineEdit_4.setText(quiz.questions[4].choices[3].text)
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
