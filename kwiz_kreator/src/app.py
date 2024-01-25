import json
import os
from datetime import datetime

from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QMainWindow, QMessageBox, QFileDialog, QListWidgetItem
)
from toolz import curry

from .app_state import AppState
from .lib.app_config import AppConfig
from .lib.connect_controls import extract_text_area_value, set_answer_index
from .lib.upload_via_ftp import UploadViaFTP
from .models import Trivia, Quiz
from .preview.launch import preview_quiz
from .ui import Ui_MainWindow
from .ui.prefs_dialog import PrefsDialog


class App(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        app_config_path = os.path.dirname(os.path.realpath(__file__)) + '/../data/app_config.json'
        self.app_config = AppConfig(app_config_path)
        self.app_state = AppState()
        self.upload = UploadViaFTP(self.app_config.ftp_config)
        self.subscribe()
        self.setupUi(self)
        self.connect_main_signals_slots()
        self.connect_selected_quiz_signal_slots()
        self.__set_window_dimensions()
        self.__display_recent_files()
        self.scrollAreaWidgetContents_2.setEnabled(False)
        self.opened_file_name = None
        self.setWindowIcon(QIcon("./images/icon.png"))

    def subscribe(self):
        self.app_state.subscribe(self)
        self.app_config.subscribe(self)
        self.upload.subscribe(self)

    def receive(self, message):
        print('APP RECEIVED MESSAGE: ' + message)
        match message:
            case "app_config_loaded":
                print("App Config Loaded")
                self.upload.sftp_config = self.app_config.ftp_config
                self.splitter.setSizes(self.app_config.splitter_position)
            case "recent_files_changed":
                self.__display_recent_files()
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
            case "quiz_deleted":
                self.__update_trivia_list()
                self.__set_menu_state()
            case "questions_reordered":
                self.__display_selected_quiz()
            case "trivia_deployed":
                self.__alert_file_deployed()
            case _:
                pass

    def disconnect_selected_quiz_signal_slots(self):
        self.titleLineEdit.disconnect()
        self.subtitleLineEdit.disconnect()
        self.authorLineEdit.disconnect()
        self.publishOnDateEdit.disconnect()
        self.q1QuestionTextEdit.disconnect()
        self.q1AnswerTextEdit.disconnect()
        self.q1ImageCaptionLineEdit.disconnect()
        self.q1ImageUrlLineEdit.disconnect()
        self.q1ChoiceRadioButton_1.disconnect()
        self.q1ChoiceRadioButton_2.disconnect()
        self.q1ChoiceRadioButton_3.disconnect()
        self.q1ChoiceRadioButton_4.disconnect()
        self.q1ChoiceLineEdit_1.disconnect()
        self.q1ChoiceLineEdit_2.disconnect()
        self.q1ChoiceLineEdit_3.disconnect()
        self.q1ChoiceLineEdit_4.disconnect()
        self.q2QuestionTextEdit.disconnect()
        self.q2AnswerTextEdit.disconnect()
        self.q2ImageCaptionLineEdit.disconnect()
        self.q2ImageUrlLineEdit.disconnect()
        self.q2ChoiceRadioButton_1.disconnect()
        self.q2ChoiceRadioButton_2.disconnect()
        self.q2ChoiceRadioButton_3.disconnect()
        self.q2ChoiceRadioButton_4.disconnect()
        self.q2ChoiceLineEdit_1.disconnect()
        self.q2ChoiceLineEdit_2.disconnect()
        self.q2ChoiceLineEdit_3.disconnect()
        self.q2ChoiceLineEdit_4.disconnect()
        self.q3QuestionTextEdit.disconnect()
        self.q3AnswerTextEdit.disconnect()
        self.q3ImageCaptionLineEdit.disconnect()
        self.q3ImageUrlLineEdit.disconnect()
        self.q3ChoiceRadioButton_1.disconnect()
        self.q3ChoiceRadioButton_2.disconnect()
        self.q3ChoiceRadioButton_3.disconnect()
        self.q3ChoiceRadioButton_4.disconnect()
        self.q3ChoiceLineEdit_1.disconnect()
        self.q3ChoiceLineEdit_2.disconnect()
        self.q3ChoiceLineEdit_3.disconnect()
        self.q3ChoiceLineEdit_4.disconnect()
        self.q4QuestionTextEdit.disconnect()
        self.q4AnswerTextEdit.disconnect()
        self.q4ImageCaptionLineEdit.disconnect()
        self.q4ImageUrlLineEdit.disconnect()
        self.q4ChoiceRadioButton_1.disconnect()
        self.q4ChoiceRadioButton_2.disconnect()
        self.q4ChoiceRadioButton_3.disconnect()
        self.q4ChoiceRadioButton_4.disconnect()
        self.q4ChoiceLineEdit_1.disconnect()
        self.q4ChoiceLineEdit_2.disconnect()
        self.q4ChoiceLineEdit_3.disconnect()
        self.q4ChoiceLineEdit_4.disconnect()
        self.q5QuestionTextEdit.disconnect()
        self.q5AnswerTextEdit.disconnect()
        self.q5ImageCaptionLineEdit.disconnect()
        self.q5ImageUrlLineEdit.disconnect()
        self.q5ChoiceRadioButton_1.disconnect()
        self.q5ChoiceRadioButton_2.disconnect()
        self.q5ChoiceRadioButton_3.disconnect()
        self.q5ChoiceRadioButton_4.disconnect()
        self.q5ChoiceLineEdit_1.disconnect()
        self.q5ChoiceLineEdit_2.disconnect()
        self.q5ChoiceLineEdit_3.disconnect()
        self.q5ChoiceLineEdit_4.disconnect()

    def save_splitter_sizes(self):
        sizes = self.splitter.sizes()
        print("SIZES ARE:" + str(sizes))
        self.app_config.save_window_preference(AppConfig.window_preferences.SPLITTER_POSITION, sizes)

    def save_window_state(self, state):
        print("WINDOW STATE IS:" + str(state))
        self.app_config.save_window_preference(AppConfig.window_preferences.WINDOW_MODE, state)

    def connect_main_signals_slots(self):

        self.splitter.splitterMoved.connect(self.save_splitter_sizes)
        self.actionSettings.triggered.connect(self.__set_settings)
        self.actionNew.triggered.connect(self.__create_new_trivia)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionNew_Quiz.triggered.connect(self.__add_new_quiz)
        self.actionSave.triggered.connect(self.save_file)
        self.actionSave_As.triggered.connect(self.save_file_as)
        self.actionPreview.triggered.connect(self.__preview_quiz)
        self.actionRemove_Quiz.triggered.connect(self.__delete_selected_quiz)
        self.actionDeploy.triggered.connect(self.__deploy_trivia)
        self.actionAbout.triggered.connect(self.about)
        self.listWidget.itemSelectionChanged.connect(self.__select_quiz)
        self.actionClear_Menu.triggered.connect(self.app_config.clear_recent_files)
        self.q1DownButton.clicked.connect(self.app_state.swap_questions(0, 1))
        self.q2UpButton.clicked.connect(self.app_state.swap_questions(1, 0))
        self.q2DownButton.clicked.connect(self.app_state.swap_questions(1, 2))
        self.q3UpButton.clicked.connect(self.app_state.swap_questions(2, 1))
        self.q3DownButton.clicked.connect(self.app_state.swap_questions(2, 3))
        self.q4UpButton.clicked.connect(self.app_state.swap_questions(3, 2))
        self.q4DownButton.clicked.connect(self.app_state.swap_questions(3, 4))
        self.q5UpButton.clicked.connect(self.app_state.swap_questions(4, 3))

    @curry
    def process_text(self, control_id, index: int, property_name: str, text: str):
        print("PROCESSING TEXT!!!!!!!!!!!!!!!!!!!" + text)
        self.app_state.set_question_property(index, property_name, text)
        self.grammar_checker.match(control_id, text)

    def connect_selected_quiz_signal_slots(self):
        # Quiz Controls
        self.titleLineEdit.textEdited.connect(self.app_state.set_selected_quiz_property('title'))
        self.subtitleLineEdit.textEdited.connect(self.app_state.set_selected_quiz_property('subtitle'))
        self.authorLineEdit.textEdited.connect(self.app_state.set_selected_quiz_property('author'))
        self.publishOnDateEdit.dateChanged.connect(
            lambda q_date: self.app_state.set_selected_quiz_property('publish_date', q_date.toString('yyyy/MM/dd')))

        # Question 1
        self.q1QuestionTextEdit.textChanged.connect(
            extract_text_area_value(self.q1QuestionTextEdit,
                                    self.process_text(self.q1QuestionTextEdit.id, 0, 'question_text')))
        self.q1AnswerTextEdit.textChanged.connect(
            extract_text_area_value(self.q1AnswerTextEdit,
                                    self.process_text(self.q1AnswerTextEdit.id, 0, 'answer_text')))
        self.q1ImageUrlLineEdit.textEdited.connect(self.app_state.set_question_property(0, 'answer_image'))
        self.q1ImageCaptionLineEdit.textEdited.connect(self.app_state.set_question_property(0, 'answer_image_caption'))
        question_1_choice_radios = [self.q1ChoiceRadioButton_1,
                                    self.q1ChoiceRadioButton_2,
                                    self.q1ChoiceRadioButton_3,
                                    self.q1ChoiceRadioButton_4]
        for idx, radio in enumerate(question_1_choice_radios):
            radio.toggled.connect(
                set_answer_index(self.app_state.set_question_property, 0, 'correct_answer_index', idx))

        self.q1ChoiceLineEdit_1.textEdited.connect(self.app_state.set_choice_text(0, 0))
        self.q1ChoiceLineEdit_2.textEdited.connect(self.app_state.set_choice_text(0, 1))
        self.q1ChoiceLineEdit_3.textEdited.connect(self.app_state.set_choice_text(0, 2))
        self.q1ChoiceLineEdit_4.textEdited.connect(self.app_state.set_choice_text(0, 3))

        # Question 2
        self.q2QuestionTextEdit.textChanged.connect(extract_text_area_value(self.q2QuestionTextEdit, self.process_text(
            self.q2QuestionTextEdit.id, 1, 'question_text')))
        self.q2AnswerTextEdit.textChanged.connect(extract_text_area_value(self.q2AnswerTextEdit,
                                                                          self.process_text(self.q2AnswerTextEdit.id, 1,
                                                                                            'answer_text')))
        self.q2ImageUrlLineEdit.textEdited.connect(self.app_state.set_question_property(1, 'answer_image'))
        self.q2ImageCaptionLineEdit.textEdited.connect(self.app_state.set_question_property(1, 'answer_image_caption'))
        question_2_choice_radios = [self.q2ChoiceRadioButton_1,
                                    self.q2ChoiceRadioButton_2,
                                    self.q2ChoiceRadioButton_3,
                                    self.q2ChoiceRadioButton_4]
        for idx, radio in enumerate(question_2_choice_radios):
            radio.toggled.connect(
                set_answer_index(self.app_state.set_question_property, 1, 'correct_answer_index', idx)
            )

        self.q2ChoiceLineEdit_1.textEdited.connect(self.app_state.set_choice_text(1, 0))
        self.q2ChoiceLineEdit_2.textEdited.connect(self.app_state.set_choice_text(1, 1))
        self.q2ChoiceLineEdit_3.textEdited.connect(self.app_state.set_choice_text(1, 2))
        self.q2ChoiceLineEdit_4.textEdited.connect(self.app_state.set_choice_text(1, 3))

        # Question 3

        self.q3QuestionTextEdit.textChanged.connect(extract_text_area_value(self.q3QuestionTextEdit, self.process_text(
            self.q3QuestionTextEdit.id, 2, 'question_text')))
        self.q3AnswerTextEdit.textChanged.connect(extract_text_area_value(self.q3AnswerTextEdit,
                                                                          self.process_text(self.q3AnswerTextEdit.id, 2,
                                                                                            'answer_text')))
        self.q3ImageUrlLineEdit.textEdited.connect(self.app_state.set_question_property(2, 'answer_image'))
        self.q3ImageCaptionLineEdit.textEdited.connect(self.app_state.set_question_property(2,
                                                                                            'answer_image_caption'))
        question_3_choice_radios = [self.q3ChoiceRadioButton_1, self.q3ChoiceRadioButton_2, self.q3ChoiceRadioButton_3,
                                    self.q3ChoiceRadioButton_4]
        for idx, radio in enumerate(question_3_choice_radios):
            radio.toggled.connect(
                set_answer_index(self.app_state.set_question_property, 2, 'correct_answer_index', idx))

        self.q3ChoiceLineEdit_1.textEdited.connect(self.app_state.set_choice_text(2, 0))
        self.q3ChoiceLineEdit_2.textEdited.connect(self.app_state.set_choice_text(2, 1))
        self.q3ChoiceLineEdit_3.textEdited.connect(self.app_state.set_choice_text(2, 2))
        self.q3ChoiceLineEdit_4.textEdited.connect(self.app_state.set_choice_text(2, 3))

        # Question 4

        self.q4QuestionTextEdit.textChanged.connect(
            extract_text_area_value(self.q4QuestionTextEdit,
                                    self.process_text(self.q4QuestionTextEdit.id, 3, 'question_text')))
        self.q4AnswerTextEdit.textChanged.connect(extract_text_area_value(self.q4AnswerTextEdit,
                                                                          self.process_text(self.q4AnswerTextEdit.id, 3,
                                                                                            'answer_text')))
        self.q4ImageUrlLineEdit.textEdited.connect(self.app_state.set_question_property(3, 'answer_image'))
        self.q4ImageCaptionLineEdit.textEdited.connect(self.app_state.set_question_property(3, 'answer_image_caption'))
        question_4_choice_radios = [self.q4ChoiceRadioButton_1,
                                    self.q4ChoiceRadioButton_2,
                                    self.q4ChoiceRadioButton_3,
                                    self.q4ChoiceRadioButton_4]
        for idx, radio in enumerate(question_4_choice_radios):
            radio.toggled.connect(
                set_answer_index(self.app_state.set_question_property, 3, 'correct_answer_index', idx))

        self.q4ChoiceLineEdit_1.textEdited.connect(self.app_state.set_choice_text(3, 0))
        self.q4ChoiceLineEdit_2.textEdited.connect(self.app_state.set_choice_text(3, 1))
        self.q4ChoiceLineEdit_3.textEdited.connect(self.app_state.set_choice_text(3, 2))
        self.q4ChoiceLineEdit_4.textEdited.connect(self.app_state.set_choice_text(3, 3))

        # Question 5

        self.q5QuestionTextEdit.textChanged.connect(
            extract_text_area_value(self.q5QuestionTextEdit,
                                    self.process_text(self.q5QuestionTextEdit.id, 4, 'question_text')))
        self.q5AnswerTextEdit.textChanged.connect(extract_text_area_value(self.q5AnswerTextEdit,
                                                                          self.process_text(self.q5AnswerTextEdit.id, 4,
                                                                                            'answer_text')))
        self.q5ImageUrlLineEdit.textEdited.connect(self.app_state.set_question_property(4, 'answer_image'))
        self.q5ImageCaptionLineEdit.textEdited.connect(self.app_state.set_question_property(4, 'answer_image_caption'))
        question_5_choice_radios = [self.q5ChoiceRadioButton_1,
                                    self.q5ChoiceRadioButton_2,
                                    self.q5ChoiceRadioButton_3,
                                    self.q5ChoiceRadioButton_4]
        for idx, radio in enumerate(question_5_choice_radios):
            radio.toggled.connect(
                set_answer_index(self.app_state.set_question_property, 4, 'correct_answer_index', idx))

        self.q5ChoiceLineEdit_1.textEdited.connect(self.app_state.set_choice_text(4, 0))
        self.q5ChoiceLineEdit_2.textEdited.connect(self.app_state.set_choice_text(4, 1))
        self.q5ChoiceLineEdit_3.textEdited.connect(self.app_state.set_choice_text(4, 2))
        self.q5ChoiceLineEdit_4.textEdited.connect(self.app_state.set_choice_text(4, 3))

    def __update_trivia_list(self):
        trivia = self.app_state.get_trivia()
        current_index = self.listWidget.currentRow()
        self.listWidget.clear()
        if len(trivia.quizzes) == 0:
            self.app_state.clear_selected_quiz()
            return
        self.listWidget.setCurrentRow(0)
        for idx, quiz in enumerate(trivia.quizzes):
            list_item = QListWidgetItem(quiz.title)
            list_item.setData(1, quiz.id)
            self.listWidget.addItem(list_item)
            if self.app_state.get_selected_quiz() and quiz.id == self.app_state.get_selected_quiz().id:
                self.listWidget.setCurrentRow(idx)

    def __select_quiz(self):
        quiz_id = self.listWidget.currentItem().data(1)
        if quiz_id is None:
            return
        if self.app_state.is_dirty and self.app_state.get_selected_quiz() is not None:
            reply = QMessageBox.question(self, 'Message',
                                         "You have unsaved changes. Do you want to save them?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                if self.opened_file_name:
                    self.save_file()
                else:
                    self.save_file_as()
        self.disconnect_selected_quiz_signal_slots()
        self.app_state.set_selected_quiz_by_id(quiz_id)
        self.connect_selected_quiz_signal_slots()

    def __add_new_quiz(self):
        first_friday = self.app_state.get_trivia().get_first_available_friday().strftime("%Y/%m/%d")
        quiz = Quiz(title="New Quiz", subtitle="", publish_date=first_friday, author="", questions=[])
        self.app_state.add_quiz(quiz)

    def __create_new_trivia(self):
        new_trivia = Trivia(quizzes=[Quiz(title="New Quiz")])
        self.app_state.set_trivia(new_trivia)
        self.opened_file_name = None
        self.listWidget.setCurrentRow(0)

    def __delete_selected_quiz(self):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure you want to delete this quiz: " + self.app_state.get_selected_quiz().title + "?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            quiz_id = self.app_state.get_selected_quiz().id
            self.app_state.delete_quiz(quiz_id)
            self.save_file()

    def __load_file(self, file_name):
        print("Loading File " + file_name)
        try:
            with open(file_name) as json_file:
                data = json.load(json_file)
                trivia = Trivia.from_json(data)
                self.listWidget.setCurrentRow(0)
                self.app_state.set_trivia(trivia)
                self.app_state.set_dirty(False)

            self.opened_file_name = file_name
        except Exception as e:
            QMessageBox.about(self, "Error", "That does not look like a valid Trail Trivia file\n\n " + str(e))
            self.app_config.remove_recent_file(file_name)
            return
        print("File Opened " + file_name)
        self.app_config.add_recent_file(file_name)

    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self,
                                                   "QFileDialog.getOpenFileName()",
                                                   "",
                                                   "JSON Files (*.json)",
                                                   options=options)
        if file_name:
            self.__load_file(file_name)

    def __preview_quiz(self):
        quiz = Quiz.clone(self.app_state.get_selected_quiz())
        quiz.publish_date = datetime.now().strftime("%Y/%m/%d")
        preview_trivia = Trivia([quiz])
        preview_trivia_json = preview_trivia.to_json()
        preview_quiz(preview_trivia_json)

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
            print("Saved As to " + full_path)

    def save_file(self):
        if self.opened_file_name is not None:
            if self.app_state.is_dirty:
                self.app_state.update_trivia_with_selected_quiz()
            trivia_data = self.app_state.get_trivia().to_json()
            with open(self.opened_file_name, 'w') as outfile:
                json.dump(trivia_data, outfile)
                outfile.close()
            self.app_state.set_dirty(False)
            print("Saved to " + self.opened_file_name)

    def __deploy_trivia(self):
        # create temp directory if it doesn't exist
        temp_file_path = os.path.dirname(os.path.realpath(__file__)) + '/../data/temp'
        if not os.path.exists(temp_file_path):
            os.makedirs(temp_file_path)

        # clean file and save
        if self.app_state.is_dirty:
            self.app_state.update_trivia_with_selected_quiz()
            self.app_state.set_dirty(False)
        trivia_data = self.app_state.get_trivia().to_json()
        if self.opened_file_name is not None:
            self.save_file()
        else:
            self.save_file_as()

        # save file to temp directory
        try:
            with open(temp_file_path + "/trivia.json", 'w') as outfile:
                json.dump(trivia_data, outfile)
                outfile.close()
        except Exception as e:
            QMessageBox.about(self, "Error",
                              "<p>Unable to save trivia data to:" + temp_file_path + "</p><p>" + str(e) + "</p>")

        # upload file to server

        print("Uploading to server")
        self.upload.push_to_server(temp_file_path)

    def __display_selected_quiz(self):
        quiz = self.app_state.get_selected_quiz()
        if quiz:
            title = quiz.title
            self.titleLineEdit.setText(title)
            self.subtitleLineEdit.setText(quiz.subtitle)
            self.publishOnDateEdit.setDate(QDate.fromString(quiz.publish_date, 'yyyy/MM/dd'))
            self.authorLineEdit.setText(quiz.author)
            # Update Question 1
            self.q1QuestionTextEdit.setPlainText(quiz.questions[0].question_text)
            self.q1AnswerTextEdit.setPlainText(quiz.questions[0].answer_text)
            self.q1ImageUrlLineEdit.setText(quiz.questions[0].answer_image)
            self.q1ImageCaptionLineEdit.setText(quiz.questions[0].answer_image_caption)
            self.q1ChoiceLineEdit_1.setText(quiz.questions[0].choices[0].text)
            self.q1ChoiceLineEdit_2.setText(quiz.questions[0].choices[1].text)
            self.q1ChoiceLineEdit_3.setText(quiz.questions[0].choices[2].text)
            self.q1ChoiceLineEdit_4.setText(quiz.questions[0].choices[3].text)
            [self.q1ChoiceRadioButton_1, self.q1ChoiceRadioButton_2, self.q1ChoiceRadioButton_3,
             self.q1ChoiceRadioButton_4][quiz.questions[0].correct_answer_index].setChecked(True)
            # Update Question 2
            self.q2QuestionTextEdit.setPlainText(quiz.questions[1].question_text)
            self.q2AnswerTextEdit.setPlainText(quiz.questions[1].answer_text)
            self.q2ImageUrlLineEdit.setText(quiz.questions[1].answer_image)
            self.q2ImageCaptionLineEdit.setText(quiz.questions[1].answer_image_caption)
            self.q2ChoiceLineEdit_1.setText(quiz.questions[1].choices[0].text)
            self.q2ChoiceLineEdit_2.setText(quiz.questions[1].choices[1].text)
            self.q2ChoiceLineEdit_3.setText(quiz.questions[1].choices[2].text)
            self.q2ChoiceLineEdit_4.setText(quiz.questions[1].choices[3].text)
            [self.q2ChoiceRadioButton_1, self.q2ChoiceRadioButton_2, self.q2ChoiceRadioButton_3,
             self.q2ChoiceRadioButton_4][quiz.questions[1].correct_answer_index].setChecked(True)
            # Update Question 3
            self.q3QuestionTextEdit.setPlainText(quiz.questions[2].question_text)
            self.q3AnswerTextEdit.setPlainText(quiz.questions[2].answer_text)
            self.q3ImageUrlLineEdit.setText(quiz.questions[2].answer_image)
            self.q3ImageCaptionLineEdit.setText(quiz.questions[2].answer_image_caption)
            self.q3ChoiceLineEdit_1.setText(quiz.questions[2].choices[0].text)
            self.q3ChoiceLineEdit_2.setText(quiz.questions[2].choices[1].text)
            self.q3ChoiceLineEdit_3.setText(quiz.questions[2].choices[2].text)
            self.q3ChoiceLineEdit_4.setText(quiz.questions[2].choices[3].text)
            [self.q3ChoiceRadioButton_1, self.q3ChoiceRadioButton_2, self.q3ChoiceRadioButton_3,
             self.q3ChoiceRadioButton_4][quiz.questions[2].correct_answer_index].setChecked(True)
            # Update Question 4
            self.q4QuestionTextEdit.setPlainText(quiz.questions[3].question_text)
            self.q4AnswerTextEdit.setPlainText(quiz.questions[3].answer_text)
            self.q4ImageUrlLineEdit.setText(quiz.questions[3].answer_image)
            self.q4ImageCaptionLineEdit.setText(quiz.questions[3].answer_image_caption)
            self.q4ChoiceLineEdit_1.setText(quiz.questions[3].choices[0].text)
            self.q4ChoiceLineEdit_2.setText(quiz.questions[3].choices[1].text)
            self.q4ChoiceLineEdit_3.setText(quiz.questions[3].choices[2].text)
            self.q4ChoiceLineEdit_4.setText(quiz.questions[3].choices[3].text)
            [self.q4ChoiceRadioButton_1, self.q4ChoiceRadioButton_2, self.q4ChoiceRadioButton_3,
             self.q4ChoiceRadioButton_4][quiz.questions[3].correct_answer_index].setChecked(True)
            # Update Question 5
            self.q5QuestionTextEdit.setPlainText(quiz.questions[4].question_text)
            self.q5AnswerTextEdit.setPlainText(quiz.questions[4].answer_text)
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

    def __bind_recent_file(self, file_name):
        return lambda: self.__load_file(file_name)

    def __set_window_dimensions(self):
        print('SETTING WINDOW PREFS')
        print(str(self.app_config))
        match self.app_config.window_mode:
            case AppConfig.window_modes.MAXIMIZED:
                self.setWindowState(Qt.WindowMaximized)
            case AppConfig.window_modes.FULLSCREEN:
                self.setWindowState(Qt.WindowFullScreen)
            case AppConfig.window_modes.WINDOWED:
                self.setWindowState(Qt.WindowNoState)
                self.resize(self.app_config.window_width, self.app_config.window_height)
            case _:
                pass

        self.splitter.setSizes(self.app_config.splitter_position)

    def __display_recent_files(self):
        recent_file_actions = [self.actionrecent_file_01, self.actionrecent_file_02, self.actionrecent_file_03,
                               self.actionrecent_file_04, self.actionrecent_file_05, self.actionrecent_file_06,
                               self.actionrecent_file_07, self.actionrecent_file_08, self.actionrecent_file_09]
        has_recent_files = self.app_config.get_recent_files() is not None and len(
            self.app_config.get_recent_files()) > 0
        print('Has Recent Files: ' + str(has_recent_files))
        self.menuRecent_Files.setEnabled(has_recent_files)
        for i in range(len(recent_file_actions)):
            file_name = self.app_config.get_recent_file_name(i)
            recent_file_action = recent_file_actions[i]

            if file_name is not None:
                recent_file_action.triggered.connect(self.__bind_recent_file(file_name))
                recent_file_action.setText(file_name)
                recent_file_action.setVisible(True)
            else:
                recent_file_action.setVisible(False)

    def __set_menu_state(self):
        has_quizzes = len(self.app_state.get_trivia().quizzes) > 0
        self.actionNew_Quiz.setEnabled(has_quizzes)
        self.actionSave.setEnabled(self.app_state.is_dirty)
        self.actionSave_As.setEnabled(has_quizzes)
        self.actionAnalyze.setEnabled(has_quizzes)
        self.actionDeploy.setEnabled(has_quizzes)
        self.scrollAreaWidgetContents_1.setEnabled(has_quizzes)
        quiz_is_selected = self.app_state.get_selected_quiz() is not None
        self.actionRemove_Quiz.setEnabled(quiz_is_selected)
        self.scrollAreaWidgetContents_2.setEnabled(quiz_is_selected)
        self.actionPreview.setEnabled(quiz_is_selected)
        self.actionDeploy.setEnabled(has_quizzes)

    def __set_settings(self):
        dialog = PrefsDialog(self.app_config.to_dict())
        result = dialog.exec_()
        if result == 1:
            print("CHANGE SETTINGS")

    def about(self):
        QMessageBox.about(
            self,
            "About Kwiz Kreator",
            "<p>An editor for creating Trail Trivia files.</p>"
            "<p>Play Trail Trivia at:</p>"
            "<p><a src='https://gmcburlington.org/trail-trivia/'>https://gmcburlington.org/trail-trivia/</a></p>"
        )

    def __alert_file_deployed(self):
        QMessageBox.about(
            self,
            "Trivia Uploaded",
            "<p>Your trivia has been uploaded to the server.</p>"
        )
