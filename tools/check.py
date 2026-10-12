"""リポジトリのチェック:相対リンク・アンカー・README と .py の一致・本体LEDの書き方。

使い方:python3 tools/check.py   (問題がなければ problems: 0)
"""
import pathlib
import re
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent


def slug(h):
    h = h.strip().lower()
    h = "".join(c for c in h if c in " -_" or unicodedata.category(c)[0] in "LN")
    return h.replace(" ", "-")


bad = 0
for md in ROOT.rglob("*.md"):
    text = re.sub(r"```.*?```", "", md.read_text(encoding="utf-8"), flags=re.S)  # コードブロックは除く
    for link in re.findall(r"\]\(([^)]+)\)", text):
        if link.startswith("http"):
            continue
        path, _, anchor = link.partition("#")
        tgt = (md.parent / path).resolve() if path else md
        if not tgt.exists():
            print("MISSING", md.relative_to(ROOT), link); bad += 1; continue
        if anchor:
            heads = [slug(h) for h in re.findall(r"^#+ (.+)$", tgt.read_text(encoding="utf-8"), re.M)]
            if anchor not in heads:
                print("BAD ANCHOR", md.relative_to(ROOT), link); bad += 1

for py in ROOT.rglob("*.py"):
    if py.parent.name in ("slides", "tools"):
        continue
    code = py.read_text(encoding="utf-8").rstrip("\n")
    if f"```python\n{code}\n```" not in (py.parent / "README.md").read_text(encoding="utf-8"):
        print("CODE NOT IN README", py.relative_to(ROOT)); bad += 1
    if "Pin(25" in code:
        print("USE Pin(\"LED\")", py.relative_to(ROOT)); bad += 1

print("problems:", bad)
