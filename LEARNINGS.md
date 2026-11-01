# LEARNINGS — Dynamic Test-Subset Routing

**Student:** Katakam Surya Teja | **USN:** 24BTRAO017
**Department:** CSE AI-Driven DevOps | **Academic Year:** 2026 – 2027

---

## 1. Git-Based Change Detection

**What I learned:**
`git diff --name-only <base> <head>` prints only the file paths that changed
between two commits, with no extra information. This is the ideal command when
you need a list of changed files rather than the actual diff content.

**Key insight:**
Using `subprocess.run(..., capture_output=True, text=True, check=True)` in
Python lets you execute Git commands safely, capture their output as a string,
and raise a `CalledProcessError` when Git exits non-zero — making error
handling explicit.

**Challenge encountered:**
On Windows, Git can return paths with backslashes or a leading `./`. The
`normalise()` helper was added specifically to convert any such variant into a
consistent forward-slash POSIX path before performing dictionary lookups.

---

## 2. Selective Pytest Execution

**What I learned:**
Pytest accepts individual file paths or directory paths as command-line
arguments. Passing `tests/test_auth.py` runs only auth tests; passing `tests/`
runs every test file in the directory. This makes targeted execution trivial.

**Key insight:**
Executing Pytest as a sub-process via:
```python
subprocess.run([sys.executable, "-m", "pytest", "-v"] + test_paths)
```
uses the _same_ Python interpreter that is running the router, which avoids
environment mismatch issues — important in CI containers where multiple Python
versions may be installed.

---

## 3. Module-to-Test Mapping

**What I learned:**
A simple Python dictionary (`MODULE_TO_TEST`) is sufficient to represent the
mapping between source files and test files. This is far easier to maintain
than a configuration file and can be extended without touching any logic.

**Best practice identified:**
The router must treat _test_ files and _configuration_ files (like
`requirements.txt`, `.gitignore`) as unknown changes that trigger the full
suite. Application modules are the only files with explicit entries in the
mapping.

---

## 4. Handling Multiple Changed Files

**What I learned:**
When more than one file changes in a commit, the router must:
1. Iterate over every changed file.
2. Check each one against the mapping.
3. Collect all mapped test paths into a set (to avoid duplicates).
4. Sort the set for reproducible output.

**Key insight:**
A `set` is the right data structure for collecting test paths because a test
file should only appear once in the selected list even if multiple application
files map to it (which doesn't happen in this project but is a good defensive
pattern).

---

## 5. Full-Suite Fallback

**What I learned:**
The fallback condition must cover two distinct cases:
- **Unknown file changed** — a file outside MODULE_TO_TEST was modified.
- **Empty change set** — `git diff` returned nothing (e.g., first commit, or
  Git references unavailable).

In both cases the router must _not_ silently skip tests. Running the full
suite is the only safe default.

**Challenge encountered:**
Deciding _when_ to fall back. The rule I settled on is: if _any single file_
in the diff is unknown, the entire selection falls back to `tests/`. This is
conservative but correct — partial execution when something unexpected changes
would be dangerous.

---

## 6. GitHub Actions Integration

**What I learned:**
GitHub Actions exposes different contexts depending on the event type:
- `pull_request` — `github.event.pull_request.base.sha` and `.head.sha`
- `push` — `github.event.before` (previous SHA) and `github.sha` (current)
- First push to a branch sets `github.event.before` to all zeros (`000...`),
  which must be detected and handled as a fallback trigger.

**Key insight:**
Using `fetch-depth: 0` in `actions/checkout@v4` ensures the full Git history
is available so that `git diff` between any two commits in the repository's
history will succeed.

**Best practice identified:**
Store the routing decision in a reusable shell step output (`$GITHUB_OUTPUT`)
so that subsequent steps can reference the resolved SHAs without repeating
the detection logic.

---

## 7. Challenges and Solutions

| Challenge | Root Cause | Solution |
|---|---|---|
| `ModuleNotFoundError` on `from src.auth import login` | Pytest working directory not set to project root | Run `pytest` from project root; Python finds packages correctly |
| `git diff` returns empty on first commit | No previous commit exists | Detect zero SHA in CI; use full-suite fallback |
| Windows path separators in git output | OS-level path differences | `normalise()` converts `\` → `/` and strips `./` |
| Duplicate test paths in output | Same test file mapped from two modules | Collect into a `set`, then sort |
| CI fails on `workflow_dispatch` | No push/PR SHAs available | Leave SHAs empty → router detects missing refs → full suite |

---

## Summary

Building a dynamic test-subset router taught me:
- How Git exposes change information through its CLI.
- How to drive Pytest programmatically rather than only from the terminal.
- Why safe fallback logic matters more than clever optimisation.
- How CI/CD pipelines can use commit metadata to make intelligent decisions.
- The importance of normalising file paths for cross-platform correctness.

These skills are directly applicable to real-world DevOps pipelines where test
execution time and reliability are both critical concerns.

