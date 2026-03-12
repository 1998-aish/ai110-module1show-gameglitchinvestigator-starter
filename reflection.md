# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

## Bug Report: Inverse Number Comparison Logic

**Issue:** The game's number comparison logic is inverted, causing opposite feedback to the player.

**Description:** When the secret code is 65 and the user inputs 70, the system incorrectly instructs the player to "increase the number" instead of "decrease the number." This indicates the greater-than and less-than comparison operators are reversed.

**Root Cause:** The conditional statements checking the user's input against the secret code likely use inverted operators:
- Using `>` where `<` should be used (or vice versa)
- Using `>=` where `<=` should be used (or vice versa)

**Example of the Bug:**
- Secret number: 65, user input: 70 → incorrectly says "increase the number" instead of "decrease"

## Bug Report: Score Resets or Disappears

**Issue:** The player's score or attempt count resets unexpectedly during gameplay.

**Description:** When the game restarts or the player navigates between pages, the score disappears or resets to zero, losing all progress from the current session.

**Root Cause:** The score variable is likely not being stored in Streamlit session state, causing it to reset on each app rerun.

**Example of the Bug:**
- Player reaches a score of 5 attempts, then the page refreshes or they navigate away → score resets to 0

---
## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

I used GitHub Copilot throughout this project.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

I asked Copilot to review the `check_guess()` function using file context from `app.py` and `logic_utils.py`. Copilot correctly identified that the hint logic was reversed: when `guess > secret`, the game incorrectly returned "Go HIGHER!" instead of "Go LOWER!". I verified the fix by running pytest to confirm all tests passed, then manually testing the Streamlit game to confirm hints now guide players correctly.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

Copilot suggested changing `check_guess()` to return only the outcome string instead of a tuple. This was misleading because the existing code relied on both the outcome and message being returned. I caught this by tracing how the function was called in the game logic and realized removing the tuple would break the code. I kept the tuple structure and fixed only the hint logic.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

I ran automated pytest tests and verified the results in the live Streamlit app to confirm the fix worked correctly.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.

I created a test case in `tests/test_game_logic.py` to verify that when the guess is higher than the secret number, `check_guess()` returns "Too High" with the hint "Go LOWER". Running `python3 -m pytest` initially failed on two test cases, which revealed I hadn't fixed all the inverted logic. After correcting the remaining comparison operators, all tests passed, confirming the hint logic was fully corrected.

- Did AI help you design or understand any tests? How?

Copilot helped me structure the pytest test cases by suggesting the assertion format and helping me trace through what outputs `check_guess()` should return for each scenario (guess too high, too low, and correct).


---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.

The secret number kept changing because it wasn't stored in Streamlit session state. Every time the app reran (which happens frequently in Streamlit), the code reinitializing the secret number would execute again, generating a new random value. Without persistence, the number had no memory between reruns.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit reruns your entire script from top to bottom whenever the user interacts with the app (like clicking a button or typing input). Session state is like a notebook that remembers values across these reruns—without it, variables reset to their initial values each time. If you store something in session state, it persists even after reruns, so the game can "remember" the secret number.

- What change did you make that finally gave the game a stable secret number?

I moved the secret number initialization into Streamlit's `st.session_state` using a conditional check: `if 'secret_number' not in st.session_state:`. This ensures the secret number is generated only once at the start of a session and persists across all subsequent reruns, giving the game the stable number it needed.


---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
