# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**_My Response_**

The game looked as it should (I'd assume) with the developer debug info available (I'm guessing it wouldn't be visible for an end user). First thing I noticed was the side bar under normal difficulty stated I had 8 attempts allowed, but shen I checked the main windo, it stated I had 7 attempts remaining.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input                | Expected Behavior | Actual Behavior                | Console Output / Error |
| -------------------- | ----------------- | ------------------------------ | ---------------------- |
| 777                  | Error message.    | Hint told me to guess higher.  | None.                  |
| -------------------- | ----------------- | ------------------------------ | ---------------------- |
| Click "New Game"     | Game reset.       | "Secret" changed, but game     | None.                  |
|                      |                   | continued to tell me to start  |                        |
|                      |                   | a new game.                    |                        |
| -------------------- | ----------------- | ------------------------------ | ---------------------- |
| Change Difficulty    | Difficulty and    | Switching between              | None.                  |
|                      | secret should     | difficulties changed the       |                        |
|                      | should change.    | guessing range _and_ secret;   |                        |
|                      |                   | however it did not change the  |                        |
|                      |                   | secret.                        |                        |
| -------------------- | ----------------- | ------------------------------ | ---------------------- |
| Attempting Guesses   | User should get   | On hard difficulty, I made 3   | "Out of attempts! The  |
|                      | full amount of    | guesses and received an "Out   | secret was 72. Score:  |
|                      | guesses.          | of attempts!" error message.   | -20" (on Hard).        |
|                      |                   |                                | problem persists on    |
|                      |                   |                                | other difficulties as  |
|                      |                   |                                | well.                  |
| -------------------- | ----------------- | ------------------------------ | ---------------------- |

**_During testing, I swapped between the different difficulties and noticed that "Easy" had you guess between 1 - 20, "Normal" had you guess between 1 - 100, and "Hard" had you guess between 1 - 50. I've noted game bugs discovered below, but the difficulties and their guess ranges aren't aligned either. "Easy" is correct with a range of 1 - 20, as the user's change of guessing the correct secret number becomes substantially easier when there are so few numbers. However, "Normal" should have the range of 1 - 50 (more difficult to guess correctly than 1 - 20), and "Hard" should have the range of 1 - 100, as it would be extremely difficult to guess the number with the allotted guesses of 5._**

**_Further along those same lines is the issue with the allotted number of guesses per difficulty. The original settings is "Easy" allows for 6 attempts, "Normal" allows for 8, and "Hard" allows for 5. "Hard" has the right number of guesses, but the number of guesses for "Easy" and "Normal" should be swapped._**

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

  **_I used Claude for this project._**

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

  **_Claude correctly determined a logic issue based upon the "777 Guess" bug I initially found. Claude determined parse_guess in app.py did not check for the guess to be in the valid range. Further, Claude correctly determined that the hints in the check_guess logic in app.py were logically inverted (i.e. guessing too high (as in 777 in my case) returned a correct outcome of "Too High," however; the hint was unlogically sound with "Go HIGHER!" when it should have stated "Go LOWER!")._**

  **_Claude even located a bug which I had not yet discovered. In app.py, the string comparison on even attempts. On every even-numbered attempt, the secret would be converted into a string, which led to a coomparison where only the first number was used, so 2 (or more) digit numbers would only be compared by their first number - i.e. 10 would be compared as "1" and 20 would be compared as "2"._**

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

  **_All of Claude's suggestions appear to have been correct._**

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

  **_In addition to the automated pytest tests, I manually went back and double checked the fixes. This led to me stumbling upon a couple of other issues that I felt needed to be addressed._**

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

  **_The most revealing test was test_integer_comparison_not_lexicographic, which checked that check_guess(9, 10) returned "Too Low" — meaning the code correctly recognized that 9 is less than 10. This sounds trivial, but it directly targeted a bug where the secret number was being converted to a string on every even-numbered attempt. Once that conversion happened, Python compared values as text rather than numbers, so "9" > "10" evaluated as True (because "9" comes after "1" alphabetically). Without this test, that bug could easily go unnoticed during casual playtesting since it only affected every other guess and produced a wrong hint rather than a crash._**

- Did AI help you design or understand any tests? How?

  **_Yes — Claude wrote the entire pytest suite in tests/test_game_logic.py. After we identified and fixed all the bugs together, I asked Claude to generate tests that specifically targeted each bug rather than just testing general functionality. Claude structured the tests in groups, one per bug, so each test had a clear purpose tied to a real failure we had observed. Claude also caught that the three original baseline tests in the file were broken — check_guess returns a tuple (outcome, message), but the original tests were comparing the full tuple against a plain string like "Win", which would have always failed. Claude corrected those while adding the new ones. The process helped me understand that good tests aren't just "does it work" checks — they're specific enough to tell you exactly which assumption broke and why._**

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

  **_I had never heard of Streamlit until this course. Most of my experience with web apps are from web development courses and projects. Every time you interact with the app — clicking a button, typing in a field, changing a dropdown — Streamlit reruns the entire Python script from top to bottom, as if you just refreshed the page. That means any regular variable you define gets reset to its starting value on every single rerun._**

  **_Session state is Streamlit's solution to this: it's a dictionary that persists between reruns, so values you store there survive across interactions. We ran into this directly with the debug history bug — the Developer Debug Info expander was being drawn early in the script, before the submit logic had a chance to update the history list. Because Streamlit renders in the order the code runs, moving the expander to the bottom of the script meant it always displayed the fully updated state. Once you understand that every button click is essentially a page reload, a lot of Streamlit's quirks start to make sense._**

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

  **_Double checking every fix performed by the AI (Claude, in this case) is actually fixed by manually checking yourself. That's how the debugger readout issue really drew my attention, and how I learned more about Streamlit and Session state, and therefore ended up moving the debugger display toward the bottom of the page._**

- What is one thing you would do differently next time you work with AI on a coding task?

  **_I'd much rather pay better attention to the changes it makes. It did a great job, but when it came to finishing up the documentation portion of this project, going back and finding (and having the AI go back and double check what I found) all the bugs/fixes to list was tedious._**

- In one or two sentences, describe how this project changed the way you think about AI generated code.

  **_I've only really used AI to assist with web development (mostly a lot of "why isn't this working correctly" debugging prompts, ahah). I'd used it a bit to assist in a Python course about a year and a half back, but most of that was learning why certain syntax did the things it did. Claude did an absolutely AMAZING job at helping me out and refreshing my memory on Python (although admittedly I still have SO MUCH to learn). I look forward to utilizing AI moving forward with some coding projects I want to complete._**

  #### (C) 2026, Robby Wideman
