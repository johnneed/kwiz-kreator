import json
import uuid
from .quiz import Quiz


class Trivia:
    def __init__(self, quizzes=[], id_=None):
        self.id_ = id_ or uuid.uuid4()
        self.quizzes = quizzes

    def to_json(self):
        trivia = {
            'id': self.id_,
            'quizzes': [q.to_json() for q in self.quizzes]
        }

        return json.dumps(trivia)

    @staticmethod
    def from_json(trivia):
        quizzes = [Quiz.from_json(q) for q in trivia['quizzes']]
        _id = trivia.get('id', None)
        return Trivia(quizzes, _id)

    def __str__(self):
        return f'Trivia: {self.id_}'

    def __repr__(self):
        return f'Trivia(title={self.quizzes}, id_={self.id_})'
