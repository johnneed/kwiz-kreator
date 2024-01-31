from datetime import datetime, timedelta

from kwiz_kreator.src.models.quiz import Quiz
from kwiz_kreator.src.models.trivia import Trivia

def date_check(publish_days, trivia: Trivia) -> dict:
    errors = {}
    day_index = 0

    def __weekday(date_str: str) -> int:
        return datetime.strptime(date_str, '%Y/%m/%d').date().weekday()

    def __next_day(first_day, _publish_days: list[int]):
        current_day = datetime.strptime(first_day, '%Y/%m/%d').date()
        while True:
            if current_day.weekday() in publish_days:
                yield current_day.strftime("%Y/%m/%d")
            current_day += timedelta(days=1)

    def __combine_errs(err1: dict, err2: dict) -> dict:
        return {k: (err1.get(k, []) + err2.get(k, [])) for k in (err1.keys() | err2.keys())}

    def __next_day_errors(_publish_days: list[int], quizzes: list[Quiz]) -> dict:
        if len(quizzes) < 2:
            return {}
        sorted_quizzes = sorted(quizzes, reverse=False, key=lambda q: q.publish_date)

        find_next_day = __next_day(sorted_quizzes[0].publish_date, _publish_days)
        errs = {}
        next_day = next(find_next_day)
        for quiz in sorted_quizzes:
            if quiz.publish_date != next_day:
                errs[quiz.id] = ["NONSEQUENTIAL"]
            else:
                next_day = next(find_next_day)
        return errs

    missing_errors = {quiz.id: ["MISSING"] for quiz in trivia.quizzes if quiz.publish_date is None}
    good_quizzes = [quiz for quiz in trivia.quizzes if quiz.id not in missing_errors.keys()]
    bad_day_errors = {quiz.id: ["BAD_DAY"] for quiz in good_quizzes if __weekday(quiz.publish_date) not in publish_days}
    next_day_errors = __next_day_errors(publish_days, good_quizzes)
    pub_dates = [quiz.publish_date for quiz in good_quizzes]
    duplicate_errors = {quiz.id: ["DUPLICATE"] for quiz in good_quizzes if pub_dates.count(quiz.publish_date) > 1}
    return __combine_errs(__combine_errs(missing_errors, bad_day_errors),
                          __combine_errs(next_day_errors, duplicate_errors))
