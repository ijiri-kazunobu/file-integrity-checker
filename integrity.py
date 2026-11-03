import argparse
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
    if not Path("baseline.json").exists():
        print("基準データがありません。先に init を実行してください")
        return
    
    text = Path("baseline.json").read_text(encoding="utf-8")
    baseline = json.loads(text)
    current = calculate_hashes(folder)
    changes =0

    for name in current:
        if name not in baseline:
            print(f"[追加] {name}")
            changes += 1
        elif current[name] != baseline[name]:
            print(f"[変更] {name}")
            changes += 1

    for name in baseline:
        if name not in current:
            print(f"[削除] {name}")
            changes += 1

    if changes == 0:
        print("異常はありませんでした")

parser = argparse.ArgumentParser(description="ファイルの改ざんを検知するツール")
parser.add_argument("command", choices=["init","check"],help="init: 基準データを保存 / check: 改ざんを検査")
parser.add_argument("folder", help="監視するフォルダのパス")
args = parser.parse_args()

folder = Path(args.folder)
if args.command == "init":
    init(folder)
elif args.command == "check":
    check(folder)