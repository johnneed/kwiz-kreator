import queue

from .models.quiz import Quiz
from .models.trivia import Trivia
from toolz import curry

class AppState:

    def __init__(self):
        self.message_queue = queue.Queue()
        self.subscribers = []
        self.trivia = Trivia()
        self.selected_quiz = None
        self.is_dirty = False

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def publish(self, message):
        print('publishing message: ', message)
        self.message_queue.put(message)
        for subscriber in self.subscribers:
            subscriber.receive(message)

    def get_trivia(self):
        return self.trivia

    def set_trivia(self, trivia):
        self.trivia = trivia
        self.selected_quiz = None
        self.is_dirty = False
        self.publish('trivia_loaded')

    def add_quiz(self, quiz):
        self.trivia.quizzes.append(quiz)
        self.selected_quiz = Quiz(quiz.title, quiz.subtitle, quiz.publish_date, quiz.author, quiz.questions, quiz.id)
        self.trivia.quizzes.sort(reverse=True, key=lambda q: q.publish_date)
        self.is_dirty = True
        self.publish('quiz_added')

    def delete_selected_quiz(self):
        quiz_id = self.selected_quiz.id
        new_quizzes = [quiz for quiz in self.trivia.quizzes if quiz.id != quiz_id]
        self.trivia.quizzes = new_quizzes
        self.selected_quiz = None
        self.is_dirty = True
        self.publish('quiz_deleted')

    def get_selected_quiz(self):
        return self.selected_quiz

    def set_selected_quiz_by_id(self, quiz_id):
        quiz = next((quiz for quiz in self.trivia.quizzes if quiz.id == quiz_id), None)
        if quiz is None:
            self.selected_quiz = None
        else:
            # use a clone of the quiz so that we can isolate changes
            self.selected_quiz = Quiz(quiz.title, quiz.subtitle, quiz.publish_date, quiz.author, quiz.questions,
                                      quiz.id)
        self.is_dirty = False
        self.publish('quiz_selected')

    def clear_selected_quiz(self):
        self.selected_quiz = None
        self.is_dirty = False
        self.publish('selected_quiz_cleared')

    @curry
    def set_selected_quiz_property(self, prop, value):
        if self.selected_quiz is not None and value != getattr(self.selected_quiz, prop):
            setattr(self.selected_quiz, prop, value)
            self.is_dirty = True
            self.publish('selected_quiz_changed')

    @curry
    def set_question_property(self, index, prop, value):
        if self.selected_quiz is not None and value != getattr(self.selected_quiz.questions[index], prop):
            question = self.selected_quiz.questions[index]
            setattr(question, prop, value)
            self.is_dirty = True
            self.publish('selected_quiz_changed')

    @curry
    def set_choice_text(self, question_index, choice_index, value):
        if self.selected_quiz is not None and value != getattr(self.selected_quiz.questions[question_index].choices[choice_index], "text"):
            question = self.selected_quiz.questions[question_index]
            choice = question.choices[choice_index]
            setattr(choice, "text", value)
            self.publish('selected_quiz_changed')
            self.is_dirty = True

    def set_dirty(self, value=True):
        self.is_dirty = value
        self.publish('dirty_changed')

    def update_trivia_with_selected_quiz(self):
        for quiz in self.trivia.quizzes:
            if quiz.id == self.selected_quiz.id:
                quiz.title = self.selected_quiz.title
                quiz.subtitle = self.selected_quiz.subtitle
                quiz.publish_date = self.selected_quiz.publish_date
                quiz.author = self.selected_quiz.author
                quiz.questions = self.selected_quiz.questions
                break

        self.is_dirty = False
        self.publish('quiz_updated')


    def reset_selected_quiz(self):
        self.selected_quiz = Quiz(self.selected_quiz)
        self.is_dirty = False
        self.publish('selected_quiz_reset')
        self.publish('selected_quiz_dirty_changed')
