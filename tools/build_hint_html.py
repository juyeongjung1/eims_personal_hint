from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "EIMS個人演習のヒント(総合版).md"
OUTPUT = ROOT / "EIMS個人演習のヒント(総合版).html"

# 配布前にここへ日時を入れると、その日時以降に各演習のヒントが表示されます。
# ローカルHTML配布用の簡易制御です。厳密なアクセス制御ではありません。
RELEASE_SCHEDULE = {
    "ex1-1": {"label": "6/9 10:20", "datetime": "2026-06-09T10:20:00+09:00"},
    "ex1-2": {"label": "6/9 11:00", "datetime": "2026-06-09T11:00:00+09:00"},
    "ex2-1": {"label": "6/9 11:30", "datetime": "2026-06-09T11:30:00+09:00"},
    "ex2-2": {"label": "6/9 12:00", "datetime": "2026-06-09T12:00:00+09:00"},
    "ex2-3": {"label": "6/9 13:40", "datetime": "2026-06-09T13:40:00+09:00"},
    "ex3-1": {"label": "6/9 14:20", "datetime": "2026-06-09T14:20:00+09:00"},
    "ex3-2": {"label": "6/9 14:40", "datetime": "2026-06-09T14:40:00+09:00"},
    "ex3-3": {"label": "6/9 15:40", "datetime": "2026-06-09T15:40:00+09:00"},
    "ex4-1": {"label": "6/10 10:40", "datetime": "2026-06-10T10:40:00+09:00"},
    "ex4-2": {"label": "6/10 10:40", "datetime": "2026-06-10T10:40:00+09:00"},
    "ex4-3": {"label": "6/10 10:40", "datetime": "2026-06-10T10:40:00+09:00"},
    "ex5-1": {"label": "6/10 11:30", "datetime": "2026-06-10T11:30:00+09:00"},
    "ex5-2": {"label": "6/10 11:50", "datetime": "2026-06-10T11:50:00+09:00"},
    "ex5-3": {"label": "6/10 14:10", "datetime": "2026-06-10T14:10:00+09:00"},
    "ex5-4": {"label": "6/10 15:30", "datetime": "2026-06-10T15:30:00+09:00"},
}

JAVA_KEYWORDS = {
    "package",
    "import",
    "public",
    "private",
    "protected",
    "class",
    "static",
    "void",
    "int",
    "long",
    "boolean",
    "if",
    "else",
    "for",
    "while",
    "return",
    "new",
    "try",
    "catch",
    "break",
    "true",
    "false",
    "null",
}
JAVA_CONTROL_WORDS = {"if", "for", "while", "switch", "catch"}
JAVA_TOKEN_PATTERN = re.compile(r'"(?:\\.|[^"\\])*"|//.*|\b\d+\b|\b[A-Za-z_][A-Za-z0-9_]*\b|\s+|.')


def slugify(text: str, index: int) -> str:
    token = re.sub(r"[^\w一-龯ぁ-んァ-ヶー.]+", "-", text, flags=re.UNICODE).strip("-")
    return token or f"section-{index}"


def exercise_group(title: str) -> str:
    match = re.search(r"演習(\d+)", title)
    return f"ex{match.group(1)}" if match else "other"


def exercise_key(title: str) -> str:
    match = re.search(r"演習(\d+)\.(\d+)", title)
    return f"ex{match.group(1)}-{match.group(2)}" if match else exercise_group(title)


def inline(text: str) -> str:
    escaped = html.escape(text)

    def code_repl(match: re.Match[str]) -> str:
        return f"<code>{match.group(1)}</code>"

    escaped = re.sub(r"`([^`]+)`", code_repl, escaped)
    return escaped


def long_division_html(code: str) -> str:
    values = {}
    for line in code.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()

    dividend = html.escape(values.get("dividend", "12345"))
    divisor = html.escape(values.get("divisor", "1000"))
    quotient = html.escape(values.get("quotient", "12"))
    product = html.escape(values.get("product", "12000"))
    remainder = html.escape(values.get("remainder", "345"))
    formula = inline(values.get("formula", "12345 % 1000 は 345"))
    note = inline(values.get("note", "% は、割り算をしたときの余りだけを取り出します。"))

    return (
        '<div class="division-card">'
        '<div class="division-figure" role="img" '
        f'aria-label="{dividend} 割る {divisor} は {quotient} あまり {remainder}">'
        f'<div class="division-quotient">{quotient}</div>'
        '<div class="division-row">'
        f'<span class="division-divisor">{divisor}</span>'
        f'<span class="division-bracket"><span>{dividend}</span></span>'
        '</div>'
        f'<div class="division-product">{product}</div>'
        '<div class="division-line"></div>'
        f'<div class="division-remainder">{remainder}</div>'
        '</div>'
        '<div class="division-explain">'
        f'<p class="division-formula">{formula}</p>'
        f'<p>{note}</p>'
        '<p>つまり、商の <code>12</code> は「何秒分あるか」、余りの <code>345</code> は「ミリ秒部分」です。</p>'
        '</div>'
        '</div>'
    )


def span(class_name: str, text: str) -> str:
    return f'<span class="{class_name}">{html.escape(text)}</span>'


def string_span(text: str) -> str:
    escaped = html.escape(text).replace("____", '<span class="blank">____</span>')
    return f'<span class="tok-string">{escaped}</span>'


def next_code_token(tokens: list[str], index: int) -> str:
    for token in tokens[index + 1 :]:
        if not token.isspace():
            return token
    return ""


def highlight_java_line(line: str) -> str:
    tokens = JAVA_TOKEN_PATTERN.findall(line)
    highlighted = []

    for index, token in enumerate(tokens):
        if token == "____":
            highlighted.append('<span class="blank">____</span>')
        elif token.startswith("//"):
            highlighted.append(span("tok-comment", token))
        elif token.startswith('"'):
            highlighted.append(string_span(token))
        elif token.isdigit():
            highlighted.append(span("tok-number", token))
        elif re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", token):
            next_token = next_code_token(tokens, index)
            if token in JAVA_KEYWORDS:
                highlighted.append(span("tok-keyword", token))
            elif next_token == "(" and token not in JAVA_CONTROL_WORDS:
                highlighted.append(span("tok-method", token))
            elif token[0].isupper():
                highlighted.append(span("tok-class", token))
            else:
                highlighted.append(span("tok-variable", token))
        else:
            highlighted.append(html.escape(token))

    return "".join(highlighted)


def code_html(code: str, lang: str) -> str:
    if lang == "longdivision":
        return long_division_html(code)

    escaped_lines = []
    is_java = lang.lower() == "java"
    for raw_line in code.rstrip("\n").splitlines():
        if is_java:
            line = highlight_java_line(raw_line)
        else:
            line = html.escape(raw_line).replace("____", '<span class="blank">____</span>')
        stripped = line.strip()
        if raw_line.strip().startswith("// ★") or raw_line.strip().startswith("// ヒント"):
            line = f'<span class="code-comment">{line}</span>'
        escaped_lines.append(line)
    escaped = "\n".join(escaped_lines)
    label = html.escape(lang or "code")
    return (
        f'<div class="code-shell" data-lang="{label}">'
        f'<div class="code-toolbar"><span>{label}</span><button type="button">コピー</button></div>'
        f'<pre><code>{escaped}</code></pre>'
        f"</div>"
    )


def render_table(lines: list[str]) -> str:
    rows = []
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)
    headers = rows[0]
    body = rows[2:]
    out = ["<div class=\"table-wrap\"><table><thead><tr>"]
    out.extend(f"<th>{inline(cell)}</th>" for cell in headers)
    out.append("</tr></thead><tbody>")
    for row in body:
        out.append("<tr>")
        out.extend(f"<td>{inline(cell)}</td>" for cell in row)
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def render_blocks(markdown: str) -> tuple[str, list[tuple[str, str, str]]]:
    lines = markdown.splitlines()
    parts: list[str] = []
    toc: list[tuple[str, str, str]] = []
    section_open = False
    paragraph: list[str] = []
    list_lines: list[str] = []
    ordered_lines: list[str] = []
    i = 0
    section_index = 0

    def flush_paragraph() -> None:
        nonlocal paragraph
        if not paragraph:
            return
        text = " ".join(p.strip() for p in paragraph)
        paragraph = []
        if text.startswith("※"):
            parts.append(f'<aside class="reference">{inline(text)}</aside>')
        elif text.startswith("ポイントは") or text.startswith("ポイント:") or text.startswith("ポイント："):
            parts.append(f'<aside class="point-box"><strong>ポイント</strong><p>{inline(text)}</p></aside>')
        elif text.startswith("注意") or "注意してください" in text:
            parts.append(f'<aside class="caution-box"><strong>注意</strong><p>{inline(text)}</p></aside>')
        elif text.endswith(":") or text.endswith("："):
            parts.append(f'<p class="lead-label">{inline(text)}</p>')
        else:
            parts.append(f"<p>{inline(text)}</p>")

    def flush_list() -> None:
        nonlocal list_lines, ordered_lines
        if list_lines:
            parts.append("<ul>" + "".join(f"<li>{inline(item)}</li>" for item in list_lines) + "</ul>")
            list_lines = []
        if ordered_lines:
            parts.append("<ol>" + "".join(f"<li>{inline(item)}</li>" for item in ordered_lines) + "</ol>")
            ordered_lines = []

    while i < len(lines):
        line = lines[i]

        if line.startswith("```"):
            flush_paragraph()
            flush_list()
            lang = line.strip("`").strip()
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1
            parts.append(code_html("\n".join(code_lines), lang))
            i += 1
            continue

        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|?\s*:?-{3,}", lines[i + 1]):
            flush_paragraph()
            flush_list()
            table_lines = [line, lines[i + 1]]
            i += 2
            while i < len(lines) and lines[i].startswith("|"):
                table_lines.append(lines[i])
                i += 1
            parts.append(render_table(table_lines))
            continue

        if not line.strip():
            flush_paragraph()
            flush_list()
            i += 1
            continue

        if line.startswith("# "):
            flush_paragraph()
            flush_list()
            title = line[2:].strip()
            parts.append(
                f'<header class="doc-hero"><p class="kicker">EIMS 個人演習</p>'
                f"<h1>{inline(title)}</h1>"
        f"<p>ヒントを演習ごとに整理し、参照テキスト・コード・重要ポイントを読みやすくまとめています。</p></header>"
            )
            i += 1
            continue

        if line.startswith("## "):
            flush_paragraph()
            flush_list()
            if section_open:
                parts.append("</section>")
            section_index += 1
            title = line[3:].strip()
            sid = slugify(title, section_index)
            group = exercise_group(title)
            key = exercise_key(title)
            toc.append((sid, title, group))
            parts.append(f'<section class="exercise" id="{sid}" data-title="{html.escape(title)}" data-group="{group}" data-exercise="{key}"><h2>{inline(title)}</h2>')
            section_open = True
            i += 1
            continue

        if line.startswith("### "):
            flush_paragraph()
            flush_list()
            title = line[4:].strip()
            hclass = ""
            if "注意" in title:
                hclass = ' class="caution-heading"'
            elif "ポイント" in title or "仕様" in title:
                hclass = ' class="point-heading"'
            parts.append(f"<h3{hclass}>{inline(title)}</h3>")
            i += 1
            continue

        if line.startswith("- "):
            flush_paragraph()
            ordered_lines = []
            list_lines.append(line[2:].strip())
            i += 1
            continue

        number_match = re.match(r"^\d+\.\s+(.*)", line)
        if number_match:
            flush_paragraph()
            list_lines = []
            ordered_lines.append(number_match.group(1).strip())
            i += 1
            continue

        image_match = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line.strip())
        if image_match:
            flush_paragraph()
            flush_list()
            alt, src = image_match.groups()
            parts.append(
                f'<figure><img src="{html.escape(src)}" alt="{html.escape(alt)}" loading="lazy">'
                f"<figcaption>{inline(alt)}</figcaption></figure>"
            )
            i += 1
            continue

        paragraph.append(line)
        i += 1

    flush_paragraph()
    flush_list()
    if section_open:
        parts.append("</section>")
    return "\n".join(parts), toc


def build_html(body: str, toc: list[tuple[str, str, str]]) -> str:
    total_count = len(toc)
    release_schedule_json = json.dumps(RELEASE_SCHEDULE, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>EIMS個人演習のヒント（総合版）</title>
<style>
:root {{
  --bg: #f7f8f5;
  --paper: #ffffff;
  --ink: #1d2528;
  --muted: #5b676c;
  --line: #d9dfdc;
  --line-strong: #bdc9c4;
  --green: #1f7a62;
  --green-soft: #e6f3ee;
  --amber: #946200;
  --amber-soft: #fff3d6;
  --code-bg: #fbfcfa;
  --code-head: #eef4f1;
  --code-line: #ccd8d3;
  --blue: #2f5f9e;
  --red: #b43d2d;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: "Yu Gothic UI", "Meiryo", system-ui, sans-serif;
  line-height: 1.78;
}}
.progress {{ position: fixed; inset: 0 auto auto 0; height: 4px; width: 0; background: var(--green); z-index: 5; }}
.layout {{ min-height: 100vh; }}
.brand {{ font-weight: 700; font-size: 15px; color: var(--green); }}
.topbar {{
  position: sticky; top: 0; z-index: 3;
  background: rgba(247, 248, 245, 0.96); backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--line); margin: -12px 0 20px; padding: 12px 0 14px;
}}
.topbar-row {{
  display: grid; grid-template-columns: 180px minmax(220px, 1fr) auto auto; gap: 12px;
  align-items: center; margin-bottom: 10px;
}}
.schedule-banner {{
  margin: 14px 0 0; padding: 10px 12px; border: 1px solid #b7dce8;
  border-radius: 8px; background: #eef9fc; color: #21424c; font-size: 13px;
}}
.schedule-banner strong {{ color: #0f5f76; }}
.search {{
  width: 100%; height: 40px; border: 1px solid var(--line); border-radius: 6px;
  padding: 0 10px; background: white; font-size: 14px;
}}
.search-status {{
  color: var(--muted); font-size: 13px; white-space: nowrap; text-align: right;
}}
.instructor-button, .instructor-panel button {{
  border: 1px solid var(--line-strong); background: white; color: #203431;
  border-radius: 6px; padding: 8px 11px; cursor: pointer; font-weight: 700;
}}
.instructor-button:hover, .instructor-panel button:hover {{
  border-color: var(--green); color: var(--green); background: var(--green-soft);
}}
.instructor-panel {{
  display: none; position: fixed; top: 70px; right: 22px; z-index: 10;
  width: min(720px, calc(100vw - 32px)); max-height: calc(100vh - 92px);
  overflow: auto; padding: 16px; border: 1px solid var(--line-strong);
  border-radius: 8px; background: white; box-shadow: 0 16px 44px rgba(20, 30, 28, 0.2);
}}
.instructor-panel.open {{ display: block; }}
.instructor-panel h3 {{ margin: 0 0 10px; font-size: 16px; color: #243235; }}
.instructor-login {{
  display: grid; grid-template-columns: minmax(180px, 260px) auto; gap: 8px; align-items: center;
}}
.instructor-login input, .schedule-editor input {{
  height: 36px; border: 1px solid var(--line); border-radius: 6px; padding: 0 9px;
  font-family: inherit; font-size: 14px;
}}
.instructor-tools {{ display: none; }}
.instructor-panel.authed .instructor-login {{ display: none; }}
.instructor-panel.authed .instructor-tools {{ display: block; }}
.instructor-actions {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin: 10px 0; }}
.instructor-actions label {{ display: inline-flex; align-items: center; gap: 6px; font-weight: 700; }}
.instructor-status {{ color: var(--muted); font-size: 13px; }}
.schedule-editor {{
  display: grid; grid-template-columns: repeat(2, minmax(260px, 1fr)); gap: 8px 14px;
  margin-top: 10px;
}}
.schedule-row {{
  display: grid; grid-template-columns: 84px minmax(170px, 1fr); gap: 8px; align-items: center;
}}
.schedule-row span {{ font-weight: 700; color: #243235; }}
.tabs {{
  display: flex; flex-wrap: wrap; gap: 8px;
}}
.tabs button {{
  border: 1px solid var(--line-strong); background: white; color: #203431;
  border-radius: 999px; padding: 8px 13px; cursor: pointer; font-weight: 700; font-size: 14px;
}}
.tabs button:hover {{ border-color: var(--green); color: var(--green); background: var(--green-soft); }}
.tabs button.active {{ background: var(--green); border-color: var(--green); color: white; }}
main {{ max-width: 1040px; width: 100%; margin: 0 auto; padding: 40px 42px 80px; }}
.release-note {{
  display: inline-flex; align-items: center; gap: 6px; color: var(--amber);
  background: var(--amber-soft); border: 1px solid #e3bd66; border-radius: 999px;
  padding: 3px 9px; font-size: 12px; font-weight: 700; margin-left: 8px;
}}
.release-note.open {{
  color: var(--green); background: var(--green-soft); border-color: #b9d8cb;
}}
.locked-message {{
  margin: 14px 0 0; padding: 16px; border: 1px solid #e3bd66; border-radius: 8px;
  background: #fff8e7; color: #654700; font-weight: 700;
}}
.locked-message small {{
  display: block; margin-top: 4px; color: #7b6125; font-weight: 500;
}}
.doc-hero {{
  padding: 20px 0 30px; border-bottom: 2px solid var(--line); margin-bottom: 26px;
}}
.kicker {{ color: var(--green); font-weight: 700; margin: 0 0 8px; }}
h1 {{ font-size: 34px; line-height: 1.25; margin: 0 0 12px; }}
h2 {{
  font-size: 25px; line-height: 1.35; margin: 0 0 22px; padding-bottom: 10px;
  border-bottom: 1px solid var(--line);
}}
h3 {{ font-size: 18px; margin: 26px 0 8px; color: #243235; }}
p {{ margin: 10px 0; }}
.exercise {{
  background: var(--paper); border: 1px solid var(--line); border-radius: 8px;
  padding: 28px; margin: 22px 0; box-shadow: 0 1px 2px rgba(20, 30, 28, 0.04);
}}
.exercise.locked > :not(h2):not(.locked-message) {{ display: none; }}
.exercise.locked {{ border-color: #e3bd66; background: #fffdf7; }}
.reference {{
  border-left: 6px solid var(--green); background: var(--green-soft);
  padding: 13px 15px; margin: 16px 0; border-radius: 0 6px 6px 0; font-weight: 700;
  box-shadow: inset 0 0 0 1px rgba(31, 122, 98, 0.08);
}}
.point-box, .caution-box {{
  margin: 16px 0; padding: 14px 15px; border-radius: 8px; border: 1px solid;
}}
.point-box {{ background: #edf7f3; border-color: #b9d8cb; }}
.caution-box {{ background: #fff4df; border-color: #e3bd66; }}
.point-box strong {{ color: var(--green); }}
.caution-box strong {{ color: var(--amber); }}
.point-box p, .caution-box p {{ margin: 6px 0 0; }}
.lead-label {{
  font-weight: 700; color: var(--green); margin-top: 20px; padding: 8px 10px;
  background: #f1f7f4; border-left: 4px solid var(--green); border-radius: 0 5px 5px 0;
}}
.point-heading, .caution-heading {{ padding-left: 10px; border-left: 5px solid; }}
.point-heading {{ border-color: var(--green); }}
.caution-heading {{ border-color: #e3b341; color: #6f4e00; }}
ul, ol {{ padding-left: 1.4rem; }}
li {{ margin: 5px 0; }}
code {{ background: #eef2f1; padding: 0.1em 0.35em; border-radius: 4px; font-family: Consolas, "Courier New", monospace; }}
.code-shell {{
  background: var(--code-bg); color: #172126; border: 1px solid var(--code-line);
  border-radius: 8px; overflow: hidden; margin: 18px 0;
  box-shadow: 0 1px 2px rgba(20, 30, 28, 0.05);
}}
.code-shell code {{
  background: transparent; padding: 0; border-radius: 0;
}}
.code-toolbar {{
  display: flex; justify-content: space-between; align-items: center; padding: 8px 12px;
  background: var(--code-head); color: #2e4b45; font-size: 12px; border-bottom: 1px solid var(--code-line);
}}
.code-toolbar span {{
  font-weight: 700; letter-spacing: 0; text-transform: uppercase;
}}
.code-toolbar button {{
  border: 1px solid var(--line-strong); background: white; color: #1f3a36;
  border-radius: 5px; padding: 4px 8px; cursor: pointer;
}}
pre {{
  margin: 0; padding: 16px; overflow: auto; font-family: Consolas, "Courier New", monospace;
  font-size: 14px; line-height: 1.65; white-space: pre;
}}
.code-comment {{
  display: inline-block; width: 100%; color: #6f4e00; background: #fff7df;
  border-left: 4px solid #e3b341; padding-left: 8px; margin-left: -8px;
}}
.tok-keyword {{ color: #7c3aed; font-weight: 700; }}
.tok-class {{ color: #0f766e; font-weight: 700; }}
.tok-method {{ color: #1d4ed8; font-weight: 700; }}
.tok-variable {{ color: #9a3412; }}
.tok-string {{ color: #15803d; }}
.tok-number {{ color: #b45309; }}
.tok-comment {{ color: #687076; font-style: italic; }}
.blank {{
  background: #ffe08a; color: #241600; border: 1px solid #c88a00;
  border-radius: 4px; padding: 0 4px; font-weight: 800;
  box-shadow: 0 0 0 2px rgba(255, 224, 138, 0.35);
}}
.division-card {{
  display: grid; grid-template-columns: minmax(220px, 280px) minmax(0, 1fr); gap: 18px;
  align-items: center; background: #fff8d9; border: 1px solid #e3bd66;
  border-radius: 8px; padding: 18px; margin: 16px 0;
}}
.division-figure {{
  font-family: Consolas, "Courier New", monospace; font-size: 30px; font-weight: 800;
  color: #283133; background: #fffdf0; border-radius: 8px; padding: 16px 18px;
  min-height: 190px;
}}
.division-quotient {{ margin-left: 118px; color: var(--red); letter-spacing: 0.08em; }}
.division-row {{ display: flex; align-items: flex-start; }}
.division-divisor {{ width: 86px; text-align: right; padding: 9px 10px 0 0; }}
.division-bracket {{
  min-width: 132px; border-top: 4px solid #485052; border-left: 4px solid #485052;
  border-radius: 0 0 0 10px; padding: 7px 0 0 12px; line-height: 1.1;
}}
.division-product {{ margin: 8px 0 0 104px; color: #6d7477; }}
.division-line {{ width: 132px; height: 4px; background: #485052; margin: 2px 0 0 104px; }}
.division-remainder {{ margin-left: 142px; color: var(--green); }}
.division-explain p {{ margin: 8px 0; }}
.division-formula {{
  display: inline-block; font-weight: 800; color: #243235; background: white;
  border: 1px solid #e3bd66; border-radius: 999px; padding: 4px 11px;
}}
.table-wrap {{ overflow: auto; margin: 16px 0; border: 1px solid var(--line); border-radius: 8px; }}
table {{ width: 100%; border-collapse: collapse; background: white; font-size: 14px; }}
th, td {{ border-bottom: 1px solid var(--line); padding: 10px 12px; vertical-align: top; }}
th {{ background: #eef4f1; text-align: left; color: #243235; }}
figure {{ margin: 18px 0; border: 1px solid var(--line); border-radius: 8px; overflow: hidden; background: #fdfefe; }}
figure img {{ display: block; width: 100%; height: auto; }}
figcaption {{ font-size: 13px; color: var(--muted); padding: 8px 12px; border-top: 1px solid var(--line); }}
.no-results {{ display: none; padding: 18px; background: var(--amber-soft); color: var(--amber); border-radius: 8px; }}
.exercise.hidden {{ display: none; }}
.search-highlight {{
  background: #c7f0ff; color: #063547; border: 1px solid #1a8fb8;
  border-radius: 4px; padding: 0 2px; font-weight: 800;
  box-shadow: 0 0 0 2px rgba(67, 184, 224, 0.28);
}}
@media (max-width: 860px) {{
  main {{ padding: 24px 16px 60px; }}
  .topbar {{ position: static; margin-top: 0; }}
  .topbar-row {{ grid-template-columns: 1fr; }}
  .search-status {{ text-align: left; }}
  .instructor-panel {{ top: 14px; right: 14px; left: 14px; width: auto; max-height: calc(100vh - 28px); }}
  .instructor-login, .schedule-editor, .schedule-row {{ grid-template-columns: 1fr; }}
  .division-card {{ grid-template-columns: 1fr; }}
  .exercise {{ padding: 20px 16px; }}
  h1 {{ font-size: 27px; }}
}}
</style>
</head>
<body>
<div class="progress" id="progress"></div>
<div class="layout">
<main>
<div class="topbar">
  <div class="topbar-row">
    <div class="brand">EIMS 個人演習のヒント</div>
    <input class="search" id="search" type="search" placeholder="演習番号・用語・コードを検索">
    <div class="search-status" id="searchStatus">{total_count}件表示中</div>
    <button class="instructor-button" id="instructorButton" type="button">講師用</button>
  </div>
  <div class="tabs" role="tablist" aria-label="演習グループ">
    <button type="button" class="active" data-tab="all">すべて</button>
    <button type="button" data-tab="ex1">演習1</button>
    <button type="button" data-tab="ex2">演習2</button>
    <button type="button" data-tab="ex3">演習3</button>
    <button type="button" data-tab="ex4">演習4</button>
    <button type="button" data-tab="ex5">演習5</button>
  </div>
  <div class="schedule-banner">
    <strong>公開スケジュール:</strong>
    2026/6/9は演習1〜3、2026/6/10は演習4〜5を、演習ごとの予定時刻に合わせて表示します。
  </div>
  <div class="instructor-panel" id="instructorPanel">
    <h3>講師用メニュー</h3>
    <div class="instructor-login">
      <input id="instructorPassword" type="password" autocomplete="current-password" placeholder="パスワード">
      <button id="instructorLogin" type="button">ログイン</button>
    </div>
    <p class="instructor-status" id="instructorStatus">講師はログインすると、公開時刻前でも全ヒントを確認できます。</p>
    <div class="instructor-tools">
      <div class="instructor-actions">
        <label><input id="forceOpenHints" type="checkbox"> 全ヒントを強制表示</label>
        <button id="saveSchedule" type="button">このPCに保存</button>
        <button id="resetSchedule" type="button">初期時刻に戻す</button>
        <button id="instructorLogout" type="button">ログアウト</button>
      </div>
      <div class="schedule-editor" id="scheduleEditor"></div>
    </div>
  </div>
</div>
{body}
<p class="no-results" id="noResults">該当する演習がありません。検索語または公開時刻を確認してください。</p>
</main>
</div>
<script>
const search = document.getElementById('search');
const sections = Array.from(document.querySelectorAll('.exercise'));
const noResults = document.getElementById('noResults');
const searchStatus = document.getElementById('searchStatus');
const tabButtons = Array.from(document.querySelectorAll('[data-tab]'));
const instructorButton = document.getElementById('instructorButton');
const instructorPanel = document.getElementById('instructorPanel');
const instructorPassword = document.getElementById('instructorPassword');
const instructorLogin = document.getElementById('instructorLogin');
const instructorLogout = document.getElementById('instructorLogout');
const forceOpenHints = document.getElementById('forceOpenHints');
const saveSchedule = document.getElementById('saveSchedule');
const resetSchedule = document.getElementById('resetSchedule');
const scheduleEditor = document.getElementById('scheduleEditor');
const instructorStatus = document.getElementById('instructorStatus');
const defaultReleaseSchedule = {release_schedule_json};
const instructorPasswordHash = '37ae240244f300205edbbae2d790fa76351668469f9f37c968536b7843272a35';
const authKey = 'eimsInstructorAuthed';
const forceOpenKey = 'eimsInstructorForceOpen';
const scheduleOverrideKey = 'eimsReleaseScheduleOverrides';
let releaseSchedule = mergeReleaseSchedule(readJson(scheduleOverrideKey, {{}}));
let isInstructor = localStorage.getItem(authKey) === 'true';
let forceOpen = localStorage.getItem(forceOpenKey) !== 'false';
let activeGroup = 'all';
let releaseTimer = null;

function readJson(key, fallback) {{
  try {{
    const value = localStorage.getItem(key);
    return value ? JSON.parse(value) : fallback;
  }} catch (error) {{
    return fallback;
  }}
}}

function writeJson(key, value) {{
  localStorage.setItem(key, JSON.stringify(value));
}}

function mergeReleaseSchedule(overrides) {{
  return {{ ...defaultReleaseSchedule, ...overrides }};
}}

function formatLabel(value) {{
  if (!value) return '';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '';
  return `${{date.getMonth() + 1}}/${{date.getDate()}} ${{String(date.getHours()).padStart(2, '0')}}:${{String(date.getMinutes()).padStart(2, '0')}}`;
}}

function toDatetimeLocalValue(value) {{
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '';
  const yyyy = date.getFullYear();
  const mm = String(date.getMonth() + 1).padStart(2, '0');
  const dd = String(date.getDate()).padStart(2, '0');
  const hh = String(date.getHours()).padStart(2, '0');
  const mi = String(date.getMinutes()).padStart(2, '0');
  return `${{yyyy}}-${{mm}}-${{dd}}T${{hh}}:${{mi}}`;
}}

async function sha256(text) {{
  const bytes = new TextEncoder().encode(text);
  const hash = await crypto.subtle.digest('SHA-256', bytes);
  return Array.from(new Uint8Array(hash)).map(byte => byte.toString(16).padStart(2, '0')).join('');
}}

function setInstructorStatus(message) {{
  instructorStatus.textContent = message;
}}

function sectionLabel(section) {{
  return section.dataset.title.replace(' のヒント', '');
}}

function buildScheduleEditor() {{
  scheduleEditor.innerHTML = '';
  sections.forEach(section => {{
    const key = section.dataset.exercise;
    const schedule = releaseSchedule[key];
    if (!schedule) return;
    const row = document.createElement('label');
    row.className = 'schedule-row';
    row.innerHTML = `<span>${{sectionLabel(section)}}</span><input type="datetime-local" data-schedule-key="${{key}}" value="${{toDatetimeLocalValue(schedule.datetime)}}">`;
    scheduleEditor.appendChild(row);
  }});
}}

function refreshInstructorUi() {{
  instructorPanel.classList.toggle('authed', isInstructor);
  forceOpenHints.checked = forceOpen;
  instructorButton.textContent = isInstructor ? '講師用 ON' : '講師用';
  buildScheduleEditor();
}}

function scheduleFor(section) {{
  return releaseSchedule[section.dataset.exercise] || null;
}}

function isReleased(section) {{
  if (isInstructor && forceOpen) return true;
  const schedule = scheduleFor(section);
  if (!schedule || !schedule.datetime) return true;
  return Date.now() >= new Date(schedule.datetime).getTime();
}}

function releaseLabel(section) {{
  const schedule = scheduleFor(section);
  return schedule ? `${{schedule.label}}公開` : '';
}}

function ensureLockedMessage(section) {{
  let message = section.querySelector('.locked-message');
  if (!message) {{
    message = document.createElement('div');
    message.className = 'locked-message';
    section.appendChild(message);
  }}
  message.innerHTML = `このヒントは <strong>${{releaseLabel(section)}}</strong> です。<small>公開時刻になると、この画面を開いたままでも数秒以内に表示されます。</small>`;
}}

function removeLockedMessage(section) {{
  const message = section.querySelector('.locked-message');
  if (message) message.remove();
}}

function escapeRegExp(text) {{
  return text.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&');
}}

function removeSearchHighlights(root) {{
  root.querySelectorAll('mark.search-highlight').forEach(mark => {{
    mark.replaceWith(document.createTextNode(mark.textContent));
  }});
  root.normalize();
}}

function highlightSearchMatches(root, query) {{
  if (!query) return;
  const pattern = new RegExp(escapeRegExp(query), 'gi');
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {{
    acceptNode(node) {{
      const parent = node.parentElement;
      if (!parent) return NodeFilter.FILTER_REJECT;
      if (parent.closest('script, style, input, textarea, button, .release-note, .locked-message')) {{
        return NodeFilter.FILTER_REJECT;
      }}
      pattern.lastIndex = 0;
      return pattern.test(node.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
    }}
  }});
  const nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);
  nodes.forEach(node => {{
    pattern.lastIndex = 0;
    const fragment = document.createDocumentFragment();
    let lastIndex = 0;
    node.nodeValue.replace(pattern, (match, offset) => {{
      if (offset > lastIndex) {{
        fragment.appendChild(document.createTextNode(node.nodeValue.slice(lastIndex, offset)));
      }}
      const mark = document.createElement('mark');
      mark.className = 'search-highlight';
      mark.textContent = match;
      fragment.appendChild(mark);
      lastIndex = offset + match.length;
      return match;
    }});
    if (lastIndex < node.nodeValue.length) {{
      fragment.appendChild(document.createTextNode(node.nodeValue.slice(lastIndex)));
    }}
    node.replaceWith(fragment);
  }});
}}

function applyFilters() {{
  const q = search.value.trim().toLowerCase();
  let shown = 0;
  sections.forEach(section => removeSearchHighlights(section));
  sections.forEach(section => {{
    const released = isReleased(section);
    const schedule = scheduleFor(section);
    const groupHit = activeGroup === 'all' || section.dataset.group === activeGroup;
    const searchText = released ? section.textContent : section.dataset.title;
    const searchHit = !q || searchText.toLowerCase().includes(q);
    const hit = groupHit && searchHit;
    section.classList.toggle('hidden', !hit);
    section.classList.toggle('locked', !released);
    if (released) {{
      removeLockedMessage(section);
    }} else {{
      ensureLockedMessage(section);
    }}
    const heading = section.querySelector('h2');
    const existingNote = heading && heading.querySelector('.release-note');
    if (existingNote) existingNote.remove();
    if (heading && schedule) {{
      const note = document.createElement('span');
      note.className = released ? 'release-note open' : 'release-note';
      note.textContent = isInstructor && forceOpen ? '講師表示中' : released ? '公開中' : releaseLabel(section);
      heading.appendChild(note);
    }}
    if (hit && q) highlightSearchMatches(section, q);
    if (hit) shown++;
  }});
  noResults.style.display = shown ? 'none' : 'block';
  searchStatus.textContent = `${{shown}}件表示中`;
}}

function scheduleNextReleaseCheck() {{
  if (releaseTimer) clearTimeout(releaseTimer);
  if (isInstructor && forceOpen) return;
  const now = Date.now();
  const nextTimes = sections
    .map(section => scheduleFor(section))
    .filter(schedule => schedule && schedule.datetime)
    .map(schedule => new Date(schedule.datetime).getTime())
    .filter(time => Number.isFinite(time) && time > now);
  if (!nextTimes.length) return;
  const nextDelay = Math.min(...nextTimes) - now;
  releaseTimer = setTimeout(refreshReleaseState, Math.min(nextDelay + 250, 2147483647));
}}

function refreshReleaseState() {{
  applyFilters();
  scheduleNextReleaseCheck();
}}

instructorButton.addEventListener('click', () => {{
  instructorPanel.classList.toggle('open');
  if (instructorPanel.classList.contains('open')) {{
    refreshInstructorUi();
    if (!isInstructor) instructorPassword.focus();
  }}
}});

document.addEventListener('click', event => {{
  if (!instructorPanel.classList.contains('open')) return;
  const clickedPanel = instructorPanel.contains(event.target);
  const clickedButton = instructorButton.contains(event.target);
  if (!clickedPanel && !clickedButton) {{
    instructorPanel.classList.remove('open');
  }}
}});

document.addEventListener('keydown', event => {{
  if (event.key === 'Escape') instructorPanel.classList.remove('open');
}});

instructorLogin.addEventListener('click', async () => {{
  const input = instructorPassword.value;
  let hash = '';
  try {{
    hash = await sha256(input);
  }} catch (error) {{
    setInstructorStatus('このブラウザではパスワード確認機能を利用できません。別のブラウザで開いてください。');
    return;
  }}
  if (hash !== instructorPasswordHash) {{
    setInstructorStatus('パスワードが違います。');
    return;
  }}
  isInstructor = true;
  forceOpen = true;
  localStorage.setItem(authKey, 'true');
  localStorage.setItem(forceOpenKey, 'true');
  instructorPassword.value = '';
  setInstructorStatus('講師としてログインしました。全ヒントを表示しています。');
  refreshInstructorUi();
  refreshReleaseState();
}});

instructorPassword.addEventListener('keydown', event => {{
  if (event.key === 'Enter') instructorLogin.click();
}});

instructorLogout.addEventListener('click', () => {{
  isInstructor = false;
  localStorage.removeItem(authKey);
  setInstructorStatus('ログアウトしました。');
  refreshInstructorUi();
  refreshReleaseState();
}});

forceOpenHints.addEventListener('change', () => {{
  forceOpen = forceOpenHints.checked;
  localStorage.setItem(forceOpenKey, String(forceOpen));
  setInstructorStatus(forceOpen ? '全ヒントを強制表示しています。' : '強制表示をOFFにしました。設定した公開日時で動作確認できます。');
  refreshReleaseState();
}});

saveSchedule.addEventListener('click', () => {{
  const overrides = {{}};
  scheduleEditor.querySelectorAll('[data-schedule-key]').forEach(input => {{
    if (!input.value) return;
    overrides[input.dataset.scheduleKey] = {{
      label: formatLabel(input.value),
      datetime: input.value,
    }};
  }});
  writeJson(scheduleOverrideKey, overrides);
  releaseSchedule = mergeReleaseSchedule(overrides);
  buildScheduleEditor();
  setInstructorStatus(forceOpen ? 'このPC用の公開日時を保存しました。強制表示をOFFにすると公開状態を確認できます。' : 'このPC用の公開日時を保存し、公開状態を更新しました。');
  refreshReleaseState();
}});

resetSchedule.addEventListener('click', () => {{
  localStorage.removeItem(scheduleOverrideKey);
  releaseSchedule = mergeReleaseSchedule({{}});
  buildScheduleEditor();
  setInstructorStatus('公開日時を初期設定に戻しました。');
  refreshReleaseState();
}});

search.addEventListener('input', refreshReleaseState);
tabButtons.forEach(button => {{
  button.addEventListener('click', () => {{
    activeGroup = button.dataset.tab;
    tabButtons.forEach(tab => tab.classList.toggle('active', tab === button));
    refreshReleaseState();
    const firstVisible = sections.find(section => !section.classList.contains('hidden'));
    if (firstVisible) firstVisible.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
  }});
}});
document.querySelectorAll('.code-toolbar button').forEach(button => {{
  button.addEventListener('click', async () => {{
    const code = button.closest('.code-shell').querySelector('code').innerText;
    await navigator.clipboard.writeText(code);
    const old = button.textContent;
    button.textContent = 'コピー済み';
    setTimeout(() => button.textContent = old, 1200);
  }});
}});
const progress = document.getElementById('progress');
window.addEventListener('scroll', () => {{
  const max = document.documentElement.scrollHeight - window.innerHeight;
  progress.style.width = max > 0 ? `${{(window.scrollY / max) * 100}}%` : '0';
}});
window.addEventListener('focus', refreshReleaseState);
document.addEventListener('visibilitychange', () => {{
  if (!document.hidden) refreshReleaseState();
}});
refreshReleaseState();
setInterval(refreshReleaseState, 5000);
</script>
</body>
</html>
"""


def main() -> None:
    body, toc = render_blocks(SOURCE.read_text(encoding="utf-8"))
    OUTPUT.write_text(build_html(body, toc), encoding="utf-8", newline="\n")
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    main()
