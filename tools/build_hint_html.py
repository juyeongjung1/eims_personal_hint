from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "EIMS個人演習のヒント(総合版).md"
OUTPUT = ROOT / "EIMS個人演習のヒント(総合版).html"

# 配布前にここへ時刻を入れると、その時刻以降に各演習のヒントが表示されます。
# 空欄の演習は常に表示されます。例: "ex1": "10:00"
RELEASE_SCHEDULE = {
    "ex1": "",
    "ex2": "",
    "ex3": "",
    "ex4": "",
    "ex5": "",
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
        f"<p>ヒントを演習ごとに整理し、参照テキスト・コード・重要ポイントを読みやすくまとめたHTML版です。</p></header>"
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
            toc.append((sid, title, group))
            parts.append(f'<section class="exercise" id="{sid}" data-title="{html.escape(title)}" data-group="{group}"><h2>{inline(title)}</h2>')
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
  display: grid; grid-template-columns: 180px minmax(220px, 1fr) auto; gap: 12px;
  align-items: center; margin-bottom: 10px;
}}
.search {{
  width: 100%; height: 40px; border: 1px solid var(--line); border-radius: 6px;
  padding: 0 10px; background: white; font-size: 14px;
}}
.search-status {{
  color: var(--muted); font-size: 13px; white-space: nowrap; text-align: right;
}}
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
@media (max-width: 860px) {{
  main {{ padding: 24px 16px 60px; }}
  .topbar {{ position: static; margin-top: 0; }}
  .topbar-row {{ grid-template-columns: 1fr; }}
  .search-status {{ text-align: left; }}
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
  </div>
  <div class="tabs" role="tablist" aria-label="演習グループ">
    <button type="button" class="active" data-tab="all">すべて</button>
    <button type="button" data-tab="ex1">演習1</button>
    <button type="button" data-tab="ex2">演習2</button>
    <button type="button" data-tab="ex3">演習3</button>
    <button type="button" data-tab="ex4">演習4</button>
    <button type="button" data-tab="ex5">演習5</button>
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
const releaseSchedule = {release_schedule_json};
let activeGroup = 'all';

function minutesOfDay(timeText) {{
  const [hour, minute] = timeText.split(':').map(Number);
  return hour * 60 + minute;
}}

function isReleased(group) {{
  const releaseTime = releaseSchedule[group];
  if (!releaseTime) return true;
  const now = new Date();
  const currentMinutes = now.getHours() * 60 + now.getMinutes();
  return currentMinutes >= minutesOfDay(releaseTime);
}}

function releaseLabel(group) {{
  return releaseSchedule[group] ? `${{releaseSchedule[group]}}公開` : '';
}}

function applyFilters() {{
  const q = search.value.trim().toLowerCase();
  let shown = 0;
  sections.forEach(section => {{
    const groupHit = activeGroup === 'all' || section.dataset.group === activeGroup;
    const searchHit = !q || section.textContent.toLowerCase().includes(q);
    const releaseHit = isReleased(section.dataset.group);
    const hit = groupHit && searchHit && releaseHit;
    section.classList.toggle('hidden', !hit);
    const heading = section.querySelector('h2');
    const existingNote = heading && heading.querySelector('.release-note');
    if (existingNote) existingNote.remove();
    if (heading && releaseSchedule[section.dataset.group]) {{
      const note = document.createElement('span');
      note.className = 'release-note';
      note.textContent = releaseLabel(section.dataset.group);
      heading.appendChild(note);
    }}
    if (hit) shown++;
  }});
  noResults.style.display = shown ? 'none' : 'block';
  searchStatus.textContent = `${{shown}}件表示中`;
}}

search.addEventListener('input', applyFilters);
tabButtons.forEach(button => {{
  button.addEventListener('click', () => {{
    activeGroup = button.dataset.tab;
    tabButtons.forEach(tab => tab.classList.toggle('active', tab === button));
    applyFilters();
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
applyFilters();
setInterval(applyFilters, 30000);
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
