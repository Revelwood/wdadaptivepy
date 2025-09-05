# Installation

## Requirements

- [Python 3.12](https://docs.python.org/3/whatsnew/3.12.html) or greater

## Basic Installation

`wdadaptivepy` is available on [Python Package Index (PyPI)](https://pypi.org/), the standard Python package repository.

```sh
pip install wdadaptivepy
```

## Recommended Installation

The recommended way to install `wdadaptivepy` is via [uv](https://github.com/astral-sh/uv). However, it can be installed via `pip` as well.

=== "uv"

    ```sh hl_lines="4"
    mkdir myProject
    cd myProject
    uv init
    uv add wdadaptivepy
    ```

=== "pip"

    ```sh hl_lines="5"
    mkdir myProject
    cd myProject
    python3 -m venv .venv  # or `python -m venv .venv`
    source .venv/bin/activate # Windows should be `.venv\Scripts\activate`
    pip install wdadaptivepy
    ```

## Additional Features

### Workday Authentication

`wdadaptivepy` supports authenticating via Workday, but it requires an additional package.

=== "uv"

    ```sh
    uv add wdadaptivepy[workday]
    ```

=== "pip"

    ```sh
    pip install wdadaptivepy[workday]
    ```
