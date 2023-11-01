import queue

from .models.trivia import Trivia
from .models.quiz import Quiz

class AppState:

    def __init__(self):
        self.message_queue = queue.Queue()
        self.subscribers = []
        self.trivia = Trivia()
        self.selected_quiz_id = None
        self.selected_quiz = Quiz()

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def publish(self, message):
        self.message_queue.put(message)
        for subscriber in self.subscribers:
            subscriber.receive(message)

    def get_trivia(self):
        return self.trivia

    def set_trivia(self, trivia):
        self.trivia = trivia
        self.publish('trivia_loaded')

    def get_selected_quiz_id(self):
        return self.selected_quiz_id

    def set_selected_quiz_id(self, quiz_id):
        self.selected_quiz_id = quiz_id
        self.publish('selected-quiz-changed')

    def get_selected_quiz(self):
        return self.selected_quiz

    def set_selected_quiz(self, quiz):
        self.selected_quiz = quiz
        self.publish('selected-quiz-changed')

    def set_selected_quiz_property(self, prop, value):
        setattr(self.selected_quiz, prop, value)
        self.publish('selected-quiz-changed')

    def set_question_property(self, question_id, prop, value):
        questions = self.selected_quiz.questions
        for question in questions:
            if question.id_ == question_id:
                setattr(question, prop, value)
                break
        self.publish('selected-quiz-changed')

    def set_choice_text(self, choice_id, value):
        choice = [choice for choice in question.choices if choice_id == choice.id_][0]
        setattr(choice, "text", value)
        self.publish('selected-quiz-changed')

