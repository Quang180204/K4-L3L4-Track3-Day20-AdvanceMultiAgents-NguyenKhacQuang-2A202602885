"""GUIDE Phần 3 - Người tuyển chọn skill (skill curator): tự viết skill từ các lần chạy thất bại.   >>> SINH VIÊN CÀI ĐẶT curate_skills <<<

Pseudo-code: guides/pseudocode/04_curator.md
Kiểm tra:    pytest tests/test_04_curator.py
Chạy thật:   python -m lab.curator
"""
import re
from pathlib import Path

from .tasks import eval_markers   # có sẵn: định danh của tác vụ đánh giá, tính lúc chạy

# ---- CÓ SẴN, KHÔNG SỬA: kiểm tra và tách khối skill (phần dễ sai và liên quan bảo mật) ----------------
SAFE_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def validate_skill(text: str, expected_name: str | None = None) -> list[str]:
    """Kiểm tra nội dung một SKILL.md. Trả về danh sách vấn đề (rỗng = hợp lệ).

    Quy tắc: có khối YAML frontmatter; `name` chữ thường/số/gạch ngang (tối đa 64 ký tự) và bằng `expected_name`
    nếu được truyền; có `description` (tối đa 1024 ký tự); phần thân tối đa 80 dòng; không chứa chuỗi nào của
    `eval_markers()`. Quy tắc về `name` cũng là biện pháp bảo mật: tên khối do LLM sinh ra được dùng để tạo
    đường dẫn, nên `../evil` không được lọt qua.
    """
    problems = []
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text.strip() + "\n", re.S)
    if not m:
        return ["missing YAML frontmatter"]
    front, body = m.groups()
    name = re.search(r"^name:\s*(.+)$", front, re.M)
    desc = re.search(r"^description:\s*(.+)$", front, re.M)
    n = name.group(1).strip() if name else ""
    if not SAFE_NAME.fullmatch(n) or len(n) > 64:
        problems.append("invalid name")
    elif expected_name is not None and n != expected_name:
        problems.append("name differs from the block name")
    if not desc or len(desc.group(1).strip()) > 1024:
        problems.append("missing or too long description")
    if len(body.strip().splitlines()) > 80:
        problems.append("body longer than 80 lines")
    low = text.lower()
    for marker in eval_markers():
        if marker in low:
            problems.append(f"mentions evaluation material: {marker}")
    return problems


def parse_skill_blocks(reply: str) -> list[tuple[str, str]]:
    """Tách câu trả lời của LLM thành danh sách (name, nội dung SKILL.md).

    Khuôn dạng: `=== SKILL: <name> ===` ... `=== END ===`. Một khối kết thúc ở điểm nào đến trước trong ba điểm:
    `=== END ===`, tiêu đề `=== SKILL:` kế tiếp, hoặc cuối văn bản (LLM đôi khi quên dòng END).
    """
    pattern = re.compile(r"^=== SKILL: (\S+) ===[ \t]*\n(.*?)(?=^=== END ===|^=== SKILL: |\Z)", re.S | re.M)
    return [(name, text.strip()) for name, text in pattern.findall(str(reply))]
# --------------------------------------------------------------------------------------------------


import json
from .model import make_model
from .tasks import ROOT, eval_markers


def curate_skills(results_dir="results", source_condition="baseline", out_dir=None, model=None, max_skills: int = 3) -> list[Path]:
    """Đọc các lần chạy của TÁC VỤ HỌC (role == "learn") trong `source_condition`, nhờ LLM viết skill, ghi file.

    Các bước: nạp run.json + trace.md -> (nếu không có check nào thất bại: in cảnh báo và trả về [] mà KHÔNG gọi LLM)
    -> dựng prompt -> model.invoke(prompt) -> parse_skill_blocks -> validate_skill(text, expected_name=name)
    -> ghi `<out_dir>/<name>/SKILL.md`. Mặc định `out_dir` = <gốc lab>/skills/auto (dùng `ROOT` từ lab.tasks).
    Giữ tối đa `max_skills` skill hợp lệ; skill không hợp lệ bị bỏ qua.
    Prompt chứa, với mỗi check thất bại, TÊN và trường `detail` (lời nhận xét của bot đánh giá: phát biểu quy tắc bị vi phạm)
    cùng phần cuối của vết (trace). Với tác vụ học, `detail` chỉ phát biểu quy tắc, không chứa đáp án.
    Tuyệt đối KHÔNG đưa dữ liệu của tác vụ đánh giá (role == "eval") vào prompt.
    model mặc định: make_model() (lab.model).
    Trả về: danh sách đường dẫn SKILL.md đã ghi.
    """
    results_dir = Path(results_dir)
    if out_dir is None:
        out_dir = ROOT / "skills" / "auto"
    else:
        out_dir = Path(out_dir)

    runs = []
    condition_dir = results_dir / source_condition
    if condition_dir.exists():
        for run_path in sorted(condition_dir.glob("*/run.json")):
            try:
                r = json.loads(run_path.read_text(encoding="utf-8"))
            except Exception:
                continue
            if r.get("role") != "learn":
                continue
            failed = []
            for check in r.get("checks", []):
                if not check.get("passed", False):
                    failed.append((check.get("name", ""), check.get("detail", "")))
            trace_path = run_path.parent / "trace.md"
            trace = ""
            if trace_path.exists():
                try:
                    trace = trace_path.read_text(encoding="utf-8")
                    trace = trace[-6000:]
                except Exception:
                    pass
            if failed:
                runs.append({
                    "task": r.get("task", run_path.parent.name),
                    "failed": failed,
                    "trace": trace,
                })

    if not runs or not any(run["failed"] for run in runs):
        print("WARNING: không có check thất bại ở tác vụ học")
        return []

    if model is None:
        model = make_model()

    prompt_lines = [
        "You write SKILLS for a programming and data analysis agent.",
        "Below are the failed checks (check names and evaluation bot feedback/rules) and traces from recent runs.",
        f"Find common procedural failure patterns and write up to {max_skills} concise skills to prevent them on new tasks of the same type.",
        "",
        "Rules:",
        "- Skills must be general: do not mention task IDs, specific private file names, specific answers, or specific numbers.",
        "- Each skill must have YAML frontmatter with `name` (lowercase, numbers, hyphens only, max 64 chars) and `description` (one sentence: when to use this skill, max 1024 chars).",
        "- The body must be at most 40 lines of imperative guidance/checklist.",
        "- Do NOT mention any evaluation markers.",
        "- Exact block format:",
        "=== SKILL: <name> ===",
        "---",
        "name: <name>",
        "description: <when to use>",
        "---",
        "<content>",
        "=== END ===",
        "",
    ]
    for run in runs:
        prompt_lines.append(f"--- TASK: {run['task']} ---")
        prompt_lines.append("Failed checks:")
        for name, detail in run["failed"]:
            prompt_lines.append(f"- {name}: {detail}")
        if run["trace"]:
            prompt_lines.append(f"Recent trace excerpt:\n{run['trace']}\n")

    prompt = "\n".join(prompt_lines)
    reply = model.invoke(prompt)
    raw_content = getattr(reply, "content", reply)
    if isinstance(raw_content, list):
        parts = []
        for p in raw_content:
            if isinstance(p, dict) and "text" in p:
                parts.append(p["text"])
            elif isinstance(p, str):
                parts.append(p)
            else:
                parts.append(str(p))
        content = "\n".join(parts)
    else:
        content = str(raw_content)

    written: list[Path] = []
    blocks = parse_skill_blocks(content)
    for name, text in blocks:
        if len(written) >= max_skills:
            break
        problems = validate_skill(text, expected_name=name)
        if problems:
            continue
        skill_file = out_dir / name / "SKILL.md"
        skill_file.parent.mkdir(parents=True, exist_ok=True)
        skill_file.write_text(text, encoding="utf-8")
        written.append(skill_file)

    return written


if __name__ == "__main__":
    for p in curate_skills():
        print("wrote", p)
