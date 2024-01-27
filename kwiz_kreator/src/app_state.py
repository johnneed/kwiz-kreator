import queue

from toolz import curry

from .models.quiz import Quiz
from .models.trivia import Trivia


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
        self.message_queue.put(message)
        for subscriber in self.subscribers:
            subscriber.receive(message)

    def get_trivia(self):
        return self.trivia

    def set_trivia(self, trivia):
        self.trivia = trivia
        self.selected_quiz = None
        self.set_dirty(False)
        self.publish('trivia_loaded')

    def add_quiz(self, quiz):
        self.trivia.quizzes.append(quiz)
        self.selected_quiz = Quiz.clone(quiz)
        self.trivia.sort_quizzes()
        self.set_dirty(True)
        self.publish('quiz_added')

    def delete_quiz(self, quiz_id):
        new_quizzes = [quiz for quiz in self.trivia.quizzes if quiz.id != quiz_id]
        self.trivia.quizzes = new_quizzes
        self.selected_quiz = None
        self.set_dirty(False)
        self.publish('quiz_deleted')

    def get_selected_quiz(self):
        return self.selected_quiz

    def set_selected_quiz_by_id(self, quiz_id):
        quiz = next((quiz for quiz in self.trivia.quizzes if quiz.id == quiz_id), None)
        if quiz is None:
            self.selected_quiz = None
        else:
            self.selected_quiz = Quiz.clone(quiz)
        self.publish('quiz_selected')

    def clear_selected_quiz(self):
        self.selected_quiz = None
        self.set_dirty(False)
        self.publish('selected_quiz_cleared')

    @curry
    def set_selected_quiz_property(self, prop, value):
        if self.selected_quiz is not None and value != getattr(self.selected_quiz, prop):
            setattr(self.selected_quiz, prop, value)
            self.set_dirty(True)
            self.publish('selected_quiz_changed')
            if prop == "publish_date":
                self.update_trivia_with_selected_quiz()

    @curry
    def set_question_property(self, index, prop, value):
        if self.selected_quiz is not None and value != getattr(self.selected_quiz.questions[index], prop):
            question = self.selected_quiz.questions[index]
            setattr(question, prop, value)
            self.set_dirty(True)
            self.publish('selected_quiz_changed')

    @curry
    def set_choice_text(self, question_index, choice_index, value):
        if self.selected_quiz is not None and value != getattr(
                self.selected_quiz.questions[question_index].choices[choice_index], "text"):
            question = self.selected_quiz.questions[question_index]
            choice = question.choices[choice_index]
            setattr(choice, "text", value)
            self.set_dirty(True)
            self.publish('selected_quiz_changed')

    def set_dirty(self, value=True):
        self.is_dirty = value
        self.publish('dirty_changed')

    def update_trivia_with_selected_quiz(self):
        for idx, quiz in enumerate(self.trivia.quizzes):
            if quiz.id == self.selected_quiz.id:
                self.trivia.quizzes[idx] = Quiz.clone(self.selected_quiz)
                break
        self.trivia.sort_quizzes()
        self.set_dirty(False)
        self.publish('quiz_updated')

    def reset_selected_quiz(self):
        for idx, quiz in enumerate(self.trivia.quizzes):
            self.selected_quiz = Quiz.clone(self.trivia.quizzes[idx])
            self.set_dirty(False)
            self.publish('selected_quiz_reset')

    def __swap_questions(self, index1, index2):
        self.selected_quiz.questions[index1], self.selected_quiz.questions[index2] = self.selected_quiz.questions[
            index2], self.selected_quiz.questions[index1]
        self.set_dirty(True)
        self.publish('questions_reordered')

    def swap_questions(self, index1, index2):
        # sanity check
        if index1 >= 5 or index2 >= 5 or index1 < 0 or index2 < 0:
            return lambda: None
        return lambda: self.__swap_questions(index1, index2)

    def __str__(self):
        return f'AppState:\n\t isDirty: {self.is_dirty}\n\t selected_quiz:{self.selected_quiz}'

    def __repr__(self):
        return f'AppState:\n\t isDirty: {self.is_dirty}\n\t selected_quiz:{self.selected_quiz}'
