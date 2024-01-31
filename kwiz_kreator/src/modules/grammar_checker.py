import queue
import uuid
from dataclasses import dataclass
from functools import lru_cache
from threading import Thread
import language_tool_python

from ..modules.decorators import debounce


@dataclass
class GrammarMatch:
    id: str
    context: str
    offset: int
    length: int
    ruleId: str
    message: str
    suggestions: list[str]

    def __init__(self, context: str, offset: int, length: int, ruleId: str, message: str, suggestions: list[str]):
        self.id = str(uuid.uuid4())
        self.context = context
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
        context = match.context
        return GrammarMatch(context, offset, length, ruleId, message, suggestions)

    def __str__(self):
        return "Context: " + str(self.context) + ", Offset: " + str(self.offset) + ", length: " + str(
            self.length) + ", ruleId: " + self.ruleId + ", message: " + self.message + ", suggestions: " + str(
            self.suggestions)

    def __repr__(self):
        return "GrammarMatch(" + str(self.context) + ", " + str(self.offset) + ", " + str(
            self.length) + ", " + self.ruleId + ", " + \
            self.message + ", " + repr(self.suggestions) + ")"


@dataclass
class GrammarMessage:
    _id: str
    _matches: list[GrammarMatch]
    _control_id: str
    _type: str

    def __init__(self, matches: list[GrammarMatch], _control_id: str, _message_type: str):
        self._id = str(uuid.uuid4())
        self._matches = matches
        self._control_id = _control_id
        self._message_type = _message_type


    @property
    def id(self):
        return self._id

    @property
    def matches(self):
        return self._matches

    @matches.setter
    def matches(self, value: list[GrammarMatch]):
        self._matches = value

    @property
    def control_id(self):
        return self._control_id

    @control_id.setter
    def control_id(self, value: uuid.UUID):
        self._control_id = value

    @property
    def message_type(self):
        return self._message_type

    @message_type.setter
    def message_type(self, value: str):
        self._message_type = value

    def __str__(self):
        return "Message Type: " + str(self._message_type) + ", Control ID: " + str(
            self._control_id) + ", Matches: " + str(self._matches)

    def __repr__(self):
        return "GrammarMessage(" + str(self._matches) + ", " + str(self._control_id) + ", " + str(
            self._message_type) + ")"


class GrammarChecker:

    def __init__(self):
        self.message_queue = queue.Queue()
        self.subscribers = []
        self._is_initiated = False
        thread = Thread(target=self.__init_grammar_tool)
        thread.start()

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def publish(self, message):
        self.message_queue.put(message)
        for subscriber in self.subscribers:
            subscriber.receive(message)

    @property
    def is_initiated(self):
        return self._is_initiated

    def __init_grammar_tool(self):
        print("INITIATING GRAMMAR TOOL")
        self.grammar_tool = language_tool_python.LanguageToolPublicAPI('en-US')
        self._is_initiated = True

    def __find_matches(self, control_id: str, text: str):
        matches = self.__fetch_matches(text)
        if matches is None or len(matches) < 1:
            return
        self.publish(GrammarMessage(matches, control_id, "MATCHES_FOUND"))

    @lru_cache(maxsize=128)
    def __fetch_matches(self, text: str):
        print("FETCH MATCHES")
        matches = self.grammar_tool.check(text)
        print(str(matches))
        my_matches = [GrammarMatch.parse_match(match) for match in matches]
        return my_matches

    @debounce(1)
    def match(self, control_id: str, text) -> None:
        if len(text) > 1:
            print("CHECK FOR GRAMMAR ERRORS: " + text)
            self.__find_matches(control_id, text)
            # thread = Thread(target=self.__find_matches, args=(control_id, text))
            # thread.start()
