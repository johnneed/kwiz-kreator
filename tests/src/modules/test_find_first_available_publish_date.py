import unittest

from freezegun import freeze_time

from kwiz_kreator.src.models.trivia import Trivia
from kwiz_kreator.src.modules.find_first_available_publish_date import find_first_available_publish_date



class TestFindFirstAvailablePublishDate(unittest.TestCase):

    @freeze_time("2012-01-14")
    def test_returns_first_day_if_no_dates(self):
        pub_dates = [0, 1, 2, 3, 4, 5, 6]
        trivia = Trivia()
        first_day = find_first_available_publish_date(pub_dates, trivia)
        print(first_day)
        self.assertEqual('2012/01/14', str(first_day))

    @freeze_time("2024-01-01")
    def test_returns_first_day_with_sequential_quizzes(self):
        test_trivia_json = {
            'id': 'ID',
            'quizzes': [
                {
                    'id': 'ID1',
                    'title': 'TITLE',
                    'subtitle': 'SUBTITLE',
                    'publishDate': '2024/01/05',
                    'author': 'AUTHOR',
                    'questions': [
                        {
                            "id": "q_id_1",
                            "questionText": "question text 1",
                            "answerText": "answer text 1",
                            "answerImage": "image 1",
                            "answerImageCaption": "caption 1",
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
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
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
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
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
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
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
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
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
                                        {"id": "qux", "text": "QUX"}],
                            "correctAnswerIndex": 5,
                            "tags": ["tag5"]
                        }
                    ]
                },
                {
                    'id': 'ID2',
                    'title': 'TITLE2',
                    'subtitle': 'SUBTITLE2',
                    'publishDate': '2024/01/12',
                    'author': 'AUTHOR2',
                    'questions': [
                        {
                            "id": "q_id_1",
                            "questionText": "question text 1",
                            "answerText": "answer text 1",
                            "answerImage": "image 1",
                            "answerImageCaption": "caption 1",
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
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
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
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
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
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
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
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
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
                                        {"id": "qux", "text": "QUX"}],
                            "correctAnswerIndex": 5,
                            "tags": ["tag5"]
                        }
                    ]
                },
                {
                    'id': 'ID3',
                    'title': 'TITLE3',
                    'subtitle': 'SUBTITLE',
                    'publishDate': '2024/01/19',
                    'author': 'AUTHOR3',
                    'questions': [
                        {
                            "id": "q_id_1",
                            "questionText": "question text 1",
                            "answerText": "answer text 1",
                            "answerImage": "image 1",
                            "answerImageCaption": "caption 1",
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
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
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
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
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
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
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
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
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
                                        {"id": "qux", "text": "QUX"}],
                            "correctAnswerIndex": 5,
                            "tags": ["tag5"]
                        }
                    ]
                }
            ]}
        pub_dates = [4]
        trivia = Trivia.from_json(test_trivia_json)
        first_day = find_first_available_publish_date(pub_dates, trivia)
        print(first_day)
        self.assertEqual('2024/01/26', str(first_day))

    @freeze_time("2024-01-01")
    def test_returns_first_day_with_non_sequential_quizzes(self):
        test_trivia_json = {
            'id': 'ID',
            'quizzes': [
                {
                    'id': 'ID1',
                    'title': 'TITLE',
                    'subtitle': 'SUBTITLE',
                    'publishDate': '2024/01/05',
                    'author': 'AUTHOR',
                    'questions': [
                        {
                            "id": "q_id_1",
                            "questionText": "question text 1",
                            "answerText": "answer text 1",
                            "answerImage": "image 1",
                            "answerImageCaption": "caption 1",
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
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
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
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
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
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
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
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
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
                                        {"id": "qux", "text": "QUX"}],
                            "correctAnswerIndex": 5,
                            "tags": ["tag5"]
                        }
                    ]
                },
                {
                    'id': 'ID2',
                    'title': 'TITLE2',
                    'subtitle': 'SUBTITLE2',
                    'publishDate': '2024/01/12',
                    'author': 'AUTHOR2',
                    'questions': [
                        {
                            "id": "q_id_1",
                            "questionText": "question text 1",
                            "answerText": "answer text 1",
                            "answerImage": "image 1",
                            "answerImageCaption": "caption 1",
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
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
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
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
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
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
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
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
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
                                        {"id": "qux", "text": "QUX"}],
                            "correctAnswerIndex": 5,
                            "tags": ["tag5"]
                        }
                    ]
                },
                {
                    'id': 'ID3',
                    'title': 'TITLE3',
                    'subtitle': 'SUBTITLE',
                    'publishDate': '2024/01/26',
                    'author': 'AUTHOR3',
                    'questions': [
                        {
                            "id": "q_id_1",
                            "questionText": "question text 1",
                            "answerText": "answer text 1",
                            "answerImage": "image 1",
                            "answerImageCaption": "caption 1",
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
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
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
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
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
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
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
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
                            "choices": [{"id": "foo", "text": "FOO"}, {"id": "bar", "text": "BAR"},
                                        {"id": "baz", "text": "BAZ"},
                                        {"id": "qux", "text": "QUX"}],
                            "correctAnswerIndex": 5,
                            "tags": ["tag5"]
                        }
                    ]
                }
            ]}

        pub_dates = [4]
        trivia = Trivia.from_json(test_trivia_json)
        first_day = find_first_available_publish_date(pub_dates, trivia)
        print(first_day)
        self.assertEqual('2024/01/19', str(first_day)
                         )