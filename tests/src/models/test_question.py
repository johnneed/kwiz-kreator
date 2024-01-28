import unittest

from kwiz_kreator.src.models.question import Question


class TestQuestion(unittest.TestCase):

    def test_question_activation(self):
        instance = Question()
        self.assertIsInstance(instance, Question)
        self.assertIsNotNone(instance.id)
        self.assertEqual(instance.question_text, "")
        self.assertEqual(instance.answer_text, "")
        self.assertEqual(instance.answer_image, "")
        self.assertEqual(instance.answer_image_caption, "")
        self.assertEqual(len(instance.choices), 4)
        self.assertEqual(instance.correct_answer_index, 0)
        self.assertEqual(instance.tags, [])

    def test_question_setters(self):
        instance = Question()
        instance.question_text = "question text"
        instance.answer_text = "answer text"
        instance.answer_image = "image"
        instance.answer_image_caption = "caption"
        instance.choices = []
        instance.correct_answer_index = 1
        instance.tags = ["tag"]

        self.assertEqual(instance.tags, ["tag"])
        self.assertEqual(instance.question_text, "question text")
        self.assertEqual(instance.answer_text, "answer text")
        self.assertEqual(instance.answer_image, "image")
        self.assertEqual(instance.answer_image_caption, "caption")
        self.assertEqual(len(instance.choices), 4)
        self.assertEqual(instance.correct_answer_index, 1)

    def test_question_to_json(self):
        instance = Question()
        instance.question_text = "question text"
        instance.answer_text = "answer text"
        instance.answer_image = "image"
        instance.answer_image_caption = "caption"
        instance.choices = []
        instance.correct_answer_index = 1
        instance.tags = ["tag"]
        my_json = instance.to_json()
        self.assertEqual(my_json["questionText"], "question text")

    def test_question_from_json(self):
        my_json = {
            "id": "test_id",
            "questionText": "question text",
            "answerText": "answer text",
            "answerImage": "image",
            "answerImageCaption": "caption",
            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"}, {"id": "baz", "text": "BAZ"}, {"id": "qux", "text": "QUX"}],
            "correctAnswerIndex": 1,
            "tags": ["tag"]
        }
        instance = Question.from_json(my_json)
        self.assertEqual(instance.id, "test_id")
        self.assertEqual(instance.tags, ["tag"])
        self.assertEqual(instance.question_text, "question text")
        self.assertEqual(instance.answer_text, "answer text")
        self.assertEqual(instance.answer_image, "image")
        self.assertEqual(instance.answer_image_caption, "caption")
        self.assertEqual(len(instance.choices), 4)
        self.assertEqual(instance.correct_answer_index, 1)

    def test_question_clone(self):
        instance = Question()
        instance.question_text = "question text"
        instance.answer_text = "answer text"
        instance.answer_image = "image"
        instance.answer_image_caption = "caption"
        instance.choices = []
        instance.correct_answer_index = 1
        instance.tags = ["tag"]
        clone = Question.clone(instance)
        self.assertEqual(instance.tags, ["tag"])
        self.assertEqual(instance.question_text, clone.question_text)
        self.assertEqual(instance.answer_text, clone.answer_text)
        self.assertEqual(instance.answer_image, clone.answer_image)
        self.assertEqual(instance.answer_image_caption, clone.answer_image_caption)
        self.assertEqual(len(clone.choices), 4)
        self.assertEqual(str(instance.choices), str(clone.choices))
        self.assertEqual(instance.correct_answer_index, clone.correct_answer_index)
        self.assertEqual(instance.id, clone.id)

    def test_repr(self):
        self.maxDiff = None
        my_json = {
            "id": "test_id",
            "questionText": "question text",
            "answerText": "answer text",
            "answerImage": "image",
            "answerImageCaption": "caption",
            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"}, {"id": "baz", "text": "BAZ"}, {"id": "qux", "text": "QUX"}],
            "correctAnswerIndex": 1,
            "tags": ["tag"]
        }
        instance = Question.from_json(my_json)
        test_repr = repr(instance)
        print("REPR STRING")
        print(test_repr)
        self.assertEqual(test_repr, 'Question(question_text="question text", choices=[Choice(id="foo", text="FOO"), Choice(id="bar", text="BAR"), Choice(id="baz", text="BAZ"), Choice(id="qux", text="QUX")], tags=[\'tag\'], answer_index=1, answer_text="answer text", answer_image="image", answer_image_caption="caption", id_="test_id")')

    def test_str(self):
        self.maxDiff = None
        my_json = {
            "id": "test_id",
            "questionText": "question text",
            "answerText": "answer text",
            "answerImage": "image",
            "answerImageCaption": "caption",
            "choices": [{"id": "foo"}, {"id": "bar"}, {"id": "baz"}, {"id": "qux"}],
            "correctAnswerIndex": 1,
            "tags": ["tag"]
        }
        instance = Question.from_json(my_json)
        test_str = str(instance)
        print("STR STRING")
        print(test_str)
        self.assertEqual(test_str, 'Question: test_id - question text')


if __name__ == '__main__':
    unittest.main()
