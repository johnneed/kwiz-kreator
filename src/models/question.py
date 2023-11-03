import json
import uuid

from .choice import Choice


class Question:
    def __init__(self, question_text="", choices=None,  tags=None, correct_answer_index=0, answer_text="",
                 answer_image="", answer_image_caption="", id_=None):
        if id_ is None:
            id_ = str(uuid.uuid4())
        if tags is None:
            tags = []
        if choices is None:
            choices = []
        self._id = id_
        self._tags = tags
        self._question_text = question_text
        self._correct_answer_index = correct_answer_index
        self._choices = choices + [Choice()] * (4 - len(choices))
        self._answer_text = answer_text
        self._answer_image = answer_image
        self._answer_image_caption = answer_image_caption



    @property
    def id(self):
        return self._id

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, tags):
        self._tags = tags

    @property
    def question_text(self):
        return self._question_text

    @question_text.setter
    def question_text(self, question_text):
        self._question_text = question_text

    @property
    def choices(self):
        return self._choices

    @choices.setter
    def choices(self, choices):
        self._choices = choices

    @property
    def correct_answer_index(self):
        return self._correct_answer_index

    @correct_answer_index.setter
    def correct_answer_index(self, correct_answer_index):
        self._correct_answer_index = correct_answer_index

    @property
    def answer_text(self):
        return self._answer_text

    @answer_text.setter
    def answer_text(self, answer_text):
        self._answer_text = answer_text

    @property
    def answer_image(self):
        return self._answer_image

    @answer_image.setter
    def answer_image(self, answer_image):
        self._answer_image = answer_image

    @property
    def answer_image_caption(self):
        return self._answer_image_caption

    @answer_image_caption.setter
    def answer_image_caption(self, answer_image_caption):
        self._answer_image_caption = answer_image_caption

    def to_json(self):
        return {
            'id': self._id,
            'tags': self._tags,
            'questionText': self.question_text,
            'choices': [c.to_json() for c in self._choices],
            'correctAnswerIndex': self._correct_answer_index,
            'answerText': self._answer_text,
            'answerImage': self._answer_image,
            'answerImageCaption': self._answer_image_caption
        }


    @staticmethod
    def from_json(question):
        return Question(question.get('questionText', ''),
                        [Choice.from_json(c) for c in question.get('choices', [])],
                        question.get('tags', []),
                        question.get('correctAnswerIndex', 0),
                        question.get('answerText', ''),
                        question.get('answerImage', ''),
                        question.get('answerImageCaption', ''),
                        question.get('id', None))

    def __str__(self):
        return f'Question: {self._id} - {self._question_text}'

    def __repr__(self):
        return f'Question(  question_text="{self._question_text}", choices="{self._choices}", tags="{self._tags}", ' \
               f'answer_index="{self._correct_answer_index}", answer_text="{self._answer_text}", ' \
               f'answer_image="{self._answer_image}", answer_image_caption="{self._answer_image_caption}", ' \
               f'id_="{self._id}")'
