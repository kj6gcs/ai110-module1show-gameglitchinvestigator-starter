# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

The game looked as it should (I'd assume) with the developer debug info available (I'm guessing it wouldn't be visible for an end user). First thing I noticed was the side bar under normal difficulty stated I had 8 attempts allowed, but shen I checked the main windo, it stated I had 7 attempts remaining.

During testing, I swapped between the different difficulties and noticed that "Easy" had you guess between 1 - 20, "Normal" had you guess between 1 - 100, and "Hard" had you guess between 1 - 50. I've noted game bugs discovered below, but the difficulties and their guess ranges aren't aligned either. "Easy" is correct with a range of 1 - 20, as the user's change of guessing the correct secret number becomes substantially easier when there are so few numbers. However, "Normal" should have the range of 1 - 50 (more difficult to guess correctly than 1 - 20), and "Hard" should have the range of 1 - 100, as it would be extremely difficult to guess the number with the allotted guesses of 5.

Further along those same lines is the issue with the allotted number of guesses per difficulty. The original settings is "Easy" allows for 6 attempts, "Normal" allows for 8, and "Hard" allows for 5. "Hard" has the right number of guesses, but the number of guesses for "Easy" and "Normal" should be swapped.

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
| (string error) |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
