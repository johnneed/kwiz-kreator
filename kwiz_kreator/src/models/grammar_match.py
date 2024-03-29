from dataclasses import dataclass


@dataclass
class GrammarMatch:
    offset: int
    length: int
    ruleId: str
    message: str
    suggestions: list[str]

    def __init__(self, offset: int, length: int, ruleId: str, message: str, suggestions: list[str]):
        self.offset = offset
        self.length = length
        self.ruleId = ruleId
        self.message = message
        self.suggestions = suggestions

    @staticmethod
    def parse_match(match: object):
        if match is None:
            return GrammarMatch(0, 0, "", "", [])
        offset = match.offset
        length = match.errorLength
        ruleId = match.ruleId
        message = match.message
        suggestions = match.replacements
        print("Offset: " + str(offset) + ", length: " + str(
            length) + ", ruleId: " + ruleId + ", message: " + message + ", suggestions: " + str(suggestions))
        return GrammarMatch(offset, length, ruleId, message, suggestions)

    def __str__(self):
        return "Offset: " + str(self.offset) + ", length: " + str(
            self.length) + ", ruleId: " + self.ruleId + ", message: " + self.message + ", suggestions: " + str(
            self.suggestions)

    def __repr__(self):
        return "Offset: " + str(self.offset) + ", length: " + str(
            self.length) + ", ruleId: " + self.ruleId + ", message: " + self.message + ", suggestions: " + str(
            self.suggestions)
