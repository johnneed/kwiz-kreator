import queue

from ..models.trivia import Trivia


class TriviaState:
    subscribers = []
    trivia = Trivia()
    selected_quiz_id = None

    def __init__(self, trivia=None, selected_quiz_id=None):
        self.message_queue = queue.Queue()
        self.subscribers = []
        self.trivia = trivia or Trivia()
        self.selected_quiz_id = selected_quiz_id

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
