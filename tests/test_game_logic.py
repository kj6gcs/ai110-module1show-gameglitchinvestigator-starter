from logic_utils import check_guess, get_range_for_difficulty, get_attempt_limit, parse_guess


# --- Existing baseline tests (corrected to unpack the (outcome, message) tuple) ---

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Bug 1: Inverted hint messages ---
# check_guess was returning "Go HIGHER!" when the guess was too high,
# and "Go LOWER!" when the guess was too low.

def test_too_high_hint_directs_player_lower():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected 'LOWER' in hint, got: {message}"

def test_too_low_hint_directs_player_higher():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected 'HIGHER' in hint, got: {message}"


# --- Bug 2: String comparison on even attempts ---
# On even-numbered attempts, the secret was cast to a string before being passed
# to check_guess. Lexicographic comparison makes "9" > "10" (True), which is
# wrong numerically. check_guess must always use integer comparison.

def test_integer_comparison_not_lexicographic():
    # Lexicographically "9" > "10" because "9" > "1", so this would wrongly
    # return "Too High". Correct integer comparison: 9 < 10, so "Too Low".
    outcome, _ = check_guess(9, 10)
    assert outcome == "Too Low", "check_guess must compare integers, not strings"

def test_two_digit_boundary_comparison():
    # Another case where string vs int comparison diverges: "19" < "2" lexicographically
    # but 19 > 2 numerically.
    outcome, _ = check_guess(19, 2)
    assert outcome == "Too High"


# --- Bug 3: Difficulty ranges were swapped for Normal and Hard ---
# Normal was 1-100 and Hard was 1-50; they should be Normal 1-50, Hard 1-100.

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_normal_range_is_not_harder_than_hard():
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert normal_high < hard_high, "Normal range should be smaller (easier) than Hard range"

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 50

def test_hard_range():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 100


# --- Bug 4: Attempt limits were swapped for Easy and Normal ---
# Easy had 6 attempts and Normal had 8; Easy should be more forgiving than Normal.

def test_easy_allows_more_attempts_than_normal():
    assert get_attempt_limit("Easy") > get_attempt_limit("Normal"), \
        "Easy should allow more attempts than Normal"

def test_easy_attempt_limit():
    assert get_attempt_limit("Easy") == 8

def test_normal_attempt_limit():
    assert get_attempt_limit("Normal") == 6

def test_hard_attempt_limit():
    assert get_attempt_limit("Hard") == 5


# --- Bug 5: parse_guess did not validate the guess was within the valid range ---
# Out-of-range inputs like 777 were accepted and processed as valid guesses.

def test_parse_guess_rejects_above_range():
    ok, value, err = parse_guess("777", 1, 100)
    assert not ok
    assert value is None
    assert err is not None

def test_parse_guess_rejects_below_range():
    ok, value, err = parse_guess("0", 1, 100)
    assert not ok
    assert value is None
    assert err is not None

def test_parse_guess_accepts_value_at_lower_bound():
    ok, value, err = parse_guess("1", 1, 100)
    assert ok
    assert value == 1
    assert err is None

def test_parse_guess_accepts_value_at_upper_bound():
    ok, value, err = parse_guess("100", 1, 100)
    assert ok
    assert value == 100
    assert err is None

def test_parse_guess_accepts_value_in_range():
    ok, value, err = parse_guess("50", 1, 100)
    assert ok
    assert value == 50
    assert err is None

def test_parse_guess_rejects_non_numeric_input():
    ok, value, err = parse_guess("abc", 1, 100)
    assert not ok
    assert value is None
    assert err is not None

def test_parse_guess_rejects_empty_input():
    ok, value, _ = parse_guess("", 1, 100)
    assert not ok
    assert value is None
