import json
import uuid

from .choice import Choice



class Question:
    def __init__(self, question_text="", choices=None, tags=None, answer_index=0, answer_text="", answer_image="",
                 answer_image_caption="",
                 id_=None):
        if tags is None:
            tags = []
        if choices is None:
            choices = []
        self.id_ = id_ or uuid.uuid4()
        self.tags = tags
        self.question_text = question_text
        self.choices = (choices + [Choice() for i in range(4)])[0:4]
        self.answer_index = answer_index or 0
        self.answer_text = answer_text or ''
        self.answer_image = answer_image or ''
        self.answer_image_caption = answer_image_caption or ''

    def to_json(self):
        question = {
            'id': self.id_,
            'tags': self.tags,
            'questionText': self.question_text,
            'choices': self.choices,
            'answerIndex': self.answer_index,
            'answerText': self.answer_text,
            'answerImage': self.answer_image,
            'answerImageCaption': self.answer_image_caption
        }

        return json.dumps(question)

    @staticmethod
    def from_json(question):
        return Question(question.get('questionText', ''),
                        [Choice.from_json(c) for c in question['choices']],
                        question.get('tags', []),
                        question.get('answerIndex', 0),
                        question.get('answerText', ''),
                        question.get('answerImage', ''),
                        question.get('answerImageCaption', ''),
                        question.get('id', None))

    def __str__(self):
        return f'Question: {self.id_} - {self.question_text}'

    def __repr__(self):
        return f'Question(  question_text={self.question_text}, choices={self.choices}, tags={self.tags}, ' \
               f'answer_index={self.answer_index}, answer_text={self.answer_text}, answer_image={self.answer_image}, ' \
               f'answer_image_caption={self.answer_image_caption}, id_={self.id_})'
