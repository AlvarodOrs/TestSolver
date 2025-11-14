# Web Automation Bot

A Python-based web automation framework using Selenium for automating browser tasks.

## Features

- Browser automation with Selenium
- Support for Chrome (with automatic driver management)
- Easy-to-use API for common automation tasks
- Modular worker system for specific automation tasks

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. For Playwright (optional), install browsers:
```bash
playwright install
```

## Usage

### Basic Example

```python
from main import WebAutomation

# Create automation instance
automation = WebAutomation(headless=False)

try:
    # Navigate to a website
    automation.navigate("https://www.example.com")
    
    # Click an element
    automation.click(By.ID, "button-id")
    
    # Type text
    automation.type_text(By.NAME, "username", "myusername")
    
finally:
    automation.close()
```

### Using Workers

```python
from bot_launcher import launch_bot
import workers

automation = launch_bot(headless=False)

try:
    # Login
    workers.logIn(automation)
    
    # Find and click on courses
    workers.find_and_click_courses(automation)
finally:
    automation.close()
```

## Available Methods

- `navigate(url)` - Navigate to a URL
- `click(by, value)` - Click an element
- `type_text(by, value, text)` - Type text into an input
- `find_element(by, value)` - Find an element
- `get_text(by, value)` - Get text from an element
- `wait_for_element(by, value)` - Wait for element to appear

## Browser Options

- `headless=True` - Run browser without GUI
- `browser="chrome"` - Choose browser (currently only Chrome supported)

## Notes

- ChromeDriver is automatically downloaded and managed via webdriver-manager
- Make sure Chrome browser is installed on your system

