import language_tool_python
from spellchecker import SpellChecker


class SpellCheckWrapper:

    def __init__(self):
        self.spell = SpellChecker()
        self.grammar_tool = language_tool_python.LanguageToolPublicAPI('en-US')

    def matches(self, text: str) -> list[str]:
        return self.grammar_tool.check(text)

    def suggestions(self, word: str) -> list[str] | None:
        corrections = self.spell.candidates(word)
        return corrections if corrections else None

    def correction(self, word: str) -> str | None:
        corrections = self.spell.candidates(word)
        return corrections[0] if corrections else None

    def check(self, word: str) -> bool:
        return word in self.spell
