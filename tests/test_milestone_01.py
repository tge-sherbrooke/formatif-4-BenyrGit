"""
Milestone 1: Code Structure (25 points)
=======================================

This milestone verifies that the student has:
1. Created a valid main.py script
2. Used proper Python structure (functions + main guard)
3. Defined configuration constants

These tests analyze code structure via AST/regex.
Tests analyze code structure via AST/regex, not execution.
"""

import os
import ast
import re
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Helper: Get repository root
# ---------------------------------------------------------------------------
def get_repo_root():
    """Find the repository root by looking for .github folder."""
    current = Path(__file__).parent.parent
    if (current / ".github").exists():
        return current
    return current


REPO_ROOT = get_repo_root()


# ---------------------------------------------------------------------------
# Test 1.1: Script Exists (5 points)
# ---------------------------------------------------------------------------
def test_main_script_exists():
    """
    Verify that main.py exists in the repository.

    Expected: main.py file present

    Suggestion: Create a file named main.py at the repository root.
    This will be your main program with timer and button polling.
    """
    script_path = REPO_ROOT / "main.py"

    assert script_path.exists(), (
        f"\n\n"
        f"Expected: main.py file in repository root\n"
        f"Actual: File not found at {script_path}\n\n"
        f"Suggestion: Create main.py with your timer and button polling code.\n"
    )


# ---------------------------------------------------------------------------
# Test 1.2: Script Has Valid Python Syntax (5 points)
# ---------------------------------------------------------------------------
def test_main_script_syntax():
    """
    Verify that main.py has valid Python syntax.

    Expected: Python code that compiles without SyntaxError

    Suggestion: Run 'python3 -m py_compile main.py' locally to find errors.
    """
    script_path = REPO_ROOT / "main.py"

    if not script_path.exists():
        pytest.skip("main.py not found - skipping syntax check")

    content = script_path.read_text()

    try:
        ast.parse(content)
    except SyntaxError as e:
        pytest.fail(
            f"\n\n"
            f"Expected: Valid Python syntax\n"
            f"Actual: SyntaxError on line {e.lineno}: {e.msg}\n\n"
            f"Suggestion: Check line {e.lineno} for syntax errors.\n"
            f"Run locally: python3 -m py_compile main.py\n"
        )


# ---------------------------------------------------------------------------
# Test 1.3: Main Guard Present (5 points)
# ---------------------------------------------------------------------------
def test_main_guard():
    """
    Verify that the script has the __name__ == "__main__" guard.

    Expected: if __name__ == "__main__": pattern

    Suggestion: Add at the end of your script:
        if __name__ == "__main__":
            main()
    """
    script_path = REPO_ROOT / "main.py"

    if not script_path.exists():
        pytest.skip("main.py not found")

    content = script_path.read_text()

    has_guard = '__name__' in content and '__main__' in content

    if not has_guard:
        pytest.fail(
            f"\n\n"
            f"Expected: if __name__ == \"__main__\": guard\n"
            f"Actual: No main guard found\n\n"
            f"Suggestion: Add this pattern to your script:\n"
            f"  def main():\n"
            f"      # Your main code here\n"
            f"      pass\n"
            f"\n"
            f"  if __name__ == \"__main__\":\n"
            f"      main()\n"
            f"\n"
            f"This allows your code to be imported as a module.\n"
        )


# ---------------------------------------------------------------------------
# Test 1.4: Function Definitions Present (5 points)
# ---------------------------------------------------------------------------
def test_function_definitions():
    """
    Verify that the script has function definitions.

    Expected: At least one 'def' function (read_sensor, publish_data, etc.)

    Suggestion: Structure your code with functions:
        def read_sensor():
            # Sensor reading logic

        def publish_data(data):
            # Publishing logic
    """
    script_path = REPO_ROOT / "main.py"

    if not script_path.exists():
        pytest.skip("main.py not found")

    content = script_path.read_text()

    # Parse AST to count function definitions
    try:
        tree = ast.parse(content)
        func_defs = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        func_names = [f.name for f in func_defs]

        if len(func_defs) < 2:
            pytest.fail(
                f"\n\n"
                f"Expected: At least 2 function definitions\n"
                f"Actual: Found {len(func_defs)} function(s): {func_names}\n\n"
                f"Suggestion: Organize your code with functions:\n"
                f"  def read_sensor(sensor):\n"
                f"      \"\"\"Read data from sensor.\"\"\"\n"
                f"      ...\n"
                f"\n"
                f"  def publish_data(client, data):\n"
                f"      \"\"\"Publish data to MQTT.\"\"\"\n"
                f"      ...\n"
            )
    except SyntaxError:
        pytest.skip("Syntax error - cannot parse AST")


# ---------------------------------------------------------------------------
# Test 1.5: Config Constants Present (5 points)
# ---------------------------------------------------------------------------
def test_config_constants():
    """
    Verify that configuration constants are defined at module level.

    Expected: INTERVAL, SENSOR_PIN, or similar constants

    Suggestion: Define constants at the top of your script:
        SENSOR_INTERVAL = 5  # seconds between readings
    """
    script_path = REPO_ROOT / "main.py"

    if not script_path.exists():
        pytest.skip("main.py not found")

    content = script_path.read_text()

    # Look for UPPERCASE constants
    has_constants = any([
        re.search(r'^[A-Z][A-Z_0-9]+\s*=', content, re.MULTILINE),
        "INTERVAL" in content,
        "SENSOR" in content and "=" in content,
        "GPIO" in content and "=" in content,
    ])

    if not has_constants:
        pytest.fail(
            f"\n\n"
            f"Expected: Configuration constants (UPPERCASE_NAMES)\n"
            f"Actual: No constants found\n\n"
            f"Suggestion: Define constants at the top of your script:\n"
            f"  SENSOR_INTERVAL = 5    # seconds between readings\n"
            f"  BUTTON_PIN = 17        # GPIO pin for button\n"
            f"  MAX_QUEUE_SIZE = 100   # Maximum items in queue\n"
            f"\n"
            f"Constants make your code more readable and maintainable.\n"
        )
