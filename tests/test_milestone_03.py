"""
Milestone 3: Bouton Polling et Arret Propre (40 points)
=======================================================

This milestone verifies that the student has:
1. Used CircuitPython digitalio for button polling
2. Implemented clean shutdown with break
3. Proper error handling in the main loop
4. KeyboardInterrupt handling for Ctrl+C

These tests verify code STRUCTURE for polling and shutdown patterns.
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
# Test 3.1: digitalio + board Import (10 points)
# ---------------------------------------------------------------------------
def test_digitalio_button_import():
    """
    Verify that the script imports digitalio and board (not gpiozero).

    Expected: 'import digitalio' and 'import board'

    Suggestion: Add digitalio and board imports for button handling:
        import board
        import digitalio
    """
    script_path = REPO_ROOT / "main.py"

    if not script_path.exists():
        pytest.skip("main.py not found")

    content = script_path.read_text()

    # Check for digitalio import
    has_digitalio = any([
        "import digitalio" in content,
        "from digitalio" in content,
    ])

    # Check for board import
    has_board = any([
        "import board" in content,
        "from board" in content,
    ])

    # Check for gpiozero (should NOT be present)
    has_gpiozero = any([
        "gpiozero" in content,
        "from gpiozero" in content,
    ])

    if has_gpiozero:
        pytest.fail(
            f"\n\n"
            f"Votre code utilise gpiozero.\n"
            f"Utilisez digitalio pour lire le bouton par polling,\n"
            f"comme montre dans la theorie semaine 4.\n\n"
            f"Suggestion: Remplacez gpiozero par digitalio:\n"
            f"  import board\n"
            f"  import digitalio\n"
        )

    if not has_digitalio or not has_board:
        missing = []
        if not has_digitalio:
            missing.append("digitalio")
        if not has_board:
            missing.append("board")
        pytest.fail(
            f"\n\n"
            f"Votre code n'importe pas {' et '.join(missing)}.\n"
            f"Ajoutez 'import board' et 'import digitalio' en haut\n"
            f"de votre script pour lire le bouton.\n\n"
            f"Suggestion:\n"
            f"  import board\n"
            f"  import digitalio\n"
        )


# ---------------------------------------------------------------------------
# Test 3.2: Button Polling Pattern (10 points)
# ---------------------------------------------------------------------------
def test_button_polling_pattern():
    """
    Verify that button polling with digitalio is used.

    Expected: digitalio configuration and button.value reading

    Suggestion: Configure and poll the button:
        button = digitalio.DigitalInOut(board.D17)
        button.direction = digitalio.Direction.INPUT
        button.pull = digitalio.Pull.UP
        # In the main loop:
        if not button.value:
            print("Bouton appuye!")
    """
    script_path = REPO_ROOT / "main.py"

    if not script_path.exists():
        pytest.skip("main.py not found")

    content = script_path.read_text()

    # Check for gpiozero callback patterns (should NOT be present)
    has_gpiozero_callback = any([
        "when_pressed" in content,
        "when_released" in content,
        "when_held" in content,
    ])

    if has_gpiozero_callback:
        pytest.fail(
            f"\n\n"
            f"Votre code utilise des callbacks gpiozero (when_pressed).\n"
            f"Utilisez plutot digitalio polling (button.value dans une boucle)\n"
            f"comme montre dans la theorie.\n\n"
            f"Suggestion: Remplacez le callback par du polling:\n"
            f"  button = digitalio.DigitalInOut(board.D17)\n"
            f"  button.direction = digitalio.Direction.INPUT\n"
            f"  button.pull = digitalio.Pull.UP\n"
            f"\n"
            f"  while True:\n"
            f"      if not button.value:\n"
            f"          print(\"Bouton appuye!\")\n"
            f"      time.sleep(0.05)\n"
        )

    # Check for digitalio polling patterns
    has_polling = any([
        "button.value" in content,
        ".value" in content and "digitalio" in content,
        "DigitalInOut" in content,
        "digitalio.DigitalInOut" in content,
        "Direction.INPUT" in content,
        "digitalio.Direction.INPUT" in content,
        "Pull.UP" in content,
        "digitalio.Pull.UP" in content,
    ])

    if not has_polling:
        pytest.fail(
            f"\n\n"
            f"Votre code doit lire le bouton par polling avec digitalio.\n"
            f"Configurez avec:\n"
            f"  button = digitalio.DigitalInOut(board.D17)\n"
            f"  button.direction = digitalio.Direction.INPUT\n"
            f"  button.pull = digitalio.Pull.UP\n\n"
            f"Puis lisez button.value dans la boucle principale:\n"
            f"  while True:\n"
            f"      if not button.value:\n"
            f"          print(\"Bouton appuye!\")\n"
            f"      time.sleep(0.05)\n"
        )


# ---------------------------------------------------------------------------
# Test 3.3: Break for Stop (10 points)
# ---------------------------------------------------------------------------
def test_break_for_stop():
    """
    Verify that break is used for clean shutdown from the main loop.

    Expected: 'break' keyword to exit the while True loop

    Suggestion: Use break to exit the main loop when button is held:
        while True:
            # ... timer and polling ...
            if button_held:
                print("Arret demande...")
                break
    """
    script_path = REPO_ROOT / "main.py"

    if not script_path.exists():
        pytest.skip("main.py not found")

    content = script_path.read_text()

    # Check for break keyword in the code
    has_break = "break" in content

    # Also check for hold detection logic (timing for button hold)
    has_hold_logic = any([
        re.search(r'hold|maintenu|held|pressed_time|press_start', content, re.IGNORECASE),
        # Check for a timing pattern related to button state
        re.search(r'button.*time|time.*button', content, re.IGNORECASE),
        # Check for a counter or duration pattern
        re.search(r'duration|compteur|count.*button|button.*count', content, re.IGNORECASE),
    ])

    if not has_break:
        pytest.fail(
            f"\n\n"
            f"Expected: 'break' pour sortir de la boucle principale\n"
            f"Actual: Aucun 'break' trouve dans le code\n\n"
            f"Suggestion: Utilisez break pour arreter le programme\n"
            f"quand le bouton est maintenu:\n"
            f"  while True:\n"
            f"      current_time = time.monotonic()\n"
            f"\n"
            f"      # Timer: lecture capteur\n"
            f"      if current_time - previous_sensor >= SENSOR_INTERVAL:\n"
            f"          read_sensor(sensor)\n"
            f"          previous_sensor = current_time\n"
            f"\n"
            f"      # Bouton: detection de maintien\n"
            f"      if not button.value:  # Bouton appuye\n"
            f"          if press_start is None:\n"
            f"              press_start = current_time\n"
            f"          elif current_time - press_start >= 2:\n"
            f"              print(\"Arret demande...\")\n"
            f"              break\n"
            f"      else:\n"
            f"          press_start = None\n"
            f"\n"
            f"      time.sleep(0.05)\n"
        )


# ---------------------------------------------------------------------------
# Test 3.4: Try/Except in Main Loop (5 points)
# ---------------------------------------------------------------------------
def test_error_handling():
    """
    Verify that the main loop includes error handling.

    Expected: try/except in main function and sensor reading

    WHY THIS MATTERS:
    Le code dans la boucle principale peut lever des exceptions
    (erreur I2C, capteur deconnecte, etc.). Toujours entourer
    le code de lecture du capteur et du bouton avec try/except
    pour eviter un crash du programme.

    Suggestion: Add error handling in the main loop:
        while True:
            try:
                current_time = time.monotonic()
                if current_time - previous >= SENSOR_INTERVAL:
                    read_sensor(sensor)
                    previous = current_time
            except Exception as e:
                print(f"Erreur: {e}")
            time.sleep(0.05)
    """
    script_path = REPO_ROOT / "main.py"

    if not script_path.exists():
        pytest.skip("main.py not found")

    content = script_path.read_text()

    # Count try/except blocks - should have at least 2
    try_count = content.count("try:")
    except_count = content.count("except")

    if try_count < 2 or except_count < 2:
        pytest.fail(
            f"\n\n"
            f"Expected: Multiple try/except blocks (at least 2)\n"
            f"Actual: Found {try_count} try blocks, {except_count} except blocks\n\n"
            f"WHY THIS MATTERS:\n"
            f"  Le code dans la boucle principale peut lever des exceptions\n"
            f"  (erreur I2C, capteur deconnecte, probleme GPIO).\n"
            f"  Sans try/except, une seule erreur arrete tout le programme.\n"
            f"  Votre capteur ou bouton peut sembler \"arreter de fonctionner\"\n"
            f"  sans message d'erreur.\n\n"
            f"Suggestion: Entourez le code sensible avec try/except:\n"
            f"  def read_sensor(sensor):\n"
            f"      try:\n"
            f"          temperature = sensor.temperature\n"
            f"          print(f\"Temp: {{temperature:.1f}} C\")\n"
            f"      except Exception as e:\n"
            f"          print(f\"Erreur lecture: {{e}}\")\n"
            f"\n"
            f"  # Dans la boucle principale:\n"
            f"  try:\n"
            f"      while True:\n"
            f"          # ... timer et polling ...\n"
            f"          time.sleep(0.05)\n"
            f"  except KeyboardInterrupt:\n"
            f"      print(\"Arret...\")\n"
        )


# ---------------------------------------------------------------------------
# Test 3.5: KeyboardInterrupt Handling (5 points)
# ---------------------------------------------------------------------------
def test_keyboard_interrupt():
    """
    Verify that KeyboardInterrupt is handled for clean Ctrl+C exit.

    Expected: except KeyboardInterrupt pattern

    Suggestion: Handle Ctrl+C gracefully:
        try:
            while True:
                # ... main loop ...
                time.sleep(0.05)
        except KeyboardInterrupt:
            print("Arret demande...")
        finally:
            button.deinit()
            print("Nettoyage termine.")
    """
    script_path = REPO_ROOT / "main.py"

    if not script_path.exists():
        pytest.skip("main.py not found")

    content = script_path.read_text()

    has_keyboard_interrupt = "KeyboardInterrupt" in content

    if not has_keyboard_interrupt:
        pytest.fail(
            f"\n\n"
            f"Expected: KeyboardInterrupt handling\n"
            f"Actual: No KeyboardInterrupt handler found\n\n"
            f"Suggestion: Handle Ctrl+C for clean exit:\n"
            f"  try:\n"
            f"      while True:\n"
            f"          # ... boucle principale ...\n"
            f"          time.sleep(0.05)\n"
            f"  except KeyboardInterrupt:\n"
            f"      print(\"Arret demande (Ctrl+C)...\")\n"
            f"  finally:\n"
            f"      button.deinit()\n"
            f"      print(\"Nettoyage termine.\")\n"
            f"\n"
            f"Le bloc finally s'execute toujours, meme apres Ctrl+C.\n"
            f"Utilisez-le pour liberer les ressources GPIO.\n"
        )
