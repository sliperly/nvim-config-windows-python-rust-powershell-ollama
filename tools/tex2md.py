#!/usr/bin/env python3
"""Build per-language Markdown files from the bilingual LaTeX sources in docs/.

For every docs/NAME_ru-en.tex it writes docs/NAME_ru.md and docs/NAME_en.md,
so the Markdown and PDF versions of a guide always come from the same source.

Usage (from the repository root):  python tools/tex2md.py
Only the small subset of LaTeX used in these documents is supported.
"""
import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
GUIDES = ("install-neovim", "install-markdown-latex", "cheatsheet-neovim")
UI = {
    "ru": {"other": "English", "pdf": "PDF (русский и английский)", "self": "Русский"},
    "en": {"other": "Русский", "pdf": "PDF (Russian and English)", "self": "English"},
}


# ---------- helpers ----------
def balanced(s, i):
    """s[i] == '{'. Return (content, index after the closing brace)."""
    assert s[i] == "{", s[i:i + 20]
    depth = 0
    for j in range(i, len(s)):
        c = s[j]
        if c == "\\":
            continue
        if c == "{" and s[j - 1] != "\\":
            depth += 1
        elif c == "}" and s[j - 1] != "\\":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
    raise ValueError("unbalanced braces near: " + s[i:i + 40])


def unescape_code(t):
    t = t.replace("\\textbackslash ", "\\").replace("\\textbackslash", "\\")
    t = t.replace("\\bs ", "\\").replace("\\bs", "\\")
    for a, b in (("\\$", "$"), ("\\%", "%"), ("\\_", "_"), ("\\&", "&"), ("\\#", "#"),
                 ("\\{", "{"), ("\\}", "}")):
        t = t.replace(a, b)
    return t.replace("--", "--")


def code_span(t):
    t = unescape_code(t.strip())
    fence = "``" if "`" in t else "`"
    return f"{fence}{t}{fence}"


def replace_cmd(s, name, fn):
    """Replace \\name{...} (balanced) using fn(content)."""
    out, i, pat = [], 0, "\\" + name + "{"
    while True:
        j = s.find(pat, i)
        if j < 0:
            out.append(s[i:])
            return "".join(out)
        out.append(s[i:j])
        content, end = balanced(s, j + len(pat) - 1)
        out.append(fn(content))
        i = end


def inline(t, lang):
    t = replace_cmd(t, "key", lambda c: "\x00" + code_span(c) + "\x01")
    t = replace_cmd(t, "textbf", lambda c: "**" + inline(c, lang) + "**")
    t = replace_cmd(t, "emph", lambda c: "*" + inline(c, lang) + "*")
    t = t.replace("\\textbackslash ", "\\").replace("\\bs ", "\\")
    for a, b in (("\\$", "$"), ("\\%", "%"), ("\\_", "_"), ("\\&", "&"), ("\\#", "#")):
        t = t.replace(a, b)
    t = t.replace("``", "\u201c").replace("''", "\u201d").replace("---", "\u2014").replace("--", "\u2013")
    t = re.sub(r"\\(leavevmode|noindent|sloppy)\b\s*", "", t)
    t = t.replace("\\newline", "<br>")
    # link guide names
    for g in GUIDES:
        t = t.replace(f"\x00`{g}`\x01", f"[`{g}`]({g}_{lang}.md)")
    return t.replace("\x00", "").replace("\x01", "")


def fence_lang(code):
    if re.search(r"^\s*(vim\.|local |require\()", code, re.M):
        return "lua"
    if re.search(r"^\\documentclass", code, re.M):
        return "latex"
    if re.match(r"^\s*(:|\\)", code) or code.lstrip().startswith(":"):
        return "vim"
    if re.search(r"^# |\*\*", code, re.M):
        return "text"
    return "powershell"


def fenced(code):
    code = code.strip("\n")
    return "```" + fence_lang(code) + "\n" + code + "\n```"


# ---------- body conversion ----------
ENV = re.compile(
    r"\\begin\{(lstlisting|Verbatim)\}(?:\[[^\]]*\])?\n?(.*?)\\end\{\1\}"
    r"|\\begin\{(itemize|enumerate)\}(?:\\setlength\\itemsep\{[^}]*\})?(.*?)\\end\{\3\}",
    re.S,
)


def convert_text(t, lang):
    """Convert one chunk of prose/environments to Markdown."""
    t = re.sub(r"(?<!\\)%.*", "", t)  # comments
    t = re.sub(r"\\(begingroup|endgroup)\b|\\(hyphenpenalty|exhyphenpenalty)=\d+ ?", "", t)
    t = re.sub(r"\{\\Large\\bfseries (.*?)\\par\}", lambda m: f"\n\n# {m.group(1)}\n\n", t, flags=re.S)
    t = re.sub(r"\\needspace\{[^}]*\}|\\(wide|narrow|sloppy|par)\b", "", t)
    out, pos = [], 0
    blocks = []

    def stash(md):
        blocks.append(md)
        return f"\n\n@@BLOCK{len(blocks) - 1}@@\n\n"

    def repl(m):
        if m.group(1):
            return stash(fenced(m.group(2)))
        kind, body = m.group(3), m.group(4)
        items = [x.strip() for x in re.split(r"\\item\b", body)[1:]]
        lines = []
        for n, it in enumerate(items, 1):
            bullet = "-" if kind == "itemize" else f"{n}."
            it = " ".join(inline(it, lang).split())
            lines.append(f"{bullet} {it}")
        return stash("\n".join(lines))

    t = ENV.sub(repl, t)

    # headings and title
    t = replace_cmd(t, "section*", lambda c: f"\n\n## {inline(c, lang)}\n\n")
    t = replace_cmd(t, "subsection*", lambda c: f"\n\n### {inline(c, lang)}\n\n")
    t = re.sub(r"\{\\Large\\bfseries (.*?)\\par\}", lambda m: f"\n\n# {inline(m.group(1), lang)}\n\n", t, flags=re.S)

    paras = re.split(r"\n\s*\n", t)
    res = []
    for p in paras:
        p = p.strip()
        if not p:
            continue
        m = re.fullmatch(r"@@BLOCK(\d+)@@", p)
        if m:
            res.append(blocks[int(m.group(1))])
        elif p.startswith("# "):
            res.append("# " + inline(p[2:], lang))
        elif p.startswith("#"):
            res.append(p)
        else:
            res.append(" ".join(inline(p, lang).split()))
    return "\n\n".join(res)


def pick(bilingual, lang):
    """'Режимы / Modes' -> the part in the requested language."""
    parts = [x.strip() for x in bilingual.split(" / ")]
    if len(parts) != 2:
        return bilingual
    cyr = [bool(re.search("[А-Яа-яЁё]", x)) for x in parts]
    if cyr[0] == cyr[1]:
        return bilingual
    want = lang == "ru"
    return parts[0] if cyr[0] == want else parts[1]


def split_rows(body):
    rows, cur, depth = [], "", 0
    i = 0
    while i < len(body):
        c = body[i]
        if c == "{" and body[i - 1:i] != "\\":
            depth += 1
        elif c == "}" and body[i - 1:i] != "\\":
            depth -= 1
        if body.startswith("\\\\", i) and depth == 0:
            rows.append(cur.strip())
            cur = ""
            i += 2
            continue
        cur += c
        i += 1
    if cur.strip():
        rows.append(cur.strip())
    return rows


def convert_table(body, lang):
    body = body.strip()
    assert body.startswith("\\hdr"), body[:40]
    pos, hdr = len("\\hdr"), []
    for _ in range(3):
        c, pos = balanced(body, pos)
        hdr.append(c)
    rest = body[pos:].replace("\\toprule", "").replace("\\midrule", "")
    rows = [r for r in split_rows(rest) if r]
    col = 1 if lang == "ru" else 2
    head = [pick(hdr[0], lang), hdr[col].strip()]
    lines = ["| " + " | ".join(head) + " |", "|---|---|"]
    for r in rows:
        cells = [c.strip() for c in r.split(" & ")]
        key = cells[0]
        key_md = "<br>".join(code_span(k) for k in re.split(r"\\newline\s*", key))
        desc = inline(cells[col], lang).replace("|", "\\|")
        lines.append(f"| {key_md} | {desc} |")
    return "\n".join(lines)


def build(tex, lang):
    body = tex.split("\\begin{document}", 1)[1].rsplit("\\end{document}", 1)[0]
    # tokenise: paracol blocks, longtables, loose full-width material
    tok = re.compile(
        r"\\begin\{paracol\}\{2\}(.*?)\\end\{paracol\}|\\begin\{longtable\}\{(?:[^{}]|\{\})*\}(.*?)\\end\{longtable\}"
        r"|\\section\*\{([^}]*)\}",
        re.S,
    )
    out, pos = [], 0
    for m in tok.finditer(body):
        loose = body[pos:m.start()]
        if loose.strip():
            out.append(convert_text(loose, lang))
        pos = m.end()
        if m.group(1) is not None:
            for chunk in re.split(r"\\switchcolumn\*?", m.group(1)):
                c = chunk.strip()
                if c.startswith("\\RU"):
                    mine = lang == "ru"
                elif c.startswith("\\EN"):
                    mine = lang == "en"
                else:
                    continue
                if mine:
                    out.append(convert_text(c[3:], lang))
        elif m.group(2) is not None:
            out.append(convert_table(m.group(2), lang))
        else:
            out.append(f"## {pick(m.group(3), lang)}")
    tail = body[pos:]
    if tail.strip():
        out.append(convert_text(tail, lang))
    return "\n\n".join(x for x in out if x.strip()) + "\n"


def main():
    n = 0
    for tex_path in sorted(DOCS.glob("*_ru-en.tex")):
        name = tex_path.name[: -len("_ru-en.tex")]
        tex = tex_path.read_text(encoding="utf-8")
        for lang in ("ru", "en"):
            md = build(tex, lang)
            first, _, rest = md.partition("\n")
            u = UI[lang]
            nav = f"{u['self']} | [{u['other']}]({name}_{'en' if lang == 'ru' else 'ru'}.md) | [{u['pdf']}]({name}_ru-en.pdf)"
            md = f"{first}\n\n{nav}\n{rest}"
            (DOCS / f"{name}_{lang}.md").write_text(md, encoding="utf-8", newline="\n")
            n += 1
            print("wrote", f"{name}_{lang}.md")
    if not n:
        sys.exit("no *_ru-en.tex files found in " + str(DOCS))


if __name__ == "__main__":
    main()
