import json

from PyQt5.QtWidgets import (
    QMainWindow, QMessageBox, QFileDialog
)

from .models import Trivia
from .state import TriviaState, SelectedQuizState
from .ui import Ui_MainWindow


# from autocorrect import Speller
class App(QMainWindow, Ui_MainWindow):

    # spell = Speller(lang='en')
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        self.trivia_state = TriviaState()
        self.selected_quiz_state = SelectedQuizState()
        self.subscribe()

    def receive(self, message):
        match message:
            case "trivia_loaded":
                self.__update_trivia_list()
            case "trivia_updated":
                pass
            case "quiz_selected":
                self.selected_quiz_state.set_quiz(self.trivia_state.get_selected_quiz())
            case "quiz_updated":
                pass
            case "selected_quiz_dirty_status_changed":
                pass
            case "trivia_dirty_status_changed":
                pass
            case _:
                pass

    def __update_trivia_list(self):
        trivia = self.trivia_state.get_trivia()
        self.listWidget.clear()
        if len(trivia.quizzes) > 0:
            for quiz in trivia.quizzes:
                self.listWidget.addItem(quiz.title)
            self.listWidget.setCurrentRow(0)
            self.trivia_state.set_selected_quiz_id(trivia.quizzes[0].id_)
        else:
            self.trivia_state.set_selected_quiz_id(None)


    def __select_quiz(self, index):
        self.trivia_state.set_selected_quiz_id(self.trivia.quizzes[index].id_)

    def subscribe(self):
        self.trivia_state.subscribe(self)
        self.selected_quiz_state.subscribe(self)

    def connectSignalsSlots(self):
        self.actionOpen.triggered.connect(self.open_file)
        # self.action_Exit.triggered.connect(self.close)
        # self.action_Find_Replace.triggered.connect(self.findAndReplace)
        # self.action_About.triggered.connect(self.about)

    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self,
                                                   "QFileDialog.getOpenFileName()",
                                                   "",
                                                   "JSON Files (*.json)",
                                                   options=options)
        if file_name:
            with open(file_name) as json_file:
                data = json.load(json_file)
                trivia = Trivia.from_json(data)
                self.trivia_state.set_trivia(trivia)

    def about(self):
        QMessageBox.about(
            self,
            "About Kwiz Kreator",
            "<p>A UI for creating Trail Trivia files</p>"
            "<p>Play Trail Trivia at https://gmcburlington.org/trail-trivia/</p>"
        )
