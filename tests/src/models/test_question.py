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
        self.assertEqual(instance.choices, [])
        self.assertEqual(instance.correct_answer_index, 0)
        self.assertEqual(instance.tags, [])

    def test_question_setters(self):
        instance = Question()
        instance.question_text = "question text"
        instance.answer_text = "answer text"
        instance.answer_image = "image"
        instance.answer_image_caption = "caption"
        instance.choices = [{}]
        instance.correct_answer_index = 1
        instance.tags = ["tag"]

        self.assertEqual(instance.tags, ["tag"])
        self.assertEqual(instance.question_text, "question text")
        self.assertEqual(instance.answer_text, "answer text")
        self.assertEqual(instance.answer_image, "image")
        self.assertEqual(instance.answer_image_caption, "caption")
        self.assertEqual(len(instance.choices), 1)
        self.assertEqual(instance.correct_answer_index, 1)

    def test_question_to_json(self):
        instance = Question()
        instance.question_text = "question text"
        instance.answer_text = "answer text"
        instance.answer_image = "image"
        instance.answer_image_caption = "caption"
        instance.choices = [{}]
        instance.correct_answer_index = 1
        instance.tags = ["tag"]
        my_json = instance.to_json()
        self.assertEqual(my_json["text"], "test")

    def test_question_from_json(self):
        my_json = {
            "id": "test_id",
            "question_text": "question text",
            "answer_text": "answer text",
            "answer_image": "image",
            "answer_image_caption": "caption",
            "choices": [{}],
            "correct_answer_index": 1,
            "tags": ["tag"]
        }
        instance = Question.from_json(my_json)
        self.assertEqual(instance.id, "test_id")
        self.assertEqual(instance.tags, ["tag"])
        self.assertEqual(instance.question_text, "question text")
        self.assertEqual(instance.answer_text, "answer text")
        self.assertEqual(instance.answer_image, "image")
        self.assertEqual(instance.answer_image_caption, "caption")
        self.assertEqual(len(instance.choices), 1)
        self.assertEqual(instance.correct_answer_index, 1)

    def test_question_clone(self):
        instance = Question()
        instance.question_text = "question text"
        instance.answer_text = "answer text"
        instance.answer_image = "image"
        instance.answer_image_caption = "caption"
        instance.choices = [{}]
        instance.correct_answer_index = 1
        instance.tags = ["tag"]
        clone = Question.clone(instance)
        self.assertEqual(instance.tags, ["tag"])
        self.assertEqual(instance.question_text, clone.question_text)
        self.assertEqual(instance.answer_text, clone.answer_text)
        self.assertEqual(instance.answer_image, clone.answer_image)
        self.assertEqual(instance.answer_image_caption, clone.answer_image)
        self.assertEqual(len(instance.choices), len(clone.choices))
        self.assertEqual(instance.correct_answer_index, clone.correct_answer_index)
        self.assertEqual(instance.id, clone.id)


if __name__ == '__main__':
    unittest.main()
