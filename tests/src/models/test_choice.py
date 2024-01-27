import unittest

from kwiz_kreator.src.models.choice import Choice

class TestChoice(unittest.TestCase):

    def test_choice_activation(self):
        print("Running test_choice_activation")
        instance = Choice()
        self.assertIsInstance(instance, Choice)
        self.assertEqual(instance.text, "")
        self.assertIsNotNone(instance.id)

    def test_choice_text_setter(self):
        instance = Choice()
        instance.text = "test"
        self.assertEqual(instance.text, "test")

    def test_choice_to_json(self):
        instance = Choice()
        instance.text = "test"
        my_json = instance.to_json()
        self.assertEqual(my_json["text"], "test")

    def test_choice_from_json(self):
        my_json = {
            "text": "test",
            "id": "test_id"
        }
        instance = Choice.from_json(my_json)
        self.assertEqual(instance.text, "test")
        self.assertEqual(instance.id, "test_id")

    def test_choice_clone(self):
        my_json = {
            "text": "test",
            "id": "test_id"
        }
        instance = Choice.from_json(my_json)
        clone = Choice.clone(instance)
        self.assertEqual(clone.text, "test")
        self.assertEqual(clone.id, "test_id")


if __name__ == '__main__':
    unittest.main()
