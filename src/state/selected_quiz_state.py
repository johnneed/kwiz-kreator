import queue

from ..models.quiz import Quiz


class SelectedQuizState:
    subscribers = []
    selected_quiz = Quiz()

    def __init__(self, selected_quiz=None):
        self.message_queue = queue.Queue()
        self.subscribers = []
        self.selected_quiz = selected_quiz or Quiz()

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def publish(self, message):
        self.message_queue.put(message)
        for subscriber in self.subscribers:
            subscriber.receive(message)

    def get_selected_quiz(self):
        return self.selected_quiz

    def set_property(self, prop, value):
        setattr(self.selected_quiz, prop, value)
        self.publish('selected-quiz-changed')

    def set_question_property(self, question_id, prop, value):
        questions = self.selected_quiz.questions
        for question in questions:
            if question.id_ == question_id:
                setattr(question, prop, value)
                break
        self.publish('selected-quiz-changed')

    def set_choice_text(self, question_id, choice_id, value):
        question = [question for question in self.selected_quiz.questions if question.id_ == question_id][0]
        choice = [choice for choice in question.choices if choice_id == choice.id_][0]
        setattr(choice, "text", value)
        self.publish('selected-quiz-changed')
