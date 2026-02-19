"""
Milestone 2: Timer Pattern (35 points)
=======================================

This milestone verifies that the student has:
1. Imported the time module
2. Used time.monotonic() for non-blocking timers
3. Implemented the timer-in-loop pattern (interval comparison)
4. NOT used threading.Thread or queue.Queue (taught later)

IMPORTANT: We test code STRUCTURE, not execution.
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
# Test 2.1: time Import (10 points)
# ---------------------------------------------------------------------------
def test_time_import():
    """
    Verify that the script imports the time module.

    Expected: 'import time' or 'from time import'

    Suggestion: Add at the top of your script:
        import time
    """
    script_path = REPO_ROOT / "main.py"

    if not script_path.exists():
        pytest.skip("main.py not found")

    content = script_path.read_text()

    has_time = any([
        "import time" in content,
        "from time import" in content,
    ])

    if not has_time:
        pytest.fail(
            f"\n\n"
            f"Expected: time module import\n"
            f"Actual: No time import found\n\n"
            f"Suggestion: Add time import:\n"
            f"  import time\n"
            f"\n"
            f"The time module provides:\n"
            f"  - time.monotonic(): timer non-bloquant\n"
            f"  - time.sleep(): pause courte pour le polling\n"
        )


# ---------------------------------------------------------------------------
# Test 2.2: time.monotonic Usage (10 points)
# ---------------------------------------------------------------------------
def test_time_monotonic_usage():
    """
    Verify that the script uses time.monotonic().

    Expected: time.monotonic() call for non-blocking timing

    Suggestion: Use time.monotonic() for non-blocking timers:
        previous_time = time.monotonic()
        while True:
            current_time = time.monotonic()
            if current_time - previous_time >= INTERVAL:
                read_sensor()
                previous_time = current_time
            time.sleep(0.05)
    """
    script_path = REPO_ROOT / "main.py"

    if not script_path.exists():
        pytest.skip("main.py not found")

    content = script_path.read_text()

    has_monotonic = "time.monotonic" in content or "monotonic()" in content

    if not has_monotonic:
        pytest.fail(
            f"\n\n"
            f"Expected: time.monotonic() usage\n"
            f"Actual: No time.monotonic() found\n\n"
            f"Suggestion: Utilisez time.monotonic() pour mesurer le temps\n"
            f"sans bloquer:\n"
            f"  previous_time = time.monotonic()\n"
            f"  while True:\n"
            f"      current_time = time.monotonic()\n"
            f"      if current_time - previous_time >= SENSOR_INTERVAL:\n"
            f"          read_sensor(sensor)\n"
            f"          previous_time = current_time\n"
            f"      time.sleep(0.05)\n"
        )


# ---------------------------------------------------------------------------
# Test 2.3: Timer-in-Loop Pattern (7 points)
# ---------------------------------------------------------------------------
def test_timer_in_loop_pattern():
    """
    Verify that the timer-in-loop pattern is used.

    Expected: time.monotonic() with interval comparison (>= or >)

    Suggestion: The timer-in-loop pattern checks elapsed time:
        if current_time - previous_time >= SENSOR_INTERVAL:
            # Action a executer periodiquement
            previous_time = current_time
    """
    script_path = REPO_ROOT / "main.py"

    if not script_path.exists():
        pytest.skip("main.py not found")

    content = script_path.read_text()

    has_monotonic = "time.monotonic" in content or "monotonic()" in content

    # Check for interval comparison patterns
    has_interval_check = any([
        # Subtraction pattern: current - previous >= INTERVAL
        re.search(r'\w+\s*-\s*\w+\s*>=\s*\w+', content),
        # Subtraction pattern: current - previous > INTERVAL
        re.search(r'\w+\s*-\s*\w+\s*>\s*\w+', content),
        # INTERVAL constant defined
        re.search(r'INTERVAL\s*=', content, re.IGNORECASE),
        # Common pattern: elapsed = current - previous
        re.search(r'elapsed\s*=\s*\w+\s*-\s*\w+', content, re.IGNORECASE),
    ])

    if not has_monotonic:
        pytest.fail(
            f"\n\n"
            f"Expected: time.monotonic() for timer pattern\n"
            f"Actual: No time.monotonic() found\n\n"
            f"Suggestion: Le pattern timer-in-loop utilise\n"
            f"time.monotonic() pour mesurer les intervalles:\n"
            f"  previous_sensor = time.monotonic()\n"
            f"  while True:\n"
            f"      current = time.monotonic()\n"
            f"      if current - previous_sensor >= SENSOR_INTERVAL:\n"
            f"          read_sensor()\n"
            f"          previous_sensor = current\n"
        )

    if not has_interval_check:
        pytest.fail(
            f"\n\n"
            f"Expected: Interval comparison (current - previous >= INTERVAL)\n"
            f"Actual: No interval check found\n\n"
            f"Suggestion: Comparez le temps ecoule avec un intervalle:\n"
            f"  SENSOR_INTERVAL = 5  # secondes\n"
            f"  previous_sensor = time.monotonic()\n"
            f"\n"
            f"  while True:\n"
            f"      current = time.monotonic()\n"
            f"      if current - previous_sensor >= SENSOR_INTERVAL:\n"
            f"          read_sensor()\n"
            f"          previous_sensor = current\n"
            f"      time.sleep(0.05)\n"
        )


# ---------------------------------------------------------------------------
# Test 2.4: No threading.Thread (8 points)
# ---------------------------------------------------------------------------
def test_no_threading():
    """
    Verify that the student does NOT use threading.Thread or queue.Queue.

    The semaine 4 pattern uses a single main loop with time.monotonic().
    Threading is taught later in the course.

    Expected: No threading or queue imports
    """
    script_path = REPO_ROOT / "main.py"

    if not script_path.exists():
        pytest.skip("main.py not found")

    content = script_path.read_text()

    has_threading = any([
        "import threading" in content,
        "from threading import" in content,
    ])

    has_queue = any([
        "import queue" in content,
        "from queue import" in content,
    ])

    if has_threading:
        pytest.fail(
            f"\n\n"
            f"Votre code utilise le module threading.\n"
            f"En semaine 4, on utilise le pattern timer-in-loop\n"
            f"avec time.monotonic() dans une seule boucle principale.\n\n"
            f"Le threading sera enseigne plus tard dans le cours.\n\n"
            f"Suggestion: Remplacez les threads par une boucle unique:\n"
            f"  import time  # PAS import threading\n"
            f"\n"
            f"  previous_sensor = time.monotonic()\n"
            f"  while True:\n"
            f"      current = time.monotonic()\n"
            f"      if current - previous_sensor >= SENSOR_INTERVAL:\n"
            f"          read_sensor()\n"
            f"          previous_sensor = current\n"
            f"      time.sleep(0.05)\n"
        )

    if has_queue:
        pytest.fail(
            f"\n\n"
            f"Votre code utilise le module queue.\n"
            f"En semaine 4, les donnees sont traitees directement\n"
            f"dans la boucle principale (pas de Queue entre threads).\n\n"
            f"Le pattern producteur-consommateur avec Queue sera\n"
            f"enseigne plus tard dans le cours.\n\n"
            f"Suggestion: Appelez vos fonctions directement:\n"
            f"  while True:\n"
            f"      if current - previous >= SENSOR_INTERVAL:\n"
            f"          read_sensor(sensor)  # Appel direct\n"
            f"          previous = current\n"
        )
