import json
import uuid
from datetime import datetime

from .question import Question


class Quiz:
    def __init__(self, title="", sub_title="", publish_date=None, author="", questions=None, id_=None):
        if questions is None:
            questions = []
        self.id_ = id_ or uuid.uuid4()
        self.title = title
        self.sub_title = sub_title
        self.publish_date = publish_date or datetime.now().strftime("%Y/%m/%d")
        self.author = author or ""
        self.questions = (questions + [Question() for i in range(5)])[0:5]

    def to_json(self):
        quiz = {
            'id': self.id_,
            'title': self.title,
            'subTitle': self.sub_title,
            'publishDate': self.publish_date,
            'author': self.author,
            'questions': [q.to_json() for q in self.questions]
        }

        return json.dumps(quiz)

    @staticmethod
    def from_json(quiz):
        return Quiz(
            quiz.get('title', ''),
            quiz.get('subTitle', ''),
            quiz.get('publishDate', ''),
            quiz.get('author', ''),
            [Question.from_json(q) for q in quiz['questions']],
            quiz.get('id', None)
        )

    def __str__(self):
        return f'Quiz: {self.id_} - {self.title}'

    def __repr__(self):
        return f'Quiz(title={self.title}, subTitle={self.sub_title}, publishDate={self.publish_date}, ' \
               f'author={self.author}, questions={self.questions}, id_={self.id_})'
