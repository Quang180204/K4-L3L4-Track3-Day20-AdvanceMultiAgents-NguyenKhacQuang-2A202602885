---
name: enforce-type-hints-and-documentation
description: Use this skill when writing or fixing Python packages and modules to ensure all public functions have complete type annotations and all requirements are met.
---
- Add type annotations to every parameter and the return value of all public functions (names not starting with `_`).
- Create regression test files (e.g., `tests/test_regressions.py`) containing at least one test function per fixed bug.
- Document all fixes in `CHANGELOG.md` under the `## Unreleased` heading using the format `- fix(<function name>): <short description>` with at least one bullet per fix.
- Never modify existing test files in `tests/`; only add new test files if needed.