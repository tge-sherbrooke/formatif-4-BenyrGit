# /// script
# requires-python = ">=3.9"
# dependencies = ["adafruit-blinka"]
# ///
"""
Local Hardware Validation for Formatif F4
==========================================

Run this script ON YOUR RASPBERRY PI to validate hardware setup.
It creates marker files that GitHub Actions will verify.

Usage:
    python3 validate_pi.py

The script will:
1. Verify digitalio (adafruit-blinka) is installed
2. Test button connection (if available)
3. Verify your main.py script (timer pattern)
4. Create marker files for GitHub Actions

After running successfully, commit and push the .test_markers/ folder.
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime


# ---------------------------------------------------------------------------
# Terminal Colors
# ---------------------------------------------------------------------------
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def success(msg):
    print(f"{Colors.GREEN}[PASS] {msg}{Colors.END}")


def fail(msg):
    print(f"{Colors.RED}[FAIL] {msg}{Colors.END}")


def warn(msg):
    print(f"{Colors.YELLOW}[WARN] {msg}{Colors.END}")


def info(msg):
    print(f"{Colors.BLUE}[INFO] {msg}{Colors.END}")


def header(msg):
    print(f"\n{Colors.BOLD}{'='*60}")
    print(f" {msg}")
    print(f"{'='*60}{Colors.END}\n")


# ---------------------------------------------------------------------------
# Marker Management
# ---------------------------------------------------------------------------
MARKERS_DIR = Path(__file__).parent / ".test_markers"


def create_marker(name, content):
    """Create a marker file for GitHub Actions verification."""
    MARKERS_DIR.mkdir(exist_ok=True)
    marker_path = MARKERS_DIR / f"{name}.txt"
    timestamp = datetime.now().isoformat()
    marker_path.write_text(f"Verified: {timestamp}\n{content}\n")
    info(f"Marker created: {marker_path.name}")


# ---------------------------------------------------------------------------
# Test: digitalio Installation
# ---------------------------------------------------------------------------
def check_digitalio():
    """Verify digitalio (adafruit-blinka) is installed and working."""
    header("DIGITALIO VERIFICATION")

    try:
        import board
        import digitalio
        success("digitalio imported successfully")
        create_marker("digitalio_verified", "digitalio available")
        return True
    except ImportError as e:
        fail(f"digitalio import failed: {e}")
        print("\n  Install with:")
        print("    pip install adafruit-blinka")
        print("\n  Note: adafruit-blinka provides digitalio and board modules")
        return False


# ---------------------------------------------------------------------------
# Test: Button (Optional)
# ---------------------------------------------------------------------------
def check_button():
    """Test button connection (optional)."""
    header("BUTTON TEST (Optional)")

    try:
        import board
        import digitalio

        button = digitalio.DigitalInOut(board.D17)
        button.direction = digitalio.Direction.INPUT
        button.pull = digitalio.Pull.UP

        info("Button initialized on GPIO 17 (digitalio polling)")
        info("Press the button within 5 seconds to test...")

        pressed = False
        start_time = time.time()

        try:
            while time.time() - start_time < 5 and not pressed:
                if not button.value:  # Pull-up: False = appuye
                    pressed = True
                    success("Button press detected!")
                time.sleep(0.05)
        finally:
            button.deinit()

        if pressed:
            create_marker("button_verified", "Button GPIO 17 working")
            return True
        else:
            warn("No button press detected - this is optional")
            return True  # Optional, don't fail

    except Exception as e:
        warn(f"Button test skipped: {e}")
        info("Button is optional for this formatif")
        return True


# ---------------------------------------------------------------------------
# Test: Script Validation
# ---------------------------------------------------------------------------
def check_main_script():
    """Verify main.py script uses timer pattern."""
    header("SCRIPT VALIDATION")

    script_path = Path(__file__).parent / "main.py"

    if not script_path.exists():
        fail("main.py not found")
        print("\n  Create your main.py script in the same folder.")
        return False

    success("main.py exists")

    # Check syntax
    try:
        with open(script_path) as f:
            compile(f.read(), script_path, 'exec')
        success("Python syntax is valid")
    except SyntaxError as e:
        fail(f"Syntax error on line {e.lineno}: {e.msg}")
        return False

    # Check required content
    content = script_path.read_text()
    checks = [
        ("import time", "time import"),
        ("__main__", "main guard"),
    ]

    all_present = True
    for pattern, desc in checks:
        if pattern in content:
            success(f"Found: {desc}")
        else:
            fail(f"Missing: {desc}")
            all_present = False

    # Check for digitalio (required for button polling)
    if "digitalio" in content:
        success("Found: digitalio import")
    else:
        fail("digitalio import not found (required for button polling)")
        all_present = False

    # Check for time.monotonic (required for timer pattern)
    if "time.monotonic" in content or "monotonic()" in content:
        success("Found: time.monotonic usage")
    else:
        fail("time.monotonic not found (required for timer pattern)")
        all_present = False

    if all_present:
        create_marker("main_script_verified", "Script structure valid")

    return all_present


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print(f"\n{Colors.BOLD}Formatif F4 - Local Hardware Validation{Colors.END}")
    print(f"{'='*60}\n")

    results = {}

    # Run all checks
    results["digitalio"] = check_digitalio()
    results["Button"] = check_button()
    results["Script"] = check_main_script()

    # Summary
    header("FINAL RESULTS")

    all_required_passed = results["digitalio"] and results["Script"]

    for test, passed in results.items():
        if passed:
            success(f"{test}: OK")
        elif test == "Button":
            warn(f"{test}: SKIPPED (optional)")
        else:
            fail(f"{test}: FAILED")

    print()

    if all_required_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}")
        print("=" * 60)
        print(" ALL REQUIRED TESTS PASSED!")
        print("=" * 60)
        print(f"{Colors.END}")

        create_marker("all_tests_passed", "All required validations completed")

        print("\nNext steps:")
        print("  git add .test_markers/")
        print("  git commit -m \"feat: validation locale completee\"")
        print("  git push")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}")
        print("=" * 60)
        print(" SOME TESTS FAILED - Fix issues and run again")
        print("=" * 60)
        print(f"{Colors.END}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
