import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat


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

    def highlightBlock(self, text: str) -> None:
        for match in self._matches:
            self.setFormat(
                match.offset,
                match.length,
                self.errorFormat,
            )
