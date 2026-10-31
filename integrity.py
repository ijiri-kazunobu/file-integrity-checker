import hashlib
from pathlib import Path

folder = Path("sample_site")

for item in folder.iterdir():
    if item.is_file():
        data = item.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        print(f"{item.name}: {digest}")