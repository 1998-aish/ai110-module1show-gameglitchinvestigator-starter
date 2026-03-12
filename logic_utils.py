"""Game logic utilities for number guessing game.

This module provides functions for parsing user input, comparing guesses,
updating scores, and determining difficulty ranges.
"""


def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """
    Return the inclusive range of valid values for a given difficulty level.
    
    This function maps difficulty levels to their corresponding numeric ranges,
    typically used for game mechanics such as number guessing or scoring systems.
    
    Parameters
    ----------
    difficulty : str
        The difficulty level. Supported values are:
        - "Easy": Returns range 1-20
        - "Normal": Returns range 1-50
        - "Hard": Returns range 1-100
        
    Returns
    -------
    tuple of (int, int)
        A tuple containing (low, high) representing the inclusive range for the
        given difficulty level. If an unrecognized difficulty is provided,
        defaults to (1, 100).
        
    Examples
    --------
    >>> get_range_for_difficulty("Easy")
    (1, 20)
    >>> get_range_for_difficulty("Normal")
    (1, 50)
    >>> get_range_for_difficulty("Hard")
    (1, 100)
    """
    # FIX: Corrected the hint logic where normal was high than difficulty.
     # Used Copilot to analyze the bug and refactor the logic into logic_utils.py.
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100


def parse_guess(raw: str) -> tuple[bool, int | None, str | None]:
    """Parse user input into an integer guess.

    This function takes a raw string input and attempts to convert it into an integer.
    It handles both integer and decimal string formats. Decimal inputs are converted
    to integers by truncating the decimal portion.

    Args:
        raw (str): The raw user input string to be parsed.

    Returns:
        tuple: A tuple containing:
            - ok (bool): True if parsing was successful, False otherwise.
            - guess_int (int | None): The parsed integer value if successful, None if failed.
            - error_message (str | None): An error message if parsing failed, None if successful.

    Raises:
        No exceptions are raised. All errors are caught and returned as error messages.

    Examples:
        >>> parse_guess("42")
        (True, 42, None)
        
        >>> parse_guess("3.14")
        (True, 3, None)
        
        >>> parse_guess("")
        (False, None, "Enter a guess.")
        
        >>> parse_guess("abc")
        (False, None, "That is not a number.")
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret) -> tuple[str, str]:
    """Compare a guess against a secret number and return the game outcome and feedback message.
    This function handles numeric comparisons and attempts type conversion if a TypeError occurs,
    allowing the function to work with both numeric and string inputs.
    Args:
        guess: The guessed value (can be int, float, or string representation of a number).
        secret: The secret value to compare against (typically int or float).
    Returns:
        tuple: A tuple containing:
            - outcome (str): One of "Win", "Too High", or "Too Low"
            - message (str): An encouraging message with emoji feedback corresponding to the outcome
    Examples:
        >>> check_guess(50, 50)
        ('Win', '🎉 Correct!')
        >>> check_guess(75, 50)
        ('Too High', '📉 Go LOWER!')
        >>> check_guess(25, 50)
        ('Too Low', '📈 Go HIGHER!')
        >>> check_guess("50", 50)
        ('Win', '🎉 Correct!')
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            # FIX: Corrected the hint logic where "Too High" previously suggested going higher.
            # Used Copilot to analyze the bug and refactor the logic into logic_utils.py.
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """
    Update the player's score based on the game outcome and attempt number.

    Args:
        current_score (int): The player's current score before the update.
        outcome (str): The result of the guess. Can be "Win", "Too High", or "Too Low".
        attempt_number (int): The current attempt number (0-indexed).

    Returns:
        int: The updated score after applying the outcome rules.

    Scoring Rules:
        - "Win": Awards 100 - 10 * (attempt_number + 1) points, with a minimum of 10 points.
        - "Too High": Awards 5 points if attempt_number is even, otherwise deducts 5 points.
        - "Too Low": Deducts 5 points.
        - Any other outcome: Returns the score unchanged.

    Examples:
        >>> update_score(100, "Win", 0)
        190
        >>> update_score(100, "Win", 10)
        110
        >>> update_score(100, "Too High", 0)
        95
        >>> update_score(100, "Too High", 1)
        105
        >>> update_score(100, "Too Low", 2)
        95
    """
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
