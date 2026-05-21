from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "EIMS個人演習のヒント(総合版).md"
OUTPUT = ROOT / "EIMS個人演習のヒント(総合版).html"


def slugify(text: str, index: int) -> str:
    token = re.sub(r"[^\w一-龯ぁ-んァ-ヶー.]+", "-", text, flags=re.UNICODE).strip("-")
    return token or f"section-{index}"


def inline(text: str) -> str:
    escaped = html.escape(text)

    def code_repl(match: re.Match[str]) -> str:
        return f"<code>{match.group(1)}</code>"

    escaped = re.sub(r"`([^`]+)`", code_repl, escaped)
    return escaped


def code_html(code: str, lang: str) -> str:
    escaped = html.escape(code.rstrip("\n"))
    escaped = escaped.replace("____", '<span class="blank">____</span>')
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


def render_blocks(markdown: str) -> tuple[str, list[tuple[str, str]]]:
    lines = markdown.splitlines()
    parts: list[str] = []
    toc: list[tuple[str, str]] = []
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
                f"<p>ヒントを演習ごとに整理し、参照テキスト・コード・画像を読みやすくまとめたHTML版です。</p></header>"
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
            toc.append((sid, title))
            parts.append(f'<section class="exercise" id="{sid}" data-title="{html.escape(title)}"><h2>{inline(title)}</h2>')
            section_open = True
            i += 1
            continue

        if line.startswith("### "):
            flush_paragraph()
            flush_list()
            title = line[4:].strip()
            parts.append(f"<h3>{inline(title)}</h3>")
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


def build_html(body: str, toc: list[tuple[str, str]]) -> str:
    toc_items = "\n".join(f'<a href="#{sid}">{inline(title)}</a>' for sid, title in toc)
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
  --green: #1f7a62;
  --green-soft: #e6f3ee;
  --amber: #946200;
  --amber-soft: #fff3d6;
  --code: #101820;
  --blue: #2f5f9e;
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
.layout {{ display: grid; grid-template-columns: 280px minmax(0, 1fr); min-height: 100vh; }}
.sidebar {{
  position: sticky; top: 0; height: 100vh; overflow: auto;
  padding: 24px 18px; border-right: 1px solid var(--line); background: #fbfcfa;
}}
.brand {{ font-weight: 700; font-size: 15px; margin-bottom: 16px; color: var(--green); }}
.search {{
  width: 100%; height: 40px; border: 1px solid var(--line); border-radius: 6px;
  padding: 0 10px; background: white; font-size: 14px;
}}
nav {{ display: grid; gap: 4px; margin-top: 18px; }}
nav a {{
  color: var(--ink); text-decoration: none; padding: 8px 10px; border-radius: 6px;
  font-size: 14px; line-height: 1.35;
}}
nav a:hover, nav a.active {{ background: var(--green-soft); color: var(--green); }}
main {{ max-width: 1040px; width: 100%; padding: 40px 42px 80px; }}
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
  border-left: 5px solid var(--green); background: var(--green-soft);
  padding: 12px 14px; margin: 14px 0; border-radius: 0 6px 6px 0; font-weight: 700;
}}
.lead-label {{ font-weight: 700; color: var(--green); margin-top: 18px; }}
ul, ol {{ padding-left: 1.4rem; }}
li {{ margin: 5px 0; }}
code {{ background: #eef2f1; padding: 0.1em 0.35em; border-radius: 4px; font-family: Consolas, "Courier New", monospace; }}
.code-shell {{ background: var(--code); color: #edf7f5; border-radius: 8px; overflow: hidden; margin: 16px 0; }}
.code-toolbar {{ display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; background: #17242d; color: #b9c9c7; font-size: 12px; }}
.code-toolbar button {{ border: 1px solid #48606b; background: #22333d; color: white; border-radius: 5px; padding: 4px 8px; cursor: pointer; }}
pre {{ margin: 0; padding: 16px; overflow: auto; font-family: Consolas, "Courier New", monospace; font-size: 14px; line-height: 1.6; }}
.blank {{ background: var(--amber-soft); color: #2b1b00; border: 1px solid #e3bd66; border-radius: 4px; padding: 0 3px; font-weight: 700; }}
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
  .layout {{ grid-template-columns: 1fr; }}
  .sidebar {{ position: static; height: auto; border-right: 0; border-bottom: 1px solid var(--line); }}
  main {{ padding: 24px 16px 60px; }}
  .exercise {{ padding: 20px 16px; }}
  h1 {{ font-size: 27px; }}
}}
</style>
</head>
<body>
<div class="progress" id="progress"></div>
<div class="layout">
<aside class="sidebar">
  <div class="brand">EIMS 個人演習のヒント</div>
  <input class="search" id="search" type="search" placeholder="演習・用語を検索">
  <nav id="toc">{toc_items}</nav>
</aside>
<main>
{body}
<p class="no-results" id="noResults">該当する演習がありません。検索語を変えてください。</p>
</main>
</div>
<script>
const search = document.getElementById('search');
const sections = Array.from(document.querySelectorAll('.exercise'));
const noResults = document.getElementById('noResults');
search.addEventListener('input', () => {{
  const q = search.value.trim().toLowerCase();
  let shown = 0;
  sections.forEach(section => {{
    const hit = !q || section.textContent.toLowerCase().includes(q);
    section.classList.toggle('hidden', !hit);
    if (hit) shown++;
  }});
  noResults.style.display = shown ? 'none' : 'block';
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
const tocLinks = Array.from(document.querySelectorAll('nav a'));
const observer = new IntersectionObserver(entries => {{
  entries.forEach(entry => {{
    if (entry.isIntersecting) {{
      tocLinks.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + entry.target.id));
    }}
  }});
}}, {{ rootMargin: '-30% 0px -60% 0px', threshold: 0 }});
sections.forEach(section => observer.observe(section));
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
