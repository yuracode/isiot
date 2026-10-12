#!/usr/bin/env bash
# Windows の PowerPoint を使って slides/pico_sensor_intro.pptx を PDF にする(WSL から実行)
# 使い方:bash tools/export_pdf_powerpoint.sh   (リポジトリのルートで実行)
set -euo pipefail
PS=/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe
ROOT=$(cd "$(dirname "$0")/.." && pwd)
WTMP=$("$PS" -NoProfile -Command '[IO.Path]::GetTempPath()' | tr -d '\r')
W="${WTMP}picoslides"
L=$(wslpath "$WTMP")/picoslides
mkdir -p "$L"
rm -f "$L/pico_sensor_intro.pdf"
cp "$ROOT/slides/pico_sensor_intro.pptx" "$L/"
"$PS" -NoProfile -Command "
\$app = New-Object -ComObject PowerPoint.Application
try {
  \$p = \$app.Presentations.Open('$W\\pico_sensor_intro.pptx', -1, 0, 0)
  \$p.SaveAs('$W\\pico_sensor_intro.pdf', 32)   # 32 = PDF
  \$p.Close()
} finally { \$app.Quit() }"
cp "$L/pico_sensor_intro.pdf" "$ROOT/slides/"
echo "PDF を作りました:slides/pico_sensor_intro.pdf"
