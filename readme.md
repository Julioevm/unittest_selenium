# Automated UI Test with Python's unittest and Selenium

This is a simple python script to demonstrate basic usage of selenium.
We have 3 brief tests that check different functions of eggtimer.com using selenium.

## Requirements

See requirements.txt

## Usage

Clone the repo and install the required python packages. I recomend to use venv to keep them within the project.

Use  to run the entire test suite:

`python3 -m unittest eggTimer.py`

Or run a specific test case:

`python3 -m unittest eggTimer.EggTimerTests.test_basic_alarm`