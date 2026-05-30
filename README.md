<!-- [START]
## Overview

TestSolver is a command-line bot that automates the resolution of self-assessment tests on the UNIR virtual campus. It handles login, course navigation, and test answering — supporting both single-choice and multi-choice question formats — and collects correction results when available.

Built with Selenium and `webdriver-manager` for zero-configuration Chrome driver setup.

## Scope

- **Authentication** — automated login to the UNIR platform via credentials in config
- **Course navigation** — supports one or multiple course IDs passed via configuration
- **Test resolution** — detects question type and selects answers; collects correction feedback when shown
- **Driver management** — uses `webdriver-manager` to handle Chrome WebDriver automatically

## Constraints

- Requires a real Chrome installation; Chromium forks may cause failures
- Incompatible with 2FA-protected accounts
- Dependent on UNIR's HTML structure — selector updates may be needed if the platform changes

## Status

Complete. Core automation flow is working. Selector maintenance may be needed over time.
[END]-->
# UNIR Test Bot

A command-line automation tool that logs into the UNIR virtual campus, enters the specified subjects, and resolves the available tests automatically using Selenium.

## Features

* Automates login to the UNIR platform
* Navigates into one or multiple courses
* Detects and answers test questions (single choice and multi-choice)
* Collects correction results when available
* Uses Chrome WebDriver automatically (via `webdriver-manager`)
* Scriptable from the command line

---

## Requirements

1. Clone the repository:

```bash
git clone https://github.com/AlvarodOrs/TestSolver.git
cd TestSolver
```

* Python 3.10+
* Google Chrome installed

Install dependencies:

```bash
pip install -r requirements.txt
```

This installs:

* selenium
* webdriver-manager

Everything else used in the project is part of the Python standard library.

---

## Usage

#### Get the COURSE_ID with:

![image](https://raw.githubusercontent.com/AlvarodOrs/TestSolver/refs/heads/main/img/get_int.png)

Click the wanted course (1), then copy the url code (2) and repeat with all desired courses.

#### Run the bot with:

```bash
python main.py
```

### Parameters to change on config.py

| Argument     | Required | Description                                |
| ------------ | -------- | ------------------------------------------ |
| `USERNAME` | Yes      | Your UNIR login email                      |
| `PASSWORD` | Yes      | Your UNIR campus password                  |
| `COURSES`  | Yes      | Comma-separated list of course identifiers |

Example:

```bash
python main.py
```

---

## Project Structure

```
project/
│
├── main.py             # Entry point
├── workers/            # Selenium automation logic
│   ├── __init__.py
│   ├── args.py
│   └── tools.py
│
├── utils.py
│   ├── __init__.py
│   ├── bot_launcher.py
│   ├── log_in.py
│   └── test.py
|
├── config.json
├── requirements.txt
└── README.md
```
## Notes

* Use a real Chrome installation; Chromium-based forks may cause failures.
* If your campus has 2FA enabled, the bot will not complete the login automatically.
* The automation depends on UNIR’s HTML structure; if UNIR updates the site, selectors may need adjustments.

---

## License

MIT License.
You are responsible for any use of this script on your own account.
