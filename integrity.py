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

folder = Path("sample_site")
hashes = calculate_hashes(folder)

text = json.dumps(hashes, indent=2, ensure_ascii=False)
Path("baseline.json").write_text(text, encoding = "utf-8")
print(f"基準データを保存しました ({len(hashes)}ファイル)")