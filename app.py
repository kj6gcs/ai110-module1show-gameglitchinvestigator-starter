import streamlit as st

# FIX: All game logic moved out of app.py and into logic_utils.py.
# User requested the refactor; Claude identified which functions to extract and rewrote
# both files so app.py handles only Streamlit UI concerns.
from logic_utils import (
    get_range_for_difficulty,
    get_attempt_limit,
    parse_guess,
    check_guess,
    update_score,
    generate_secret,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

# FIX: attempt_limit_map dict replaced with get_attempt_limit() from logic_utils.
# Claude refactored this during the logic extraction and corrected the swapped Easy/Normal values.
attempt_limit = get_attempt_limit(difficulty)
low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = generate_secret(difficulty)

# FIX: attempts counter was initialized to 1 instead of 0, consuming one attempt before
# the player ever guessed. User identified the mismatch between sidebar and main window;
# Claude traced it to this initialization and corrected it to 0.
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

# FIX: Switching difficulty did not reset the secret, so an out-of-range secret could persist
# into an easier difficulty. User identified this during playtesting; Claude added difficulty
# tracking in session state so any change triggers a full game reset.
if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty

if st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.secret = generate_secret(difficulty)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []

st.subheader("Make a guess")

# FIX: Info banner was hardcoded to "1 and 100" regardless of difficulty.
# Claude updated it to use the low/high values from get_range_for_difficulty().
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

# FIX: Text input and submit button wrapped in st.form so pressing Enter submits the guess.
# User requested this as a personal preference; Claude identified st.form as the correct
# Streamlit pattern and restructured the input controls accordingly.
with st.form("guess_form"):
    raw_guess = st.text_input(
        "Enter your guess:",
        key=f"guess_input_{difficulty}"
    )
    submit = st.form_submit_button("Submit Guess 🚀")

col1, col2 = st.columns(2)
with col1:
    new_game = st.button("New Game 🔁")
with col2:
    show_hint = st.checkbox("Show hint", value=True)

# FIX: New Game did not reset status, score, or history, and used a hardcoded range.
# User found the game stayed locked on the game-over screen after clicking New Game.
# Claude added the missing status/score/history resets and replaced randint(1,100)
# with generate_secret(difficulty).
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = generate_secret(difficulty)
    st.session_state.status = "playing"
    st.session_state.score = 0
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    # FIX: parse_guess now receives low/high so out-of-range guesses (e.g. 777) are rejected.
    # User identified the issue; Claude added range parameters to parse_guess in logic_utils.
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        # FIX: Original code cast secret to a string on even-numbered attempts, causing
        # lexicographic comparison errors. Claude removed the string conversion so
        # check_guess always receives the integer secret directly.
        outcome, message = check_guess(guess_int, st.session_state.secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

# FIX: Expander moved to bottom of script so it renders after all session state updates.
# User noticed history was always one guess behind; Claude identified it as a Streamlit
# rendering order issue and relocated the expander here to fix it.
with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
