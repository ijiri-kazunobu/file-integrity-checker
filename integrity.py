import hashlib
import json
from pathlib import Path

def calculate_hashes(folder):
    hashes = {}
    for item in folder.iterdir():
        if item.is_file():
            data = item.read_bytes()
            digest =hashlib.sha256(data).hexdigest()
            hashes[item.name] = digest 
    return hashes

def init(folder):
    hashes = calculate_hashes(folder)
    text = json.dumps(hashes, indent=2, ensure_ascii=False)
    Path("baseline.json").write_text(text, encoding = "utf-8")
    print(f"基準データを保存しました ({len(hashes)}ファイル)")

def check(folder):
    text = Path("baseline.json").read_text(encoding="utf-8")
    baseline = json.loads(text)
    current = calculate_hashes(folder)

    for name in current:
        if name not in baseline:
            print(f"[追加] {name}")
        elif current[name] != baseline[name]:
            print(f"[変更] {name}")

    for name in baseline:
        if name not in current:
            print(f"[削除] {name}")


folder = Path("sample_site")
check(folder)