import uuid

from PyQt5.QtCore import QEvent, Qt, pyqtSlot
from PyQt5.QtGui import QContextMenuEvent, QMouseEvent, QTextCursor, QTextCharFormat
from PyQt5.QtWidgets import QMenu, QTextEdit
from toolz import curry
from .correction_action import SpecialAction
from .highlighter import GrammarCheckHighlighter
from ..lib.grammar_checker import GrammarChecker, GrammarMatch


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
        match message.type:
            case "MATCHES_FOUND":
                if self.id == message.id:
                    self.highlighter.matches = message.matches
                    self.highlighter.highlightBlock(self.toPlainText())
            case _:
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
        start = text_cursor.selectionStart()

        if word_to_check != "":
            match = next((m for m in self.highlighter.matches if m.offset == start), None)
            if match is not None and match.suggestions is not None and len(match.suggestions) > 0:
                self.contextMenu.addSeparator()
                self.contextMenu.addMenu(self.create_suggestions_menu(match))

        self.contextMenu.exec_(event.globalPos())

    def create_suggestions_menu(self, match: GrammarMatch):
        suggestions_menu = QMenu("Change to", self)
        suggestions = match.suggestions
        for word in suggestions:
            action = SpecialAction(word, self.contextMenu)
            action.actionTriggered.connect( self.correct_word(match))
            suggestions_menu.addAction(action)

        return suggestions_menu

    @pyqtSlot(str)
    @curry
    def correct_word(self, match, word):
        text_cursor = self.textCursor()
        text_cursor.beginEditBlock()
        text_cursor.removeSelectedText()
        text_cursor.insertText(word)
        text_cursor.endEditBlock()
        match_index = next((index for (index, m) in enumerate(self.highlighter.matches) if m.id == match.id), None)
        len_diff = len(word) - match.length
        corrected = [GrammarMatch(m.context, m.offset + len_diff, m.length, m.ruleId, m.message, m.suggestions) for
                     m in self.highlighter.matches]
        self.highlighter.matches = self.highlighter.matches[0:match_index] + corrected[match_index + 1:]
        self.highlighter.rehighlight()
