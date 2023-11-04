import queue

from .models.quiz import Quiz
from .models.trivia import Trivia


class AppState:

    def __init__(self):
        self.message_queue = queue.Queue()
        self.subscribers = []
        self.trivia = Trivia()
        self.selected_quiz = None
        self.selected_quiz_is_dirty = False
        self.trivia_is_dirty = False

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
        if len(trivia.quizzes) > 0:
            self.trivia.quizzes.sort(reverse=True, key=lambda q: q.publish_date)
            self.selected_quiz = Quiz(trivia.quizzes[0].title, trivia.quizzes[0].subtitle,
                                      trivia.quizzes[0].publish_date, trivia.quizzes[0].author,
                                      trivia.quizzes[0].questions, trivia.quizzes[0].id)
        self.set_trivia_is_dirty(False)
        self.publish('trivia_loaded')


    def add_quiz(self, quiz):
        self.trivia.quizzes.append(quiz)
        self.selected_quiz = Quiz(quiz.title, quiz.subtitle, quiz.publish_date, quiz.author, quiz.questions, quiz.id)
        self.trivia.quizzes.sort(reverse=True, key=lambda q: q.publish_date)
        self.set_trivia_is_dirty(True)
        self.app_state.set_trivia_is_dirty(False)
        self.publish('quiz_added')


    def delete_quiz(self, quiz_id):
        new_quizzes = [quiz for quiz in self.trivia.quizzes if quiz.id != quiz_id]
        self.trivia.quizzes = new_quizzes
        self.publish('quiz_deleted')
        self.trivia_is_dirty = True
        if quiz_id == self.selected_quiz.id:
            self.selected_quiz = None
            self.publish('quiz_selected')

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
        self.publish('quiz_selected')
        self.selected_quiz_is_dirty = False

    def clear_selected_quiz(self):
        self.selected_quiz = None
        self.publish('selected_quiz_cleared')

    def set_selected_quiz_property(self, prop, value):
        setattr(self.selected_quiz, prop, value)
        self.publish('selected_quiz_changed')
        self.selected_quiz_is_dirty = True

    def set_question_property(self, index, prop, value=''):
        question = self.selected_quiz.questions[index]
        setattr(question, prop, value)
        self.publish('selected_quiz_changed')
        self.selected_quiz_is_dirty = True

    def set_choice_text(self, question_index, choice_index, value):
        question = self.selected_quiz.questions[question_index]
        choice = question.choices[choice_index]
        setattr(choice, "text", value)
        self.publish('selected_quiz_changed')
        self.selected_quiz_is_dirty = True

    def set_trivia_is_dirty(self, value=True):
        self.trivia_is_dirty = value
        self.publish('trivia_dirty_changed')

    def set_selected_quiz_is_dirty(self, value=None):
        if value is None:
            return
        self.selected_quiz_is_dirty = value
        self.publish('selected_quiz_dirty_changed')

    def save_selected_quiz(self):
        for quiz in self.trivia.quizzes:
            if quiz.id == self.selected_quiz.id:
                quiz.title = self.selected_quiz.title
                quiz.subtitle = self.selected_quiz.subtitle
                quiz.publish_date = self.selected_quiz.publish_date
                quiz.author = self.selected_quiz.author
                quiz.questions = self.selected_quiz.questions
                break

        self.selected_quiz_is_dirty = False
        self.set_trivia_is_dirty(True)
        self.publish('quiz_saved')

    def reset_selected_quiz(self):
        self.selected_quiz = Quiz(self.selected_quiz)
        self.selected_quiz_is_dirty = False
        self.publish('selected_quiz_reset')
