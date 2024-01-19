import uuid

from PyQt5.QtCore import QEvent, Qt, pyqtSlot
from PyQt5.QtGui import QContextMenuEvent, QMouseEvent, QTextCursor, QTextCharFormat
from PyQt5.QtWidgets import QMenu, QTextEdit

from .correction_action import SpecialAction
from .highlighter import GrammarCheckHighlighter
from ..lib.grammar_checker import GrammarChecker


class SpellTextEdit(QTextEdit):
    def __init__(self, *args):
        if args and type(args[0]) == GrammarChecker:
            super().__init__(*args[1:])
            self.grammar_checker = args[0]
            self.id = str(uuid.uuid4())
            self.grammar_checker.subscribe(self)

        else:
            super().__init__(*args)

        self.highlighter = GrammarCheckHighlighter(self.document())
        self.highlighter.errorFormat.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
        self.highlighter.errorFormat.setUnderlineColor(Qt.red)

    def receive(self, message):
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!ID: ' + self.id + ' Received Message: ' + str(message))
        match message.type:
            case "MATCHES_FOUND":
                if self.id == message.id:
                    self.highlighter.matches = message.matches
                    self.highlighter.highlightBlock(self.toPlainText())
            case _:
                print("PASSING")
                pass

    def set_grammar_checker(self, grammar_checker):
        self.grammar_checker = grammar_checker
        self.grammar_checker.subscribe(self)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.RightButton:
            event = QMouseEvent(
                QEvent.MouseButtonPress,
                event.pos(),
                Qt.LeftButton,
                Qt.LeftButton,
                Qt.NoModifier,
            )
        super().mousePressEvent(event)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        self.contextMenu = self.createStandardContextMenu(event.pos())
        text_cursor = self.textCursor()
        text_cursor.select(QTextCursor.WordUnderCursor)
        self.setTextCursor(text_cursor)
        word_to_check = text_cursor.selectedText()
        if word_to_check != "":
            suggestions = self.speller.suggestions(word_to_check)

            if suggestions is not None and len(suggestions) > 0:
                self.contextMenu.addSeparator()
                self.contextMenu.addMenu(self.create_suggestions_menu(suggestions))

        self.contextMenu.exec_(event.globalPos())

    def create_suggestions_menu(self, suggestions: list[str]):
        suggestions_menu = QMenu("Change to", self)
        for word in suggestions:
            action = SpecialAction(word, self.contextMenu)
            action.actionTriggered.connect(self.correct_word)
            suggestions_menu.addAction(action)

        return suggestions_menu

    @pyqtSlot(str)
    def correct_word(self, word: str):
        text_cursor = self.textCursor()
        text_cursor.beginEditBlock()
        text_cursor.removeSelectedText()
        text_cursor.insertText(word)
        text_cursor.endEditBlock()

