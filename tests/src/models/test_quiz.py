import unittest

from kwiz_kreator.src.models.quiz import Quiz

test_quiz_json = {
    'id': 'ID',
    'title': 'TITLE',
    'subtitle': 'SUBTITLE',
    'publishDate': '1/1/2024',
    'author': 'AUTHOR',
    'questions': [
        {
            "id": "q_id_1",
            "questionText": "question text 1",
            "answerText": "answer text 1",
            "answerImage": "image 1",
            "answerImageCaption": "caption 1",
            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"}, {"id": "baz", "text": "BAZ"},
                        {"id": "qux", "text": "QUX"}],
            "correctAnswerIndex": 1,
            "tags": ["tag1"]
        },
        {
            "id": "q_id_2",
            "questionText": "question text 2",
            "answerText": "answer text 2",
            "answerImage": "image 2",
            "answerImageCaption": "caption 2",
            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"}, {"id": "baz", "text": "BAZ"},
                        {"id": "qux", "text": "QUX"}],
            "correctAnswerIndex": 2,
            "tags": ["tag2"]
        },
        {
            "id": "q_id_3",
            "questionText": "question text 3",
            "answerText": "answer text 3",
            "answerImage": "image 3",
            "answerImageCaption": "caption 3",
            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"}, {"id": "baz", "text": "BAZ"},
                        {"id": "qux", "text": "QUX"}],
            "correctAnswerIndex": 3,
            "tags": ["tag3"]
        },
        {
            "id": "q_id_4",
            "questionText": "question text 4",
            "answerText": "answer text 4",
            "answerImage": "image 4",
            "answerImageCaption": "caption 4",
            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"}, {"id": "baz", "text": "BAZ"},
                        {"id": "qux", "text": "QUX"}],
            "correctAnswerIndex": 4,
            "tags": ["tag4"]
        },
        {
            "id": "q_id_5",
            "questionText": "question text 5",
            "answerText": "answer text 5",
            "answerImage": "image 5",
            "answerImageCaption": "caption 5",
            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"}, {"id": "baz", "text": "BAZ"},
                        {"id": "qux", "text": "QUX"}],
            "correctAnswerIndex": 5,
            "tags": ["tag5"]
        }
    ]
}


class TestQuiz(unittest.TestCase):

    def test_quiz_activation(self):
        instance = Quiz()
        self.assertIsInstance(instance, Quiz)
        self.assertIsNotNone(instance.id)
        self.assertEqual(instance.title, "")
        self.assertEqual(instance.subtitle, "")
        self.assertNotEquals(instance.publish_date, "")
        self.assertEqual(instance.author, "")
        self.assertEqual(len(instance.questions), 5)

    def test_quiz_setters(self):
        instance = Quiz()
        instance.title = "TITLE"
        instance.subtitle = "SUBTITLE"
        instance.author = "AUTHOR"
        instance.publish_date = "1/2/2024"
        instance.questions = []

        self.assertIsNotNone(instance.id)
        self.assertEqual(instance.title, "TITLE")
        self.assertEqual(instance.subtitle, "SUBTITLE")
        self.assertEqual(instance.publish_date, "1/2/2024")
        self.assertEqual(instance.author, "AUTHOR")
        self.assertEqual(len(instance.questions), 5)

    def test_quiz_from_json(self):
        instance = Quiz.from_json(test_quiz_json)
        self.assertEqual(instance.id, "ID")
        self.assertEqual(instance.title, "TITLE")
        self.assertEqual(instance.subtitle, "SUBTITLE")
        self.assertEqual(instance.publish_date, "1/1/2024")
        self.assertEqual(instance.author, "AUTHOR")
        self.assertEqual(len(instance.questions), 5)

    def test_quiz_to_json(self):
        instance = Quiz.from_json(test_quiz_json)
        my_json = instance.to_json()
        self.assertEqual(my_json, test_quiz_json)

    def test_quiz_clone(self):
        instance = Quiz.from_json(test_quiz_json)
        clone = Quiz.clone(instance)
        self.assertEqual(instance.title, "TITLE")
        self.assertEqual(instance.subtitle, clone.subtitle)
        self.assertEqual(instance.publish_date, clone.publish_date)
        self.assertEqual(instance.author, clone.author)
        self.assertEqual(len(clone.questions), 5)
        self.assertEqual(instance.id, clone.id)

    def test_repr(self):
        self.maxDiff = None
        instance = Quiz.from_json(test_quiz_json)
        test_repr = repr(instance)
        self.assertEqual(test_repr,
                         'Quiz(title="TITLE", subtitle="SUBTITLE", publish_date="1/1/2024", author="AUTHOR", questions="[Question(question_text="question text 1", choices=[Choice(id="foo", text="FOO"), Choice(id="bar", text="BAR"), Choice(id="baz", text="BAZ"), Choice(id="qux", text="QUX")], tags=[\'tag1\'], answer_index=1, answer_text="answer text 1", answer_image="image 1", answer_image_caption="caption 1", id_="q_id_1"), Question(question_text="question text 2", choices=[Choice(id="foo", text="FOO"), Choice(id="bar", text="BAR"), Choice(id="baz", text="BAZ"), Choice(id="qux", text="QUX")], tags=[\'tag2\'], answer_index=2, answer_text="answer text 2", answer_image="image 2", answer_image_caption="caption 2", id_="q_id_2"), Question(question_text="question text 3", choices=[Choice(id="foo", text="FOO"), Choice(id="bar", text="BAR"), Choice(id="baz", text="BAZ"), Choice(id="qux", text="QUX")], tags=[\'tag3\'], answer_index=3, answer_text="answer text 3", answer_image="image 3", answer_image_caption="caption 3", id_="q_id_3"), Question(question_text="question text 4", choices=[Choice(id="foo", text="FOO"), Choice(id="bar", text="BAR"), Choice(id="baz", text="BAZ"), Choice(id="qux", text="QUX")], tags=[\'tag4\'], answer_index=4, answer_text="answer text 4", answer_image="image 4", answer_image_caption="caption 4", id_="q_id_4"), Question(question_text="question text 5", choices=[Choice(id="foo", text="FOO"), Choice(id="bar", text="BAR"), Choice(id="baz", text="BAZ"), Choice(id="qux", text="QUX")], tags=[\'tag5\'], answer_index=5, answer_text="answer text 5", answer_image="image 5", answer_image_caption="caption 5", id_="q_id_5")]", id_="ID")')

    def test_str(self):
        self.maxDiff = None
        instance = Quiz.from_json(test_quiz_json)
        test_str = str(instance)

        self.assertEqual(test_str,
                         'Quiz(title="TITLE", subtitle="SUBTITLE", publish_date="1/1/2024", author="AUTHOR", questions="[Question(question_text="question text 1", choices=[Choice(id="foo", text="FOO"), Choice(id="bar", text="BAR"), Choice(id="baz", text="BAZ"), Choice(id="qux", text="QUX")], tags=[\'tag1\'], answer_index=1, answer_text="answer text 1", answer_image="image 1", answer_image_caption="caption 1", id_="q_id_1"), Question(question_text="question text 2", choices=[Choice(id="foo", text="FOO"), Choice(id="bar", text="BAR"), Choice(id="baz", text="BAZ"), Choice(id="qux", text="QUX")], tags=[\'tag2\'], answer_index=2, answer_text="answer text 2", answer_image="image 2", answer_image_caption="caption 2", id_="q_id_2"), Question(question_text="question text 3", choices=[Choice(id="foo", text="FOO"), Choice(id="bar", text="BAR"), Choice(id="baz", text="BAZ"), Choice(id="qux", text="QUX")], tags=[\'tag3\'], answer_index=3, answer_text="answer text 3", answer_image="image 3", answer_image_caption="caption 3", id_="q_id_3"), Question(question_text="question text 4", choices=[Choice(id="foo", text="FOO"), Choice(id="bar", text="BAR"), Choice(id="baz", text="BAZ"), Choice(id="qux", text="QUX")], tags=[\'tag4\'], answer_index=4, answer_text="answer text 4", answer_image="image 4", answer_image_caption="caption 4", id_="q_id_4"), Question(question_text="question text 5", choices=[Choice(id="foo", text="FOO"), Choice(id="bar", text="BAR"), Choice(id="baz", text="BAZ"), Choice(id="qux", text="QUX")], tags=[\'tag5\'], answer_index=5, answer_text="answer text 5", answer_image="image 5", answer_image_caption="caption 5", id_="q_id_5")]", id_="ID")')

    def test_sets_correct_questions_length(self):
        instance = Quiz()
        instance.questions = []
        self.assertEqual(len(instance.questions), 5)
        too_few_questions = [{
            "id": "q_id_1",
            "questionText": "question text 1",
            "answerText": "answer text 1",
            "answerImage": "image 1",
            "answerImageCaption": "caption 1",
            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"}, {"id": "baz", "text": "BAZ"},
                        {"id": "qux", "text": "QUX"}],
            "correctAnswerIndex": 1,
            "tags": ["tag1"]
        }]
        instance.questions = too_few_questions
        self.assertEqual(len(instance.questions), 5)
        too_many_questions = [
            {
                "id": "q_id_1",
                "questionText": "question text 1",
                "answerText": "answer text 1",
                "answerImage": "image 1",
                "answerImageCaption": "caption 1",
                "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"}, {"id": "baz", "text": "BAZ"},
                            {"id": "qux", "text": "QUX"}],
                "correctAnswerIndex": 1,
                "tags": ["tag1"]
            },
            {
                "id": "q_id_2",
                "questionText": "question text 2",
                "answerText": "answer text 2",
                "answerImage": "image 2",
                "answerImageCaption": "caption 2",
                "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"}, {"id": "baz", "text": "BAZ"},
                            {"id": "qux", "text": "QUX"}],
                "correctAnswerIndex": 2,
                "tags": ["tag2"]
            },
            {
                "id": "q_id_3",
                "questionText": "question text 3",
                "answerText": "answer text 3",
                "answerImage": "image 3",
                "answerImageCaption": "caption 3",
                "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"}, {"id": "baz", "text": "BAZ"},
                            {"id": "qux", "text": "QUX"}],
                "correctAnswerIndex": 3,
                "tags": ["tag3"]
            },
            {
                "id": "q_id_4",
                "questionText": "question text 4",
                "answerText": "answer text 4",
                "answerImage": "image 4",
                "answerImageCaption": "caption 4",
                "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"}, {"id": "baz", "text": "BAZ"},
                            {"id": "qux", "text": "QUX"}],
                "correctAnswerIndex": 4,
                "tags": ["tag4"]
            },
            {
                "id": "q_id_5",
                "questionText": "question text 5",
                "answerText": "answer text 5",
                "answerImage": "image 5",
                "answerImageCaption": "caption 5",
                "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"}, {"id": "baz", "text": "BAZ"},
                            {"id": "qux", "text": "QUX"}],
                "correctAnswerIndex": 5,
                "tags": ["tag5"]
            },
            {
                "id": "q_id_6",
                "questionText": "question text 6",
                "answerText": "answer text 6",
                "answerImage": "image 6",
                "answerImageCaption": "caption 6",
                "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"}, {"id": "baz", "text": "BAZ"},
                            {"id": "qux", "text": "QUX"}],
                "correctAnswerIndex": 6,
                "tags": ["tag5"]
            }
        ]
        instance.questions = too_many_questions
        self.assertEqual(len(instance.questions), 5)


if __name__ == '__main__':
    unittest.main()
