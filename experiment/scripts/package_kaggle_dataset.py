"""Package the existing seminar data without modifying it."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
target = ROOT / "outputs" / "s07_hcmus_rag_corpus.zip"
target.parent.mkdir(exist_ok=True)
files = sorted(p for p in (ROOT / "data").rglob("*") if p.is_file())
manifest = {str(p.relative_to(ROOT / "data")).replace("\\", "/"):
            hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
    for path in files:
        archive.write(path, str(path.relative_to(ROOT / "data")))
    archive.writestr("SHA256SUMS.json", json.dumps(manifest, indent=2))
    archive.writestr("README.md", (ROOT / "README.md").read_text(encoding="utf-8"))
print(target, target.stat().st_size)
