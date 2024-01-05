from PyQt5.QtCore import QEvent, Qt, pyqtSlot
from PyQt5.QtGui import QContextMenuEvent, QMouseEvent, QTextCursor
from PyQt5.QtWidgets import QMenu, QTextEdit

from .correction_action import SpecialAction
from .highlighter import SpellCheckHighlighter
from .spell_check_wrapper import SpellCheckWrapper


class SpellTextEdit(QTextEdit):
    def __init__(self, *args):
        if args and type(args[0]) == SpellCheckWrapper:
            super().__init__(*args[1:])
            self.speller = args[0]
        else:
            super().__init__(*args)

        self.highlighter = SpellCheckHighlighter(self.document())
        if hasattr(self, "speller"):
            self.highlighter.setSpeller(self.speller)

    def set_speller(self, speller):
        self.speller = speller
        self.highlighter.setSpeller(self.speller)

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
