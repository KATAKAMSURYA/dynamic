# Screenshot Guide — Dynamic Test-Subset Routing

**Student:** Katakam Surya Teja | **USN:** 24BTRAO017
**Department:** CSE AI-Driven DevOps | **Academic Year:** 2026 – 2027

> Take each screenshot in the exact order shown. Use a consistent terminal
> (VS Code integrated terminal or macOS Terminal). Name files exactly as shown.

---

## Screenshot 1 — Python Environment & Pytest Installation

**Application:** Terminal / VS Code integrated terminal
**Commands to run:**
```bash
cd Dynamic-Test-Subset-Routing
python --version
python -m pip install -r requirements.txt
python -m pip show pytest
```
**Expected visible output:**
- `Python 3.12.x`
- pip install progress/success messages
- Pytest version `8.x.x`

**Filename:** `01_python_env_pytest_install.png`

---

## Screenshot 2 — VS Code Project Structure

**Application:** Visual Studio Code
**Steps:**
1. Open VS Code.
2. File → Open Folder → select `Dynamic-Test-Subset-Routing/`.
3. Expand the Explorer panel (left sidebar) to show the full tree.
**Expected visible output:**
- `.github/workflows/test-routing.yml`
- `router/test_router.py`
- `src/auth.py`, `src/payment.py`, `src/user.py`
- `tests/test_auth.py`, `tests/test_payment.py`, `tests/test_user.py`, `tests/test_router.py`
- `.gitignore`, `requirements.txt`, `README.md`, `LEARNINGS.md`

**Filename:** `02_vscode_project_structure.png`

---

## Screenshot 3 — Initial Full Test Suite (10 Passed)

**Application:** Terminal
**Command:**
```bash
python -m pytest -v
```
**Expected visible output:**
```
tests/test_auth.py::TestLogin::test_valid_login_admin PASSED
...
============ X passed in Y.YYs ============
```
All tests pass. Confirm the total count shown.

**Filename:** `03_full_suite_all_passed.png`

---

## Screenshot 4 — Git Initialisation & Initial Commit

**Application:** Terminal
**Commands:**
```bash
git init
git add .
git commit -m "Initial project setup"
git log --oneline
```
**Expected visible output:**
- `Initialized empty Git repository …`
- `[main (root-commit) xxxxxxx] Initial project setup`
- Single commit in `git log --oneline`

**Filename:** `04_git_init_initial_commit.png`

---

## Screenshot 5 — Experiment 1: Authentication-Only Routing

**Application:** Terminal
**Commands:**
```bash
# (After modifying src/auth.py and committing it)
python router/test_router.py --base <BASE_SHA> --head <HEAD_SHA>
```
**Expected visible output:**
- `Changed files: src/auth.py`
- `Selected test path(s): → tests/test_auth.py`
- Pytest output: `2 passed`

**Filename:** `05_experiment1_auth_only.png`

---

## Screenshot 6 — Experiment 2: Payment-Only Routing

**Application:** Terminal
**Commands:**
```bash
# (After modifying src/payment.py and committing it)
python router/test_router.py --base <BASE_SHA> --head <HEAD_SHA>
```
**Expected visible output:**
- `Changed files: src/payment.py`
- `Selected test path(s): → tests/test_payment.py`
- Pytest output: `2 passed`

**Filename:** `06_experiment2_payment_only.png`

---

## Screenshot 7 — Experiment 3: User-Only Routing

**Application:** Terminal
**Commands:**
```bash
# (After modifying src/user.py and committing it)
python router/test_router.py --base <BASE_SHA> --head <HEAD_SHA>
```
**Expected visible output:**
- `Changed files: src/user.py`
- `Selected test path(s): → tests/test_user.py`
- Pytest output: `2 passed`

**Filename:** `07_experiment3_user_only.png`

---

## Screenshot 8 — Experiment 4: Multiple-Module Routing

**Application:** Terminal
**Commands:**
```bash
# (After modifying src/auth.py AND src/payment.py and committing both)
python router/test_router.py --base <BASE_SHA> --head <HEAD_SHA>
```
**Expected visible output:**
- `Changed files: src/auth.py, src/payment.py`
- `Selected test path(s): → tests/test_auth.py, → tests/test_payment.py`
- Pytest output: `4 passed`

**Filename:** `08_experiment4_multiple_modules.png`

---

## Screenshot 9 — Experiment 5: Shared-File Fallback

**Application:** Terminal
**Commands:**
```bash
# (After modifying requirements.txt and committing it)
python router/test_router.py --base <BASE_SHA> --head <HEAD_SHA>
```
**Expected visible output:**
- `'requirements.txt' is not a tracked application module — falling back to full test suite.`
- `Selected test path(s): → tests/`
- Pytest output: total tests passed

**Filename:** `09_experiment5_fallback.png`

---

## Screenshot 10 — GitHub Actions Workflow YAML

**Application:** VS Code (or GitHub web editor)
**Steps:**
1. Open `.github/workflows/test-routing.yml` in VS Code.
2. Ensure the full file content is visible.
**Expected visible output:**
- `on: push / pull_request / workflow_dispatch`
- Steps: checkout, setup-python, install deps, determine SHAs, run router

**Filename:** `10_github_actions_yaml.png`

---

## Screenshot 11 — GitHub Repository Page

**Application:** Web browser (GitHub)
**Steps:**
1. Navigate to `https://github.com/<your-username>/Dynamic-Test-Subset-Routing`.
2. Ensure the repository is visible with all files in the file tree.
**Expected visible output:**
- Repository name
- All folders: `.github/`, `router/`, `src/`, `tests/`
- `README.md` rendered below the file tree

**Filename:** `11_github_repo_page.png`

---

## Screenshot 12 — Successful GitHub Actions Workflow

**Application:** Web browser (GitHub)
**Steps:**
1. Go to the **Actions** tab of your repository.
2. Click the latest workflow run triggered by a push to `main`.
3. Confirm all steps show a green ✅ checkmark.
**Expected visible output:**
- Workflow name: `Dynamic Test-Subset Routing`
- All steps green
- Summary shows tests passed

**Filename:** `12_github_actions_success.png`

---

## Naming Convention Summary

| # | Filename |
|---|---|
| 1 | `01_python_env_pytest_install.png` |
| 2 | `02_vscode_project_structure.png` |
| 3 | `03_full_suite_all_passed.png` |
| 4 | `04_git_init_initial_commit.png` |
| 5 | `05_experiment1_auth_only.png` |
| 6 | `06_experiment2_payment_only.png` |
| 7 | `07_experiment3_user_only.png` |
| 8 | `08_experiment4_multiple_modules.png` |
| 9 | `09_experiment5_fallback.png` |
| 10 | `10_github_actions_yaml.png` |
| 11 | `11_github_repo_page.png` |
| 12 | `12_github_actions_success.png` |
