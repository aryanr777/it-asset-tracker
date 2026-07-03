# 🛡️ EdgeShield IT Asset Tracker

A robust, lightweight Python CLI tool designed to manage, audit, and report on IT asset inventories. Built from real field experience, it provides system administrators and IT managers with a fast, terminal-based workflow for tracking device distribution, locations, and audit compliance using a simple, version-controllable CSV backend.

---

## ✨ Features

- **📊 Beautiful Terminal UI**: Powered by `rich` to output clean, color-coded interactive tables, status tags, and audit flags.
- **🔍 Advanced Filtering**: Query your inventory dynamically by location (e.g., Rydalmere, Blacktown) or lifecycle status (`active`, `offboarded`, `unassigned`).
- **👤 Instant Assignee Search**: Perform partial-name lookups to see all hardware currently checked out to a specific team member.
- **🚨 Compliance & Auditing**: Automatically flag active assets that have been assigned longer than a set threshold (default: 90 days).
- **📝 CSV-Backed Storage**: No heavy database required. Assets are stored in `assets.csv` for easy viewing, manual editing, and Git tracking.
- **📤 Plain-Text Export**: Export filtered reports to formatted `.txt` files for sharing or documentation.

---

## 🛠️ Tech Stack & Dependencies

- **Python 3.8+**
- [**Click**](https://click.palletsprojects.com/) (v8.3.3) — For building the robust Command Line Interface.
- [**Rich**](https://rich.readthedocs.io/) (v15.0.0) — For formatting tables, colors, and console output.
- **Standard Libraries**: Dataclasses, CSV, DateTime.

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/aryanr777/it-asset-tracker.git
cd it-asset-tracker
```

### 2. Set Up a Virtual Environment (Recommended)
To prevent package conflicts with global Python packages, create and activate a virtual environment:

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
Install the required packages listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

> [!TIP]
> If you encounter a `ModuleNotFoundError: No module named 'click'` or similar error when running the tracker, verify that your virtual environment is active, or explicitly invoke Python using the virtual environment's executable (e.g., `./.venv/Scripts/python main.py` on Windows).

---

## 📖 Usage Guide

Run `python main.py --help` to view all available commands and options.

```text
Usage: main.py [OPTIONS] COMMAND [ARGS]...

  EdgeShield IT Asset Tracker — manage and audit device inventories.

Options:
  --help  Show this message and exit.

Commands:
  add     Add a new asset to the inventory.
  audit   Flag active assets that have been assigned longer than --days.
  find    Find all assets assigned to a person (partial name match).
  list    List all assets, with optional filters.
  report  Export a full report to a text file.
```

### 1. List Inventory (`list`)
Display assets in a structured table. You can filter the list by location or status.

* **List all assets:**
  ```bash
  python main.py list
  ```
* **Filter by location:**
  ```bash
  python main.py list --location Rydalmere
  # Or shorthand
  python main.py list -l Blacktown
  ```
* **Filter by status:**
  ```bash
  python main.py list --status unassigned
  # Or shorthand
  python main.py list -s active
  ```

### 2. Find Assignee's Hardware (`find`)
Locate all devices assigned to a specific person. Supports partial name matching (case-insensitive).

```bash
python main.py find --assignee "Sarah"
# Or shorthand
python main.py find -a "Okafor"
```

### 3. Track Assignments and Run Audits (`audit`)
Identify devices that have been checked out for too long. By default, it flags active assets assigned for more than **90 days**, highlighting them with a `⚠` warning in the terminal.

* **Run audit with default 90-day threshold:**
  ```bash
  python main.py audit
  ```
* **Run audit with a custom threshold (e.g., 180 days):**
  ```bash
  python main.py audit --days 180
  # Or shorthand
  python main.py audit -d 180
  ```

### 4. Add a New Asset (`add`)
Quickly register a new asset into the tracking sheet. The asset is automatically marked as `active` with today's date.

```bash
python main.py add --tag LAP-0011 --model "MacBook Pro 16" --serial "SN-Z9Y8X7" --assignee "Jane Doe" --location "Rydalmere" --notes "New hire laptop"
```

*Required options*: `--tag`, `--model`, `--location`.
*Optional options*: `--serial`, `--assignee`, `--notes`.

### 5. Export Asset Reports (`report`)
Generate and save a plain-text report of your inventory.

* **Export full report:**
  ```bash
  python main.py report
  ```
* **Export report for a specific location to a custom file:**
  ```bash
  python main.py report --location Rydalmere --output rydalmere_report.txt
  ```

---

## 📂 Data Structure (`assets.csv`)

The tracker reads and writes directly to `assets.csv`. The schema contains the following columns:

| Column | Description | Example |
| :--- | :--- | :--- |
| `asset_tag` | Unique identifier for the hardware | `LAP-0001` |
| `model` | Manufacturer and model name | `Dell Latitude 5540` |
| `serial` | Hardware serial number | `SN-A1B2C3` |
| `assignee` | Name of the person the device is assigned to | `Sarah Chen` |
| `location` | Physical location or office site | `Rydalmere` |
| `status` | Device status (`active`, `offboarded`, `unassigned`) | `active` |
| `assigned_date` | Date the asset was assigned (`YYYY-MM-DD` or empty) | `2024-01-15` |
| `return_date` | Date the asset was returned (`YYYY-MM-DD` or empty) | `2024-03-01` |
| `notes` | Supplemental remarks or associations | `Primary work laptop` |

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! 
Feel free to open an issue or submit a pull request if you want to expand the auditing rules or add support for database backends.



