# wdadaptivepy

A python wrapper for the Workday Adaptive Planning API, providing an easy-to-use library to create, read, update, and delete data, metadata, and other information within Adaptive.

## Overview

[Workday Adaptive Planning](https://www.workday.com/en-us/products/adaptive-planning/overview.html) is a cloud-based planning, reporting, and analysis solution. This library simplifies interacting with the Adaptive Planning API via a Pythonic interface.

## Features

- Functionality
  - Retrieve information from Adaptive
    - Support for metadata
      - Account
      - Attributes
      - Currencies
      - Dimensions
      - Level
      - Time
      - Version
    - Support for data
      - Generic Data
      - Modeled Sheet Data
    - Support for users
      - Users
      - Groups
    - Support for security
      - Permission Sets
  - Support for data formats
    - Import/export data using JSON
    - Import/export data using XML
    - Export data using CSV
  - Helper functions
    - Get base/leaf members
    - Get parent/branch members
    - Get parent of a member
    - Get children of a member
    - Get ancestors of a member
    - Get descendents of a member

### Planned Features

- Functionality
  - Send information to Adaptive
    - Support for metadata
      - Account
      - Attributes
      - Currencies
      - Dimensions
      - Level
      - Time
      - Version
    - Support for data
      - Generic Data
      - Modeled Sheet Data
    - Support for users
      - Users
      - Groups
    - Support for security
      - Permission Sets
  - Integrations
    - Tasks
  - Support for data formats
    - Import/export data using XLSX
    - Import data using CSV
    - Import/export data using TXT
  - Helper functions
    - Get raw API requests
    - Get raw API responses
  - Logging
  - Workday Authentication Token

## Getting Started

### Pre-requisites

- Python 3.12+
- Valid credentials (username/password) for an active Workday Adaptive Planning account
  - wdadaptivepy will be limited to the access granted to the Adaptive user (ie: wdadaptivepy will respect Adaptive's user security)

### Installation

- Run `pip install wdadaptivepy`

## Example Usage

```python
from wdadaptivepy import AdaptiveConnection


adaptive = AdaptiveConnection(username="YOUR_ADAPTIVE@USER.NAME", password="Y0urP@$$w0rd!")

# Update Level names containing " - OLD"
levels = adaptive.levels.get_all()
for level in levels:
    level.name.replace(" - OLD", " - NEW")
# adaptive.levels.update(levels)  # Not currently implemented
```

## Documentatation

- wdadaptivepy
  - [wdadaptivepy Source Code](https://github.com/Revelwood/wdadaptivepy)
  - [wdadaptivepy Documentation](https://revelwood.github.io/wdadaptivepy)

- Workday Adaptive Planning
  - [Workday Adaptive Planning XML API Documentation](https://doc.workday.com/adaptive-planning/en-us/workday-adaptive-planning-documentation/integration/managing-data-integration/api-documentation/understanding-the-adaptive-planning-rest-api/api-methods/brk1623709249507.html?toc=11.0.4.1.3.0)
  - [Workday Adaptive Planning JSON API Documentation](https://doc.workday.com/adaptive-planning/en-us/workday-adaptive-planning-documentation/integration/managing-data-integration/api-documentation/json-apis/jyo1644861365611.html?toc=11.0.4.5.1)
  - [Workday Adaptive Planning API Changelog](https://doc.workday.com/adaptive-planning/en-us/workday-adaptive-planning-documentation/integration/managing-data-integration/api-documentation/understanding-the-adaptive-planning-rest-api/vmo1623708512342.html)

## Issues

Please submit an issue on the [GitHub repository](https://github.com/Revelwood/wdadaptivepy) for any bugs or issues that are found.

## Contribute

The preferred tools for developing wdadaptivepy are listed below. Other tools can be used, but the guide will assume the stack below is used.

- [Github (code repository)](https://github.com)
- [git (version control system)](https://github.com/git/git)
- [uv (Python manager, Python builder)](https://github.com/astral-sh/uv)
- [Visual Studio Code (editor)](https://github.com/microsoft/vscode)
- [ruff (linter, formatter)](https://github.com/astral-sh/ruff)
- [pyright (static type checker)](https://github.com/microsoft/pyright)
- [pytest (testing)](https://github.com/pytest-dev/pytest)
- [mkdocs-material (documentation)](https://github.com/squidfunk/mkdocs-material)

### Develop

1. Fork the [wdadaptivepy repo](https://github.com/Revelwood/wdadaptivepy/fork)
2. Git clone the forked repo onto your device (eg: `git clone git@github.com:YOUR_GITHUB_ACCOUNT/YOUR_FORKED_REPO_NAME.git`)
3. Within the cloned directory, run `uv sync --no-install-project` to create a Python virtual environment and install all dependencies
4. Complete any modifications to the source code
5. Ensure all modified code is covered by tests via `uv run pytest --cov`
6. Ensure all tests pass
7. Commit all changes (eg: `git commit -m "Added functionality for recent Adaptive release"`)
8. Create pull request for committed changes
