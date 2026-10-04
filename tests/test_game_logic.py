import pytest
from streamlit.testing.v1 import AppTest

from logic_utils import (
    check_guess,
    get_guess_message,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

# FIX: AI-assisted regression cases cover both high/low hint directions.
def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"
    assert get_guess_message(result) == "📉 Go LOWER!"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"
    assert get_guess_message(result) == "📈 Go HIGHER!"

def test_guess_compares_multi_digit_numbers_numerically():
    assert check_guess(9, 10) == "Too Low"
    assert check_guess(20, 10) == "Too High"

@pytest.mark.parametrize(
    ("raw_guess", "secret", "expected_outcome", "expected_message"),
    [
        ("40", 50, "Too Low", "📈 Go HIGHER!"),
        ("50", 50, "Win", "🎉 Correct!"),
        ("60", 50, "Too High", "📉 Go LOWER!"),
    ],
)
def test_entered_guess_produces_expected_response(
    raw_guess, secret, expected_outcome, expected_message
):
    valid, guess, error = parse_guess(raw_guess)

    assert valid, error
    outcome = check_guess(guess, secret)
    assert outcome == expected_outcome
    assert get_guess_message(outcome) == expected_message

def test_submit_displays_feedback_after_one_click():
    app = AppTest.from_file("app.py").run(timeout=10)
    app.session_state["secret"] = 50
    app.text_input[0].set_value("60")
    app.button[0].click().run(timeout=10)

    assert app.warning[0].value.endswith("Go LOWER!")
    app.run(timeout=10)
    assert app.warning[0].value.endswith("Go LOWER!")

def test_second_guess_submits_on_first_click():
    app = AppTest.from_file("app.py").run(timeout=10)
    app.session_state["secret"] = 50

    app.text_input[0].set_value("60")
    app.button[0].click().run(timeout=10)
    assert app.session_state["history"] == [60]

    app.text_input[0].set_value("40")
    app.button[0].click().run(timeout=10)

    assert app.session_state["history"] == [60, 40]
    assert app.session_state["attempts"] == 2
    assert app.warning[0].value.endswith("Go HIGHER!")

@pytest.mark.parametrize("finished_status", ["won", "lost"])
def test_new_game_restarts_finished_game(finished_status):
    app = AppTest.from_file("app.py").run(timeout=10)
    app.session_state["status"] = finished_status
    app.session_state["attempts"] = 6
    app.session_state["score"] = 35
    app.session_state["history"] = [20, 80]
    app.session_state["guess_feedback"] = ("warning", "Old feedback")
    app.button[1].click().run(timeout=10)

    assert app.session_state["status"] == "playing"
    assert app.session_state["attempts"] == 0
    assert app.session_state["score"] == 0
    assert app.session_state["history"] == []
    assert 1 <= app.session_state["secret"] <= 100
    assert app.success[0].value == "New game started."

def test_parse_guess_returns_integer():
    assert parse_guess("42") == (True, 42, None)

def test_parse_guess_rejects_empty_and_non_numeric_input():
    assert parse_guess("") == (False, None, "Enter a guess.")
    assert parse_guess("hello") == (False, None, "That is not a number.")

def test_get_range_for_difficulty():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 50)

@pytest.mark.parametrize(
    ("current_score", "outcome", "attempt_number", "expected_score"),
    [
        (0, "Too Low", 1, 0),
        (2, "Too Low", 2, 0),
        (0, "Too High", 1, 0),
        (10, "Too High", 1, 5),
        (0, "Too High", 2, 5),
        (10, "Win", 1, 90),
    ],
)
def test_score_stays_nonnegative_after_guess(
    current_score, outcome, attempt_number, expected_score
):
    assert update_score(current_score, outcome, attempt_number) == expected_score
