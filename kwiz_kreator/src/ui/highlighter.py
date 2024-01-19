import re
import uuid
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat
from .spell_check_wrapper import SpellCheckWrapper

class SpellCheckHighlighter(QSyntaxHighlighter):
    wordRegEx = re.compile(r"\b([A-Za-z]{2,})\b")

    def highlightBlock(self, text: str) -> None:
        if not hasattr(self, "speller"):
            return

        self.misspelledFormat = QTextCharFormat()
        self.misspelledFormat.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
        self.misspelledFormat.setUnderlineColor(Qt.red)

        for word_object in self.wordRegEx.finditer(text):
            if not self.speller.check(word_object.group()):
                self.setFormat(
                    word_object.start(),
                    word_object.end() - word_object.start(),
                    self.misspelledFormat,
                )

    def setSpeller(self, speller: SpellCheckWrapper):
        self.speller = speller


class GrammarCheckHighlighter(QSyntaxHighlighter):
    def __init__(self, *args):
        super(GrammarCheckHighlighter, self).__init__(*args)
        self._matches = []
        self._errorFormat = QTextCharFormat()

    @property
    def matches(self):
        return self._matches

    @matches.setter
    def matches(self, value):
        self._matches = value

    @property
    def errorFormat(self):
        return self._errorFormat

    @errorFormat.setter
    def errorFormat(self, value):
        self._errorFormat = value


    def get_suggestions(self, word):
        return self.speller.suggestions(word)

    def highlightBlock(self, text: str) -> None:

        for match in self._matches:
            self.setFormat(
                match.offset,
                match.length,
                self.errorFormat,
            )

