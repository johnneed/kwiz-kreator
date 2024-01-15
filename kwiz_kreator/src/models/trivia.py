from datetime import datetime, timedelta
import json
import uuid
from .quiz import Quiz


class Trivia:
    def __init__(self, quizzes=[], id_=None):
        self._id = id_ or str(uuid.uuid4())
        self._quizzes = quizzes
        self.sort_quizzes()
    @property
    def quizzes(self):
        return self._quizzes

    @quizzes.setter
    def quizzes(self, quizzes):
        self._quizzes = quizzes
        self.sort_quizzes()

    @property
    def id(self):
        return self._id

    def to_json(self):
        return {
            'id': self._id,
            'quizzes': [q.to_json() for q in self.quizzes]
        }

    @staticmethod
    def from_json(trivia):
        quizzes = [Quiz.from_json(q) for q in trivia['quizzes']]
        _id = trivia.get('id', None)
        return Trivia(quizzes, _id)

    def get_first_available_friday(self):
        publish_dates = [q.publish_date for q in self.quizzes]
        my_friday = datetime.now().date() + timedelta((4 - datetime.now().weekday()) % 7)
        while my_friday.strftime("%Y/%m/%d") in publish_dates:
            my_friday += timedelta(7)
        return my_friday

    def sort_quizzes(self):
        self.quizzes.sort(reverse=True, key=lambda q: q.publish_date)
    def __str__(self):
        return f'Trivia(title="{self.quizzes}", id_="{self._id}")'

    def __repr__(self):
        return f'Trivia(title="{self.quizzes}", id_="{self._id}")'
