from datetime import datetime, timedelta

from toolz import curry

from kwiz_kreator.src.models.trivia import Trivia


@curry
def find_first_available_publish_date(publish_days: list[int], trivia: Trivia) -> str:
    quiz_dates = [q.publish_date for q in trivia.quizzes]
    my_day = datetime.now().date()
    while datetime.strftime(my_day, '%Y/%m/%d') in quiz_dates or my_day.weekday() not in publish_days:
        my_day += timedelta(1)
    return datetime.strftime(my_day, '%Y/%m/%d')

