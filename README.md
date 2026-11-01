# Dynamic Test-Subset Routing

| Field | Details |
|---|---|
| **Student Name** | Katakam Surya Teja |
| **USN** | 24BTRAO017 |
| **Department** | CSE AI-Driven DevOps |
| **Academic Year** | 2026 – 2027 |
| **Assignment** | Assignment 2 – Dynamic Test-Subset Routing |

---

## Introduction

Modern software projects accumulate large test suites. Running every test on every commit wastes CI/CD time and resources. **Dynamic Test-Subset Routing** solves this by inspecting which source files changed in a Git commit and executing _only_ the corresponding Pytest files. When a change cannot be safely mapped to a known module, the entire test suite runs as a safety net.

---

## Problem Statement

Given a Python project with multiple independent modules, design and implement a routing engine that:

1. Detects which application files were modified between two Git references.
2. Maps each changed file to its dedicated test file.
3. Executes only the selected tests, saving time and compute.
4. Falls back to the full test suite when unknown or shared files change.

---

## Objectives

- Understand Git-based change detection using `git diff --name-only`.
- Build a module-to-test mapping in Python.
- Implement selective Pytest execution via `subprocess`.
- Handle edge cases: empty diff, unknown files, multiple simultaneous changes.
- Integrate the router into a GitHub Actions CI/CD pipeline.

---

## Technologies

| Technology | Version / Tool | Purpose |
|---|---|---|
| Python | 3.12 | Implementation language |
| Pytest | ≥ 8.0 | Test framework |
| Git | Any modern | Change detection |
| GitHub | — | Source hosting |
| GitHub Actions | ubuntu-latest | CI/CD pipeline |
| YAML | — | Workflow configuration |
| VS Code | — | Development IDE |

---

## Architecture

```
Git Diff (base → head)
        │
        ▼
  git_changed_files()
        │
        ▼
   normalise() each path
        │
        ▼
   select_tests()
   ┌────────────────────────────┐
   │ Known module? → add test   │
   │ Unknown file? → full suite │
   │ Empty diff?  → full suite  │
   └────────────────────────────┘
        │
        ▼
   run_tests(selected_paths)
        │
        ▼
   pytest -v [path(s)]
```

---

## Folder Structure

```
Dynamic-Test-Subset-Routing/
├── .github/
│   └── workflows/
│       └── test-routing.yml      ← GitHub Actions CI/CD
├── router/
│   ├── __init__.py
│   └── test_router.py            ← Routing engine + CLI entry point
├── src/
│   ├── __init__.py
│   ├── auth.py                   ← Authentication module
│   ├── payment.py                ← Payment module
│   └── user.py                   ← User Management module
├── tests/
│   ├── test_auth.py              ← Auth tests (2 test classes)
│   ├── test_payment.py           ← Payment tests (2 test classes)
│   ├── test_user.py              ← User tests (2 test classes)
│   └── test_router.py            ← Router unit tests (4 scenarios)
├── .gitignore
├── requirements.txt
├── README.md
├── LEARNINGS.md
└── SCREENSHOT_GUIDE.md
```

---

## Application Modules

### A. Authentication — `src/auth.py`

```python
login(username: str, password: str) -> bool
```

Validates credentials against an in-memory store. Returns `True` for correct, non-empty credentials; `False` otherwise. Rejects empty username or password immediately.

---

### B. Payment — `src/payment.py`

```python
process_payment(amount: float) -> bool
```

Accepts amounts in the range `[0.01, 10 000.00]`. Returns `False` for zero, negative values, or amounts exceeding the upper limit.

---

### C. User Management — `src/user.py`

```python
create_user(name: str, email: str) -> dict | None
```

Validates a non-empty name and a basic e-mail pattern. Returns `{"name": …, "email": …}` on success, `None` on failure.

---

## Routing Engine — `router/test_router.py`

### Module-to-Test Mapping

| Changed File | Test Executed |
|---|---|
| `src/auth.py` | `tests/test_auth.py` |
| `src/payment.py` | `tests/test_payment.py` |
| `src/user.py` | `tests/test_user.py` |
| Any unknown file | `tests/` (full suite) |
| Empty change set | `tests/` (full suite) |

### Key Functions

| Function | Responsibility |
|---|---|
| `normalise(path)` | Strips `./`, converts `\` → `/` |
| `git_changed_files(base, head)` | Runs `git diff --name-only`; returns sorted list |
| `select_tests(files)` | Applies routing rules; returns test paths |
| `run_tests(test_paths)` | Executes `pytest -v`; returns exit code |
| `main(argv)` | CLI entry point; wires everything together |

---

## Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/Dynamic-Test-Subset-Routing.git
cd Dynamic-Test-Subset-Routing

# Create and activate a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
python -m pip install -r requirements.txt
```

---

## Execution Commands

### Run full test suite

```bash
python -m pytest -v
```

Expected: **10 tests passed** (2 auth + 2 payment + 2 user + 4 router).

### Run the routing engine manually

```bash
python router/test_router.py --base <BASE_COMMIT> --head <HEAD_COMMIT>
```

---

## Git Experiments

### Setup

```bash
git init
git add .
git commit -m "Initial project setup"
```

### Experiment 1 — Authentication-only change

```bash
# Edit src/auth.py (add a comment or new credential)
git add src/auth.py
git commit -m "Experiment 1: modify auth module"
BASE=$(git rev-parse HEAD~1)
HEAD=$(git rev-parse HEAD)
python router/test_router.py --base $BASE --head $HEAD
# Expected: tests/test_auth.py → 2 passed
```

### Experiment 2 — Payment-only change

```bash
git add src/payment.py
git commit -m "Experiment 2: modify payment module"
BASE=$(git rev-parse HEAD~1)
HEAD=$(git rev-parse HEAD)
python router/test_router.py --base $BASE --head $HEAD
# Expected: tests/test_payment.py → 2 passed
```

### Experiment 3 — User-only change

```bash
git add src/user.py
git commit -m "Experiment 3: modify user module"
BASE=$(git rev-parse HEAD~1)
HEAD=$(git rev-parse HEAD)
python router/test_router.py --base $BASE --head $HEAD
# Expected: tests/test_user.py → 2 passed
```

### Experiment 4 — Multiple-module change

```bash
git add src/auth.py src/payment.py
git commit -m "Experiment 4: modify auth and payment"
BASE=$(git rev-parse HEAD~1)
HEAD=$(git rev-parse HEAD)
python router/test_router.py --base $BASE --head $HEAD
# Expected: tests/test_auth.py + tests/test_payment.py → 4 passed
```

### Experiment 5 — Shared-file fallback

```bash
git add requirements.txt
git commit -m "Experiment 5: update requirements"
BASE=$(git rev-parse HEAD~1)
HEAD=$(git rev-parse HEAD)
python router/test_router.py --base $BASE --head $HEAD
# Expected: tests/ (full suite) → 10 passed
```

---

## Expected Routing Scenarios

| Scenario | Changed Files | Tests Selected | Expected |
|---|---|---|---|
| Auth only | `src/auth.py` | `tests/test_auth.py` | 2 passed |
| Payment only | `src/payment.py` | `tests/test_payment.py` | 2 passed |
| User only | `src/user.py` | `tests/test_user.py` | 2 passed |
| Auth + Payment | `src/auth.py`, `src/payment.py` | `tests/test_auth.py`, `tests/test_payment.py` | 4 passed |
| Unknown file | `requirements.txt` | `tests/` | 10 passed |
| Empty diff | _(none)_ | `tests/` | 10 passed |

---

## Test Results Summary

| Test File | Tests | Status |
|---|---|---|
| `tests/test_auth.py` | 6 | ✅ Passed |
| `tests/test_payment.py` | 6 | ✅ Passed |
| `tests/test_user.py` | 5 | ✅ Passed |
| `tests/test_router.py` | 8 | ✅ Passed |

---

## GitHub Actions

The workflow file `.github/workflows/test-routing.yml` triggers on:

- **Push** to `main` — compares `github.event.before` → `github.sha`
- **Pull Request** to `main` — compares PR base → PR head SHA
- **Manual dispatch** (`workflow_dispatch`) — full-suite fallback

Steps:
1. Checkout with full Git history (`fetch-depth: 0`)
2. Set up Python 3.12
3. Install `requirements.txt`
4. Determine base/head SHAs
5. Execute `python router/test_router.py --base … --head …`

The workflow **fails** if any selected tests fail, providing a genuine quality gate.

---

## Conclusion

This project demonstrates that selective test execution is achievable with a small amount of Python and Git knowledge. The router correctly identifies changed modules, maps them to tests, and provides a reliable full-suite fallback for safety. Integrating this pattern into GitHub Actions brings the benefits of fast, targeted CI to any Python project.

