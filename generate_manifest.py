"""Generate manifest for app code only"""
import os
import json
import hashlib
from pathlib import Path
from datetime import datetime

def calculate_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()[:16]

def main():
    base_dir = Path(__file__).parent
    files_dir = base_dir / "files"
    
    manifest = {
        "version": "1.0.0",
        "build_time": datetime.now().isoformat(),
        "files": {}
    }
    
    for file_path in files_dir.rglob("*"):
        if file_path.is_file():
            rel_path = str(file_path.relative_to(files_dir)).replace("\\", "/")
            manifest["files"][rel_path] = {
                "hash": calculate_hash(file_path),
                "size": file_path.stat().st_size
            }
    
    with open(base_dir / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    
    print(f"Generated manifest with {len(manifest['files'])} files")

if __name__ == "__main__":
    main()
