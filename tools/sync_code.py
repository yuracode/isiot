"""README.md の <!-- include: ファイル名 --> の直後のコードブロックを、.py の中身で更新する。

使い方:python3 tools/sync_code.py   (リポジトリのルートで実行)
.py を直したら、これを実行すれば README のコードもそろう。
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAT = re.compile(r"<!-- include: (\S+) -->\n(```python\n.*?\n```\n?)?", re.S)

for md in ROOT.rglob("README.md"):
    text = md.read_text(encoding="utf-8")

    def rep(m):
        code = (md.parent / m.group(1)).read_text(encoding="utf-8").rstrip("\n")
        return f"<!-- include: {m.group(1)} -->\n```python\n{code}\n```\n"

    new = PAT.sub(rep, text)
    if new != text:
        md.write_text(new, encoding="utf-8")
        print("updated", md.relative_to(ROOT))
