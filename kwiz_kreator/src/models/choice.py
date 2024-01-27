import uuid


class Choice:
    def __init__(self, text="", id_=None):
        if id_ is None:
            id_ = str(uuid.uuid4())
        self._id = id_
        self._text = text

    @property
    def id(self):
        return self._id

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    def to_json(self):
        return{
            'id': self._id,
            'text': self._text,
        }

    @staticmethod
    def from_json(choice):
        return Choice(
            choice.get('text', ""),
            choice.get('id', None)
        )

    @staticmethod
    def clone(choice):
        return Choice(
            choice.text,
            choice.id
        )
    def __str__(self):
        return f'Choice {self._id} - {self._text}'

    def __repr__(self):
        return f'Choice(text="{self._text}", id_="{self._id}")'
