### Human
The test suite of the `bookings` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Tool call: ls
{"path": "workspace"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/', '/workspace/tests/']

### Tool call: glob
{"path": "workspace", "pattern": "**/*"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/__init__.py', '/workspace/bookings/__pycache__/__init__.cpython-314.pyc', '/workspace/bookings/__pycache__/billing.cpython-314.pyc', '/workspace/bookings/__pycache__/calendar_export.cpython-314.pyc', '/workspace/bookings/__pycache__/schedule.cpython-314.pyc', '/workspace/bookings/__pycache__/timeutil.cpython-314.pyc', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py', '/workspace/tests/__pycache__/test_bookings.cpython-314-pytest-9.1.1.pyc', '/workspace/tests/test_bookings.py']

### Tool call: execute
{"command": "pytest workspace/tests"}

### Tool result
============================= test session starts ==============================
platform linux -- Python 3.14.4, pytest-9.1.1, pluggy-1.6.0
rootdir: /tmp/lab_sandbox_0_h9guby
plugins: anyio-4.15.1, langsmith-0.14.4
collected 0 items / 1 error

==================================== ERRORS ====================================
______________ ERROR collecting workspace/tests/test_bookings.py _______________
ImportError while importing test module '/tmp/lab_sandbox_0_h9guby/workspace/tests/test_bookings.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/mnt/c/Users/PC/K4-L3L4-Track3-Day20-AdvanceMultiAgents-NguyenKhacQuang-2A202602885/tasks/code-eval/workspace/tests/test_bookings.py:1: in <module>
    from bookings.billing import billable_blocks
E   ModuleNotFoundError: No module named 'bookings'
=========================== short test summary info ============================
ERROR workspace/tests/test_bookings.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
=============================== 1 error in 3.90s ===============================

Exit code: 2
[Command failed with exit code 2]

### Tool call: execute
{"command": "PYTHONPATH=workspace pytest workspace/tests"}

### Tool result
============================= test session starts ==============================
platform linux -- Python 3.14.4, pytest-9.1.1, pluggy-1.6.0
rootdir: /tmp/lab_sandbox_0_h9guby
plugins: anyio-4.15.1, langsmith-0.14.4
collected 3 items

workspace/tests/test_bookings.py FF.                                     [100%]

=================================== FAILURES ===================================
_______________________ test_total_minutes_mixed_formats _______________________

    def test_total_minutes_mixed_formats():
>       assert total_minutes(["1h30m", "2h"]) == 210
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

/mnt/c/Users/PC/K4-L3L4-Track3-Day20-AdvanceMultiAgents-NguyenKhacQuang-2A202602885/tasks/code-eval/workspace/tests/test_bookings.py:6: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
workspace/bookings/schedule.py:7: in total_minutes
    return sum(parse_duration(d) for d in durations)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
workspace/bookings/schedule.py:7: in <genexpr>
    return sum(parse_duration(d) for d in durations)
               ^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

text = '2h'

    def parse_duration(text):
        """Convert a duration string to whole minutes (int).
    
        Supported formats:
          "1h30m" -> 90
          "2h"    -> 120
          "45m"   -> 45
          "1:30"  -> 90
          "45"    -> 45    # a bare number means minut

### Tool call: read_file
{"file_path": "workspace/tests/test_bookings.py"}

### Tool result
@@ lines 1-15 of 15 @@
from bookings.billing import billable_blocks
from bookings.schedule import add_slot, total_minutes


def test_total_minutes_mixed_formats():
    assert total_minutes(["1h30m", "2h"]) == 210


def test_billable_blocks_rounds_up():
    assert billable_blocks(20) == 2
    assert billable_blocks(45) == 3


def test_add_slot_single_call():
    assert add_slot("a") == ["a"]

### Tool call: read_file
{"file_path": "workspace/bookings/billing.py"}

### Tool result
@@ lines 1-11 of 11 @@
"""Billing rules."""


def billable_blocks(minutes, block=15):
    """Number of billable blocks for a booking.

    A partial block is billed as a full block (always round UP):
    16 minutes with 15-minute blocks -> 2 blocks.
    `minutes` must be >= 0; a negative value raises ValueError.
    """
    return round(minutes / block)

### Tool call: read_file
{"file_path": "workspace/bookings/calendar_export.py"}

### Tool result
@@ lines 1-7 of 7 @@
"""Calendar export."""
from .timeutil import parse_duration


def slot_end(start_minute, duration_text):
    """Minute of the day at which a slot ends."""
    return start_minute + parse_duration(duration_text)

### Tool call: read_file
{"file_path": "workspace/bookings/schedule.py"}

### Tool result
@@ lines 1-17 of 17 @@
"""Schedule helpers."""
from .timeutil import parse_duration


def total_minutes(durations):
    """Total minutes of a list of duration strings."""
    return sum(parse_duration(d) for d in durations)


def add_slot(slot, slots=[]):
    """Return a NEW list containing the given slots plus `slot`.

    Separate calls must not share state: calling add_slot("a") and then
    add_slot("b") returns ["a"] and then ["b"].
    """
    slots.append(slot)
    return slots

### Tool call: read_file
{"file_path": "workspace/bookings/timeutil.py"}

### Tool result
@@ lines 1-19 of 19 @@
"""Time helpers for the bookings package."""
import re


def parse_duration(text):
    """Convert a duration string to whole minutes (int).

    Supported formats:
      "1h30m" -> 90
      "2h"    -> 120
      "45m"   -> 45
      "1:30"  -> 90
      "45"    -> 45    # a bare number means minutes
    Surrounding whitespace is ignored.
    """
    m = re.fullmatch(r"(\d+)h(\d+)m", text.strip())
    if not m:
        raise ValueError(f"bad duration: {text!r}")
    return int(m.group(1)) * 60 + int(m.group(2))

### Tool call: glob
{"path": "workspace", "pattern": "**/*.py"}

### Tool result
['/workspace/bookings/__init__.py', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py', '/workspace/tests/test_bookings.py']

### Tool call: read_file
{"file_path": "workspace/bookings/__init__.py"}

### Tool result
@@ lines 1-1 of 1 @@
__version__ = "1.4.2"

### Tool call: edit_file
{"file_path": "workspace/bookings/timeutil.py", "new_string": "def parse_duration(text):\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    text = text.strip()\n    if text.isdigit():\n        return int(text)\n    \n    # Check for \"H:MM\" format\n    m_hm = re.fullmatch(r\"(\\d+):(\\d+)\", text)\n    if m_hm:\n        return int(m_hm.group(1)) * 60 + int(m_hm.group(2))\n\n    # Check for \"XhYm\" or \"Xh\" or \"Ym\"\n    m_h_m = re.fullmatch(r\"(?:(\\d+)h)?(?:(\\d+)m)?\", text)\n    if m_h_m and (m_h_m.group(1) is not None or m_h_m.group(2) is not None):\n        h = int(m_h_m.group(1)) if m_h_m.group(1) is not None else 0\n        m = int(m_h_m.group(2)) if m_h_m.group(2) is not None else 0\n        # Ensure it matched the entire text (no trailing invalid chars)\n        # Actually fullmatch ensures it matched the entire text, but let's check if group(0) == text\n        if m_h_m.group(0) == text:\n            return h * 60 + m\n\n    raise ValueError(f\"bad duration: {text!r}\")", "old_string": "def parse_duration(text):\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare n

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/timeutil.py'

### Tool call: edit_file
{"file_path": "workspace/bookings/billing.py", "old_string": "def billable_blocks(minutes, block=15):\n    \"\"\"Number of billable blocks for a booking.\n\n    A partial block is billed as a full block (always round UP):\n    16 minutes with 15-minute blocks -> 2 blocks.\n    `minutes` must be >= 0; a negative value raises ValueError.\n    \"\"\"\n    return round(minutes / block)", "new_string": "def billable_blocks(minutes, block=15):\n    \"\"\"Number of billable blocks for a booking.\n\n    A partial block is billed as a full block (always round UP):\n    16 minutes with 15-minute blocks -> 2 blocks.\n    `minutes` must be >= 0; a negative value raises ValueError.\n    \"\"\"\n    if minutes < 0:\n        raise ValueError(\"minutes must be >= 0\")\n    import math\n    return math.ceil(minutes / block)"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/billing.py'

### Tool call: edit_file
{"new_string": "def add_slot(slot, slots=None):\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    if slots is None:\n        slots = []\n    else:\n        slots = list(slots)\n    slots.append(slot)\n    return slots", "file_path": "workspace/bookings/schedule.py", "old_string": "def add_slot(slot, slots=[]):\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    slots.append(slot)\n    return slots"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/schedule.py'

### Tool call: execute
{"command": "PYTHONPATH=workspace pytest workspace/tests"}

### Tool result
============================= test session starts ==============================
platform linux -- Python 3.14.4, pytest-9.1.1, pluggy-1.6.0
rootdir: /tmp/lab_sandbox_0_h9guby
plugins: anyio-4.15.1, langsmith-0.14.4
collected 3 items

workspace/tests/test_bookings.py ...                                     [100%]

============================== 3 passed in 0.02s ===============================

[Command succeeded with exit code 0]

### Tool call: write_file
{"content": "from bookings.billing import billable_blocks\nfrom bookings.calendar_export import slot_end\nfrom bookings.schedule import add_slot, total_minutes\nfrom bookings.timeutil import parse_duration\nimport pytest\n\n\ndef test_parse_duration_all_formats():\n    assert parse_duration(\"1h30m\") == 90\n    assert parse_duration(\"2h\") == 120\n    assert parse_duration(\"45m\") == 45\n    assert parse_duration(\"1:30\") == 90\n    assert parse_duration(\"45\") == 45\n    assert parse_duration(\"  2h 30m  \") == 150 # wait, does spaces inside work? Surrounding whitespace is ignored.\n    assert parse_duration(\" 2h \") == 120\n\n\ndef test_parse_duration_invalid():\n    with pytest.raises(ValueError):\n        parse_duration(\"abc\")\n\n\ndef test_billable_blocks_negative():\n    with pytest.raises(ValueError):\n        billable_blocks(-1)\n    assert billable_blocks(0) == 0\n    assert billable_blocks(15) == 1\n    assert billable_blocks(16) == 2\n\n\ndef test_add_slot_state():\n    res1 = add_slot(\"a\")\n    res2 = add_slot(\"b\")\n    assert res1 == [\"a\"]\n    assert res2 == [\"b\"]\n    res3 = add_slot(\"c\", [\"x\"])\n    assert res3 == [\"x\", \"c\"]\n\n\ndef test_slot_end():\n    assert slot_end(480, \"1h30m\") == 570\n", "file_path": "workspace/tests/extra_test_bookings.py"}

### Tool result
Updated file /workspace/tests/extra_test_bookings.py

### Tool call: execute
{"command": "PYTHONPATH=workspace pytest workspace/tests"}

### Tool result
============================= test session starts ==============================
platform linux -- Python 3.14.4, pytest-9.1.1, pluggy-1.6.0
rootdir: /tmp/lab_sandbox_0_h9guby
plugins: anyio-4.15.1, langsmith-0.14.4
collected 3 items

workspace/tests/test_bookings.py ...                                     [100%]

============================== 3 passed in 0.11s ===============================

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "PYTHONPATH=workspace pytest workspace/tests/extra_test_bookings.py"}

### Tool result
============================= test session starts ==============================
platform linux -- Python 3.14.4, pytest-9.1.1, pluggy-1.6.0
rootdir: /tmp/lab_sandbox_0_h9guby
plugins: anyio-4.15.1, langsmith-0.14.4
collected 5 items

workspace/tests/extra_test_bookings.py F....                             [100%]

=================================== FAILURES ===================================
_______________________ test_parse_duration_all_formats ________________________

    def test_parse_duration_all_formats():
        assert parse_duration("1h30m") == 90
        assert parse_duration("2h") == 120
        assert parse_duration("45m") == 45
        assert parse_duration("1:30") == 90
        assert parse_duration("45") == 45
>       assert parse_duration("  2h 30m  ") == 150 # wait, does spaces inside work? Surrounding whitespace is ignored.
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^

workspace/tests/extra_test_bookings.py:14: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

text = '2h 30m'

    def parse_duration(text):
        """Convert a duration string to whole minutes (int).
    
        Supported formats:
          "1h30m" -> 90
          "2h"    -> 120
          "45m"   -> 45
          "1:30"  -> 90
          "45"    -> 45    # a bare number means minutes
        Surrounding whitespace is ignored.
        """
        text = text.strip()
        if text.isdigit():
            return int(text)
    
        # Check for "H:MM" format

### Tool call: delete
{"file_path": "workspace/tests/extra_test_bookings.py"}

### Tool result
Deleted /workspace/tests/extra_test_bookings.py

### Tool call: edit_file
{"new_string": "def parse_duration(text):\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    text = text.strip()\n    if text.isdigit():\n        return int(text)\n\n    # Check for \"H:MM\" format\n    m_hm = re.fullmatch(r\"(\\d+):(\\d+)\", text)\n    if m_hm:\n        return int(m_hm.group(1)) * 60 + int(m_hm.group(2))\n\n    # Check for \"XhYm\", \"Xh\", \"Ym\"\n    m_h = re.fullmatch(r\"(\\d+)h\", text)\n    if m_h:\n        return int(m_h.group(1)) * 60\n\n    m_m = re.fullmatch(r\"(\\d+)m\", text)\n    if m_m:\n        return int(m_m.group(1))\n\n    m_hm2 = re.fullmatch(r\"(\\d+)h(\\d+)m\", text)\n    if m_hm2:\n        return int(m_hm2.group(1)) * 60 + int(m_hm2.group(2))\n\n    raise ValueError(f\"bad duration: {text!r}\")", "old_string": "def parse_duration(text):\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    text = text.strip()\n    if text.isdigit():\n        return int(text)\n    \n    # Check for \"H:MM\" format\n    m_hm = re.fullmatch(r\"(\\d+):(\\d+)\", text)\n    if m_hm:\n    

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/timeutil.py'

### Tool call: execute
{"command": "PYTHONPATH=workspace pytest workspace/tests"}

### Tool result
============================= test session starts ==============================
platform linux -- Python 3.14.4, pytest-9.1.1, pluggy-1.6.0
rootdir: /tmp/lab_sandbox_0_h9guby
plugins: anyio-4.15.1, langsmith-0.14.4
collected 3 items

workspace/tests/test_bookings.py ...                                     [100%]

============================== 3 passed in 0.02s ===============================

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "git status"}

### Tool result
[stderr] fatal: not a git repository (or any parent up to mount point /)
[stderr] Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).

Exit code: 128
[Command failed with exit code 128]

### Tool call: execute
{"command": "PYTHONPATH=workspace pytest workspace/tests"}

### Tool result
============================= test session starts ==============================
platform linux -- Python 3.14.4, pytest-9.1.1, pluggy-1.6.0
rootdir: /tmp/lab_sandbox_0_h9guby
plugins: anyio-4.15.1, langsmith-0.14.4
collected 3 items

workspace/tests/test_bookings.py ...                                     [100%]

============================== 3 passed in 0.02s ===============================

[Command succeeded with exit code 0]

### Assistant
[{'type': 'text', 'text': 'I have successfully fixed the issues in the `bookings` package so that the test suite passes and all functions correctly implement their specifications and docstrings:\n\n- **`bookings/timeutil.py`**: Updated `parse_duration` to correctly parse all supported duration formats (`"1h30m"`, `"2h"`, `"45m"`, `"1:30"`, and bare numbers like `"45"`).\n- **`bookings/billing.py`**: Updated `billable_blocks` to correctly round up partial blocks using `math.ceil` and raise a `ValueError` for negative input minutes.\n- **`bookings/schedule.py`**: Fixed the default mutable argument bug in `add_slot` so that separate calls do not share state.\n\n### Summary of Changed Files:\n- `workspace/bookings/timeutil.py`\n- `workspace/bookings/billing.py`\n- `workspace/bookings/schedule.py`', 'extras': {'signature': 'EmAKXgFpFH0TdHCnnD6CdwDY1D4mvAyMgqo6YNsLZu+EZJyhaRVDLXmvTkD9MMJvpoyXhC800lxgzpKD8+sl4SBum3zlReCAfUDIKtXVeHBd6TouSbtboGENXerrrbp64Ls='}}]