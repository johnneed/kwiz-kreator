import json
import uuid


class Choice:
    def __init__(self, text="", id_=None):
        self.id_ = id_ or uuid.uuid4()
        self.text = text or ''

    def to_json(self):
        choice = {
            'id': self.id_,
            'text': self.text,
        }

        return json.dumps(choice)

    @staticmethod
    def from_json(choice):
        return Choice(
            choice.get('text', ""),
            choice.get('id', None)
        )

    def __str__(self):
        return f'Choice {self.id_} - {self.text}'

    def __repr__(self):
        return f'Choice(text={self.text}, id_={self.id_})'
