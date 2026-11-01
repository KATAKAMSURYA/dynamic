"""
Dynamic Test-Subset Router
==========================
Detects which application source files changed between two Git references
and executes only the corresponding Pytest test files.

If any changed file cannot be mapped to a known test, or if the change
set is empty / Git references are unavailable, the entire tests/ directory
is executed as a safe fallback.

Author  : Katakam Surya Teja
USN     : 24BTRAO017
Dept    : CSE AI-Driven DevOps
Academic: 2026-2027
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import PurePosixPath

# ---------------------------------------------------------------------------
# Module → Test mapping
# ---------------------------------------------------------------------------

MODULE_TO_TEST: dict[str, str] = {
    "src/auth.py": "tests/test_auth.py",
    "src/payment.py": "tests/test_payment.py",
    "src/user.py": "tests/test_user.py",
}

# Full-suite fallback target
FULL_SUITE: str = "tests/"

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------


def normalise(path: str) -> str:
    """
    Normalise a raw file path returned by Git into a consistent
    repository-relative POSIX path with no leading ``./``.

    Parameters
    ----------
    path : str
        Raw path string, possibly with Windows separators or a leading ``./``.

    Returns
    -------
    str
        Cleaned, POSIX-style, repository-relative path string.

    Examples
    --------
    >>> normalise(".\\\\src\\\\auth.py")
    'src/auth.py'
    >>> normalise("./src/auth.py")
    'src/auth.py'
    """
    # Normalise Windows back-slashes → forward slashes
    normalised = path.replace("\\", "/")
    # Strip a leading "./"
    if normalised.startswith("./"):
        normalised = normalised[2:]
    return normalised.strip()


def git_changed_files(base: str, head: str) -> list[str]:
    """
    Return the list of file paths that differ between *base* and *head*
    by executing ``git diff --name-only``.

    Parameters
    ----------
    base : str
        Base Git reference (commit SHA, branch name, tag, …).
    head : str
        Head Git reference to compare against *base*.

    Returns
    -------
    list[str]
        Sorted list of repository-relative POSIX paths.
        Returns an empty list when the command fails or produces no output.
    """
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", base, head],
            capture_output=True,
            text=True,
            check=True,
        )
        lines = [normalise(line) for line in result.stdout.splitlines() if line.strip()]
        return sorted(set(lines))
    except subprocess.CalledProcessError as exc:
        print(
            f"[router] ⚠  git diff failed (base={base!r}, head={head!r}): {exc.stderr.strip()}",
            file=sys.stderr,
        )
        return []
    except FileNotFoundError:
        print("[router] ⚠  'git' executable not found on PATH.", file=sys.stderr)
        return []


# ---------------------------------------------------------------------------
# Core routing logic
# ---------------------------------------------------------------------------


def select_tests(files: list[str]) -> list[str]:
    """
    Map a list of changed files to the test paths that should be executed.

    Routing Rules
    -------------
    1. If *files* is empty → full-suite fallback.
    2. For every changed file:
       - If it is in MODULE_TO_TEST → add its corresponding test file.
       - Otherwise → trigger full-suite fallback immediately.
    3. De-duplicate and sort the selected paths before returning.

    Parameters
    ----------
    files : list[str]
        Repository-relative POSIX paths of changed files.

    Returns
    -------
    list[str]
        Sorted, de-duplicated list of test paths to pass to Pytest.
        Guaranteed to be non-empty.

    Examples
    --------
    >>> select_tests(["src/auth.py"])
    ['tests/test_auth.py']

    >>> select_tests(["requirements.txt"])
    ['tests/']

    >>> select_tests([])
    ['tests/']
    """
    # Scenario 6: empty change set → full suite
    if not files:
        print("[router] No changed files detected — running full test suite (fallback).")
        return [FULL_SUITE]

    selected: set[str] = set()

    for f in files:
        if f in MODULE_TO_TEST:
            selected.add(MODULE_TO_TEST[f])
        else:
            # Scenario 5: unknown / shared file → full suite
            print(
                f"[router] '{f}' is not a tracked application module "
                "— falling back to full test suite."
            )
            return [FULL_SUITE]

    # Scenarios 1-4: all changed files were known application modules
    return sorted(selected)


# ---------------------------------------------------------------------------
# Test execution
# ---------------------------------------------------------------------------


def run_tests(test_paths: list[str]) -> int:
    """
    Execute Pytest on the provided *test_paths* using the current Python
    interpreter and return the process exit code.

    Parameters
    ----------
    test_paths : list[str]
        Test file or directory paths to pass to Pytest.

    Returns
    -------
    int
        Pytest's exit code (0 = all passed, non-zero = failure/error).
    """
    cmd = [sys.executable, "-m", "pytest", "-v"] + test_paths
    print(f"\n[router] Running: {' '.join(cmd)}\n", flush=True)
    result = subprocess.run(cmd)
    return result.returncode


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    """
    Parse arguments, detect changed files, select tests, and execute Pytest.

    Environment variable fallbacks
    ------------------------------
    BASE_SHA : str  – used when ``--base`` is not supplied.
    HEAD_SHA : str  – used when ``--head`` is not supplied.

    Parameters
    ----------
    argv : list[str] | None
        Argument vector (defaults to ``sys.argv[1:]``).

    Returns
    -------
    int
        Exit code to propagate to the shell.
    """
    parser = argparse.ArgumentParser(
        description="Dynamic Test-Subset Router — selectively runs Pytest based on Git changes."
    )
    parser.add_argument("--base", default=None, help="Base Git reference (commit SHA or branch).")
    parser.add_argument("--head", default=None, help="Head Git reference (commit SHA or branch).")
    args = parser.parse_args(argv)

    # Resolve references: CLI args take priority, then env vars
    base = args.base or os.environ.get("BASE_SHA", "")
    head = args.head or os.environ.get("HEAD_SHA", "")

    print("=" * 60)
    print(" Dynamic Test-Subset Router")
    print(f" Student : Katakam Surya Teja  |  USN: 24BTRAO017")
    print("=" * 60)

    if base and head:
        print(f"[router] Comparing  base={base!r}  →  head={head!r}")
        changed = git_changed_files(base, head)
        if changed:
            print(f"[router] Changed files ({len(changed)}):")
            for f in changed:
                print(f"         • {f}")
        else:
            print("[router] No differences found between the two references.")
    else:
        print("[router] ⚠  --base / --head not provided — running full test suite (fallback).")
        changed = []

    selected = select_tests(changed)

    print(f"\n[router] Selected test path(s):")
    for p in selected:
        print(f"         → {p}")
    print()

    return run_tests(selected)


if __name__ == "__main__":
    sys.exit(main())
