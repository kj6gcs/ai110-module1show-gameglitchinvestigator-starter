# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable.

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: _"How do I keep a variable from resetting in Streamlit when I click a button?"_
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.

  **_The game is designed to be a guessing game where the app picks a random number within a given range based upon difficulty (easy, normal, and hard). The user/player makes guesses as to what that random number may be, with a limited number of attempts per round/game based on the difficulty setting, as well. The game will give your hints as to whether you go higher or lower (or if you correctly guess the secret number) as you go through your attempts_**

- [ ] Detail which bugs you found.
- [ ] Explain what fixes you applied.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. After determining the bugs and running them through Claude to identify the code blocks and logic issues surrounding the bugs, I prompted Claude to do the following to fix these issues:

   _"ok, let's refractor all of the affected (effected?) logic code blocks into logic.utils.py. This includes get_range_for_difficulty(), parse_guess(), check_guess(), attempt_limit_map{}, the attempts allowed/limit and issue where it starts at 1 instead of zero (lines 100 and 105 as the file is now in app.py), the whole if new_game logic, and the submit logic I suppose?_

   _While you're at the refactoring, please update the logic to fix all of our identified bugs and issues."_

2. _Claude made the following changes per my request, summarized by Claude:_

#### Refactor & Bug Fix Summary

#### logic_utils.py — Pure Logic

| Function                      | Change                                                                                                                                              |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `get_range_for_difficulty()`  | Moved from app.py; fixed Normal → 1–50 and Hard → 1–100 (were swapped)                                                                              |
| `get_attempt_limit()`         | New function; fixed Easy → 8 and Normal → 6 (were swapped); Hard → 5 unchanged                                                                      |
| `parse_guess(raw, low, high)` | Moved from app.py; added `low`/`high` params; now rejects guesses outside the valid range                                                           |
| `check_guess()`               | Moved from app.py; fixed inverted hints ("Too High" → "Go LOWER!", "Too Low" → "Go HIGHER!"); removed `except TypeError` string-comparison fallback |
| `update_score()`              | Moved from app.py; no logic changes                                                                                                                 |
| `generate_secret()`           | New helper; centralizes secret generation using the correct difficulty range                                                                        |

### app.py — UI Only

| Location                      | Change                                                                                                                     |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Imports                       | Added `from logic_utils import ...`; removed `import random`                                                               |
| `attempt_limit_map` dict      | Replaced with `get_attempt_limit(difficulty)` call                                                                         |
| `attempts` session state init | Fixed: starts at `0` (was `1`)                                                                                             |
| New Game handler              | Added resets for `status`, `score`, and `history`; replaced hardcoded `randint(1, 100)` with `generate_secret(difficulty)` |
| Info banner                   | Now displays actual `low`/`high` range instead of hardcoded "1 and 100"                                                    |
| Submit — `parse_guess` call   | Now passes `low` and `high` for range validation                                                                           |
| Submit — `check_guess` call   | Removed even-attempt string conversion; secret is always passed as an integer                                              |

3. _With these initial changes, the gamed seemed fairly well repaired. However, upon testing the game, I found another bug: If you change difficulties after being on another difficulty without selecting "new game" after changing said difficulty (i.e. going from hard to normal, or any combination of going from a higher difficulty to a lower difficulty), the secret could remain higher than the valid range. So, I ran this issue by Claude as well._

4. _Claude advised "Good catch. The fix is to track the active difficulty in session state and reset the game whenever it changes. Let me update app.py."_

   _Claude then made the neccessary changes per my request._

5. _With the changes made, the game now automatically updates the secret number to be in the correct valid guessing range of the new selected difficulty._

6. _A personal point of frustration was not having the game accept my guess by pressing enter (I know some people don't mind taking their hands off their keyboards to use the mouse to click the button, but I'm not one of those people). I ran this preference by Claude and Claude identified the text imput and submit button as being the area of concern and changed the code where both items are now inside of an st.form to trigger the same "if submit:" logic._

7. _Not sure if it counts as a bug, but the developer menu would not update correctly (in my opinion, at least) as you entered guesses. Guess 1 wouldn't show until submitting guess 2, guess 2 not until guess 3, etc. I advised Claude of this issue and Claude advised:_

   _This is a Streamlit rendering order issue. The debug expander renders early in the script, before the if submit: block runs and appends to history. By the time history is updated, the expander has already drawn with the old state. Moving the expander to after the submit block fixes it._

   _Claude then moved the expander to the bottom of the game page, correcting the issue, so we now can see a live update of our guessed numbers._

**Screenshot** _(optional)_: <!-- Insert a screenshot of your fixed, winning game here -->

![Alt Text for accessibility](/winningScreenshotWithDeveloperOutput.png "Winning Screenshot")

![Alt Text for accessibility](/yayBalloons.png "Winning Screenshot - Now with 100% more balloons!")

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
