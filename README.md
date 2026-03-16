# 🤖 Form Automation with Playwright

A Python-based automation tool that uses [Playwright](https://playwright.dev/python/) to automatically fill out a multi-page Google Form with randomized, realistic responses. Designed for survey automation where multiple respondents need to submit responses programmatically.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Approaches](#approaches)
- [Tracing & Debugging](#tracing--debugging)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

This project automates the submission of a Google Form survey focused on **Supply Chain Management** practices — covering areas like Strategic Purchasing, Supplier Management, Quality Systems, Cost Management, and Delivery Performance. The tool reads a list of respondents (email + gender) and submits a form for each one with randomized answers, simulating real-world survey responses.

---

## Features

- ✅ Automates multi-page Google Form submissions
- ✅ Supports multiple respondents from a JSON file or Python list
- ✅ Randomizes answers for demographic and Likert-scale questions
- ✅ Handles bilingual form elements (Dutch `Volgende` / English `Next`)
- ✅ Built-in Playwright tracing for debugging (screenshots + network snapshots)
- ✅ Two implementation approaches for flexibility

---

## Project Structure

```
form-automation/
│
├── autoForm.py              # Approach 1: Reads respondents from responder.json
├── autoForm-approach2.py    # Approach 2: Reads respondents from data.py (Python list)
├── data.py                  # Respondent data as a Python list of dicts
├── responder.json           # Respondent data as a JSON array
├── requirements.txt         # Python dependencies
├── trace.zip                # Playwright trace output (auto-generated, git-ignored)
├── .gitignore               # Git ignore rules
└── README.md                # Project documentation
```

---

## Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)
- A valid **Google Form URL** (the target form)

---

## Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd form-automation
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate        # On Linux/macOS
# .venv\Scripts\activate         # On Windows
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browser Binaries

After installing the Python package, you **must** also install the browser binaries:

```bash
playwright install chromium
```

> If you encounter system dependency errors (common on Linux), run:
> ```bash
> playwright install-deps chromium
> ```

---

## Configuration

### Respondent Data

You can configure respondents in **two ways** depending on which script you use:

#### Option A — `responder.json` (used by `autoForm.py`)

Edit `responder.json` to add one or more respondents:

```json
[
    {
        "email": "alice@example.com",
        "gender": "Female"
    },
    {
        "email": "bob@example.com",
        "gender": "Male"
    }
]
```

#### Option B — `data.py` (used by `autoForm-approach2.py`)

Edit the `entries` list in `data.py`:

```python
entries = [
    {
        "email": "alice@example.com",
        "gender": "Female"
    },
    {
        "email": "bob@example.com",
        "gender": "Male"
    }
]
```

### Form URL

The target Google Form URL is hardcoded in both scripts. To point to a different form, update the `formURL` variable at the top of the relevant script:

```python
formURL = "https://forms.gle/your-form-id-here"
```

---

## Usage

### Run Approach 1 (JSON-based)

```bash
python autoForm.py
```

### Run Approach 2 (Python data list-based)

```bash
python autoForm-approach2.py
```

Both scripts will launch a **visible Chromium browser** (non-headless), navigate to the form, and fill it out for each respondent. A `trace.zip` file is generated in the project root after execution.

> **Tip:** To run headlessly (no browser window), change `headless=False` to `headless=True` in the script. Note that some Google Forms may behave differently in headless mode.

---

## How It Works

The form is divided into **3 pages**, each automated as follows:

### Page 1 — Respondent Demographics

| Field                        | Source                          |
|------------------------------|---------------------------------|
| Email                        | From `responder.json` / `data.py` |
| Gender                       | From `responder.json` / `data.py` |
| Age Range                    | Random from `["21-30", "31-40"]` |
| Organisational Experience    | Random from `["<4", "4-8", "9-12", ">12"]` |
| Overall Experience           | Random from `["<5", "5-10", "11-15", ">15"]` |
| Designation                  | Random from `["Worker", "Manager", "Senior Manager", "General Manager"]` |
| Department                   | Random from `["Operations", "Supply Chain"]` |
| Level of Management          | Random from `["Bottom", "Middle", "Top"]` |

### Page 2 — Survey Questions (Likert Scale)

30 questions across four categories are answered with a randomly selected Likert response:

- `Strongly Agree` / `Agree` / `Neutral` / `Disagree` / `Strongly Disagree`

**Categories covered:**
- **Strategic Purchasing** (6 questions)
- **Supplier Management Practices** (7 questions)
- **Quality System** (8 questions)
- **Cost Management Practices** (4 questions)
- **Delivery Performance** (5 questions)

### Page 3 — Factor Ranking

Five supply chain factors are each assigned a random rank:

| Factor     | Rank Options                          |
|------------|---------------------------------------|
| Quality    | Rank 1 – Rank 5 (randomly assigned)  |
| Price      | Rank 1 – Rank 5 (randomly assigned)  |
| Quantity   | Rank 1 – Rank 5 (randomly assigned)  |
| Service    | Rank 1 – Rank 5 (randomly assigned)  |
| Innovation | Rank 1 – Rank 5 (randomly assigned)  |

---

## Approaches

### Approach 1 — `autoForm.py`

- Reads respondent data from **`responder.json`**
- Uses **explicit label-based locators** for Page 2 (matches exact question text + language-specific answer labels, e.g., `"Strongly Agree, antwoord voor <question>"`)
- More brittle but more precise — tightly coupled to the form's label text

### Approach 2 — `autoForm-approach2.py`

- Reads respondent data from **`data.py`**
- Uses **generic role-based locators** for Pages 2 & 3:
  ```python
  for radio_group in page.get_by_role('radiogroup').all():
      radio_group.get_by_role('radio').nth(random.randint(0, 4)).click()
  ```
- More robust and language-agnostic — works even if form labels change
- The final Submit button click is commented out by default (safety measure)

---

## Tracing & Debugging

Both scripts enable **Playwright Tracing**, which records a full trace of the automation run including:

- Screenshots at every step
- Network request/response snapshots
- Source context

The trace is saved as `trace.zip` in the project root. To inspect it:

```bash
playwright show-trace trace.zip
```

> `trace.zip` is listed in `.gitignore` and will not be committed to version control.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: playwright` | Run `pip install -r requirements.txt` inside your virtual environment |
| Browser binary not found | Run `playwright install chromium` |
| Missing system dependencies (Linux) | Run `playwright install-deps chromium` |
| `TimeoutError` during form fill | The form page may have loaded slowly; try increasing timeouts or checking your internet connection |
| Form fields not found | The Google Form UI may have changed; inspect the form manually and update locator selectors |
| `TypeError: list indices must be integers or slices, not str` | Ensure `responder.json` is a **JSON array** (`[{...}]`), not a plain object (`{...}`) |

---

## License

This project is licensed under the **Apache License 2.0**. See the [LICENSE](./LICENSE) file for details.