def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except (OverflowError, TypeError, ValueError):
        return False, None, "That is not a number."

    return True, value, None


# FIX: AI-assisted review keeps guess comparisons numeric.
def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome.

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


# FIX: AI-assisted review corrected the higher/lower hint directions.
def get_guess_message(outcome: str):
    """Return user-facing feedback for a guess outcome."""
    messages = {
        "Win": "🎉 Correct!",
        "Too High": "📉 Go LOWER!",
        "Too Low": "📈 Go HIGHER!",
    }
    return messages[outcome]


def update_score(outcome: str, attempt_number: int, attempt_limit: int):
    """Score a game by guesses used: 100 first try, minus 10 per extra guess."""
    if attempt_number > attempt_limit:
        return 0

    if outcome == "Win":
        return max(0, 100 - 10 * (attempt_number - 1))

    if outcome in {"Too High", "Too Low"}:
        if attempt_number >= attempt_limit:
            return 0
        return max(0, 100 - 10 * attempt_number)

    return 0
