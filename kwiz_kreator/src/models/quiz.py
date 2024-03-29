import uuid
from datetime import datetime

from .question import Question


class Quiz:
    def __init__(self, title="", subtitle="", publish_date=None, author="", questions=None, id_=None):
        self.question_count = 5
        if id_ is None:
            id_ = str(uuid.uuid4())
        if questions is None:
            questions = []
        if publish_date is None:
            publish_date = datetime.now().strftime("%Y/%m/%d")
        self._id = id_
        self._title = title
        self._subtitle = subtitle
        self._publish_date = publish_date
        self._author = author
        self._questions = questions + [Question()] * (self.question_count - len(questions))

    @property
    def question_count(self):
        return self._question_count

    @question_count.setter
    def question_count(self, question_count: int):
        if question_count < 1:
            raise ValueError("question_count must be greater than 0")
        self._question_count = question_count


    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def subtitle(self):
        return self._subtitle

    @subtitle.setter
    def subtitle(self, subtitle):
        self._subtitle = subtitle

    @property
    def publish_date(self):
        return self._publish_date

    @publish_date.setter
    def publish_date(self, publish_date):
        self._publish_date = publish_date

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, author):
        self._author = author

    @property
    def questions(self):
        return self._questions

    @questions.setter
    def questions(self, questions):
        my_questions = [q if isinstance(q, Question) else Question.from_json(q) for q in questions][
                       :self.question_count]
        self._questions = my_questions + [Question()] * (self.question_count - len(my_questions))

    def to_json(self):
        return {
            'id': self._id,
            'title': self._title,
            'subtitle': self._subtitle,
            'publishDate': self._publish_date,
            'author': self._author,
            'questions': [q.to_json() for q in self._questions]
        }

    @staticmethod
    def from_json(quiz):
        return Quiz(
            quiz.get('title', ''),
            quiz.get('subtitle', ''),
            quiz.get('publishDate', ''),
            quiz.get('author', ''),
            [Question.from_json(q) for q in quiz['questions']],
            quiz.get('id', None)
        )

    @staticmethod
    def clone(quiz):
        return Quiz(
            quiz.title,
            quiz.subtitle,
            quiz.publish_date,
            quiz.author,
            [Question.clone(q) for q in quiz.questions],
            quiz.id
        )

    def __str__(self):
        return f'Quiz(title="{self._title}", subtitle="{self._subtitle}", publish_date="{self._publish_date}", ' \
               f'author="{self._author}", questions="{self._questions}", id_="{self._id}")'

    def __repr__(self):
        return f'Quiz(title="{self._title}", subtitle="{self._subtitle}", publish_date="{self._publish_date}", ' \
               f'author="{self._author}", questions="{self._questions}", id_="{self._id}")'
