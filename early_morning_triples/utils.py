import random
from typing import Literal

from early_morning_triples.constants.can_province_capitals import (
    CAN_PROVINCE_AND_TERRITORY_CAPITALS,
)
from early_morning_triples.constants.country_capitals import COUNTRY_CAPITALS
from early_morning_triples.constants.us_state_capitals import US_STATE_CAPITALS


class QuestionPicker(object):
    def __init__(self):
        self.questions = {
            "US_STATE_CAPITALS": US_STATE_CAPITALS,
            "CAN_PROVINCE_AND_TERRITORY_CAPITALS": CAN_PROVINCE_AND_TERRITORY_CAPITALS,
            "COUNTRY_CAPITALS": COUNTRY_CAPITALS,
        }

    def pick_question(
        self,
        question_set: Literal[
            "US_STATE_CAPITALS",
            "CAN_PROVINCE_AND_TERRITORY_CAPITALS",
            "COUNTRY_CAPITALS",
        ],
    ):
        possible_questions = self.questions[question_set]
        question = random.choice(list(possible_questions.keys()))
        answer = possible_questions[question]

        del self.questions[question_set][question]

        return question, answer
