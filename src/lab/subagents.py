"""GUIDE Phần 1 - Định nghĩa subagent (tác tử con).   >>> SINH VIÊN CÀI ĐẶT <<<

Pseudo-code: guides/pseudocode/02_subagents.md
Kiểm tra:    pytest tests/test_02_agent.py
"""


def get_subagents() -> list[dict]:
    """Trả về danh sách subagent (ít nhất 2, tên khác nhau).

    Mỗi phần tử là một dict có các khóa bắt buộc:
      "name":          tên duy nhất (chữ thường, có thể có dấu gạch ngang)
      "description":   khi nào tác tử chính nên giao việc cho subagent này (viết như một hướng dẫn hành động)
      "system_prompt": chỉ dẫn cho subagent
    Gợi ý vai trò: explorer (đọc và báo cáo), implementer (thực hiện), reviewer (kiểm tra độc lập).
    """
    return [
        {
            "name": "explorer",
            "description": "Use to inspect the workspace, read files, analyze raw logs or data, and report factual findings without modifying any files.",
            "system_prompt": (
                "You are an exploration assistant. Your job is to inspect files, search contents, and gather facts. "
                "Do not create, edit, or delete any files. Report your findings clearly, objectively, and concisely."
            ),
        },
        {
            "name": "implementer",
            "description": "Use to perform multi-step modifications, write or edit code/data files, and run tests or verification commands.",
            "system_prompt": (
                "You are an implementation assistant. Your job is to make changes, write/edit files, and run commands or tests. "
                "Always verify your changes and report which files were modified and the outcome of tests."
            ),
        },
        {
            "name": "reviewer",
            "description": "Use to independently review deliverables, check edge cases, and run tests against requirements without modifying files.",
            "system_prompt": (
                "You are a review and verification assistant. Your job is to independently verify that solutions meet requirements, "
                "check file contents and formatting, and test edge cases. Do not modify files. Report any discrepancies found."
            ),
        },
    ]

