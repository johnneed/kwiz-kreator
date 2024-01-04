from spellchecker import SpellChecker


class SpellCheckWrapper:

    def __init__(self):
        self.spell = SpellChecker()

    def suggestions(self, word: str) -> list[str] | None:
        corrections = self.spell.candidates(word)
        print("corrections: ", corrections)
        return corrections if corrections else None

    def correction(self, word: str) -> str | None:
        corrections = self.spell.candidates(word)
        print("correction: ", corrections)
        return corrections[0] if corrections else None

    def check(self, word: str) -> bool:
        return word in self.spell
