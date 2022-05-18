"""
Early morning triples!!!
"""
import datetime
import json
import os
import random

from early_morning_triples.constants.colors import BColors
from early_morning_triples.constants.constants import (
    CAN_PROVINCE_AND_TERRITORY_CAPITALS,
    COUNTRY_CAPITALS,
    QUESTIONS,
    ROUND1,
    ROUND2,
    ROUND3,
    SCORE,
    TIEBREAKER,
    US_STATE_CAPITALS,
)
from early_morning_triples.utils import QuestionPicker


class EarlyMorningTriples(object):
    def __init__(self):
        self.base = os.path.abspath(os.path.dirname(__file__))

        self.contestants = []
        self.scorecard = {}

        self.question_picker = QuestionPicker()

    def _get_contestants(self):
        while True:
            contestant_count = len(self.contestants)

            contestant = input(
                BColors.MAGENTA
                + f'Enter contestant #{contestant_count + 1} (or "EXIT"): '
            ).strip()
            if contestant in self.contestants:
                print(f"{contestant} is already a registered contestant!")
                continue

            if contestant == "EXIT":
                break

            self.contestants.append(contestant)
            self.scorecard[contestant] = {
                QUESTIONS: {ROUND1: [], ROUND2: [], ROUND3: [], TIEBREAKER: []},
                SCORE: 0,
            }

            if len(self.contestants) == 4:
                break

        # Randomize contestant order
        random.shuffle(self.contestants)

        if len(self.contestants) < 2:
            raise ValueError("There must be at least two contestants!")

    def _ask_questions(self, question_set, round_number):
        for contestant in self.contestants:
            print(BColors.GREEN + f"{contestant} is up for {round_number}!")
            for i in range(3):
                question, answer = self.question_picker.pick_question(question_set)
                while (
                    contestant_is_correct := input(
                        BColors.WHITE
                        + f"Question #{i + 1} - {contestant}, What is the capital of {question} ({answer}) yes/no: "
                    ).lower()
                ) not in ["yes", "no"]:
                    print('Enter either "yes" or "no"')

                self.scorecard[contestant][QUESTIONS][round_number].append(
                    {
                        "question": question,
                        "answer": answer,
                        "contestant_is_correct": contestant_is_correct,
                    }
                )

                if contestant_is_correct == "yes":
                    self.scorecard[contestant][SCORE] += 1

    def _tiebreaker(self):
        # Check for tiebreaker
        max_score = max(v["score"] for v in self.scorecard.values())

        top_contestants = [
            contestant
            for contestant, values in self.scorecard.items()
            if values["score"] == max_score
        ]

        if len(top_contestants) == 1:
            return top_contestants[0], False
        else:
            # Reverse order for participants from non-tiebreaker question
            print(top_contestants)
            print(self.contestants)
            top_contestants = [
                c for c in reversed(self.contestants) if c in top_contestants
            ]

            print(BColors.RED + "We have a TIEBREAKER!!!")
            print(
                f"Tiebreaker contestants are: {', '.join(top_contestants)} with {max_score} points each"
            )
            tiebreaker_round = 1
            while len(top_contestants) > 1:
                contestants_to_remove = []
                for contestant in top_contestants:
                    question, answer = self.question_picker.pick_question(
                        COUNTRY_CAPITALS
                    )
                    while (
                        contestant_is_correct := input(
                            BColors.WHITE
                            + f"Tiebreak Question #{tiebreaker_round} - {contestant}, What is the capital of "
                            f"{question} ({answer}) yes/no: "
                        ).lower()
                    ) not in ["yes", "no"]:
                        print('Enter either "yes" or "no"')

                    self.scorecard[contestant][QUESTIONS][TIEBREAKER].append(
                        {
                            "question": question,
                            "answer": answer,
                            "contestant_is_correct": contestant_is_correct,
                        }
                    )

                    if contestant_is_correct == "no":
                        contestants_to_remove.append(contestant)

                tiebreaker_round += 1

                if contestants_to_remove != top_contestants:
                    for contestant in contestants_to_remove:
                        top_contestants.remove(contestant)

            return top_contestants[0], True

    def _save_scorecard(self, winner, had_tiebreaker):
        should_save_scorecard = input(
            BColors.CYAN + "Would you like to save a scorecard? yes/no: "
        ).lower()
        if should_save_scorecard == "yes":
            scorecard_dir = os.path.join(self.base, "scorecards")

            if not os.path.exists(scorecard_dir):
                os.mkdir(scorecard_dir)

            name = f"early-morning-triples-scorecard-{datetime.datetime.now().strftime('%-m-%-d-%y')}.json"
            with open(os.path.join(scorecard_dir, name), "w") as j:
                j.write(
                    json.dumps(
                        {
                            "winner": winner,
                            "had_tiebreaker": had_tiebreaker,
                            "scorecard": self.scorecard,
                        },
                        indent=4,
                        sort_keys=True,
                        ensure_ascii=False,
                        separators=(",", ":"),
                    )
                )

    def __call__(self):
        # Get the contestants
        self._get_contestants()

        # Round 1: US state capitals
        self._ask_questions(US_STATE_CAPITALS, ROUND1)

        # Round 2: CAN province/territory capitals
        self._ask_questions(CAN_PROVINCE_AND_TERRITORY_CAPITALS, ROUND2)

        # Round 3: Country capitals
        self._ask_questions(COUNTRY_CAPITALS, ROUND3)

        # Tiebreak?
        winner, had_tiebreaker = self._tiebreaker()
        if had_tiebreaker:
            print(
                BColors.GREEN + f"Today's winner is {winner} with a tiebreaker victory!"
            )
        else:
            print(BColors.GREEN + f"Today's winner is {winner}!")

        # Save scorecard
        self._save_scorecard(winner, had_tiebreaker)


if __name__ == "__main__":
    EarlyMorningTriples()()
