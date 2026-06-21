import random


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50   # Fixed: was 1-100 (swapped with Hard)
    if difficulty == "Hard":
        return 1, 100  # Fixed: was 1-50 (swapped with Normal)
    return 1, 100


def get_attempt_limit(difficulty: str):
    """Return the number of allowed attempts for a given difficulty."""
    limits = {
        "Easy": 8,    # Fixed: was 6 (swapped with Normal)
        "Normal": 6,  # Fixed: was 8 (swapped with Easy)
        "Hard": 5,
    }
    return limits.get(difficulty, 6)


def parse_guess(raw: str, low: int, high: int):
    """
    Parse user input into an int guess and validate it is within range.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    # Fixed: validate guess is within the valid range
    if value < low or value > high:
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess: int, secret: int):
    """
    Compare guess to secret and return (outcome, message).

    outcome: "Win", "Too High", or "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"   # Fixed: was "Go HIGHER!"
    return "Too Low", "📈 Go HIGHER!"        # Fixed: was "Go LOWER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score


def generate_secret(difficulty: str) -> int:
    """Generate a new secret number for the given difficulty."""
    low, high = get_range_for_difficulty(difficulty)
    return random.randint(low, high)
