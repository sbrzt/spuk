# src/manifest.py

import hashlib
import json
from pathlib import Path
from typing import Dict

MANIFEST_NAME = ".manifest.json"


def hash_templates(templates_dir: Path) -> str:
    """Fingerprint every template file so a template edit invalidates all entities."""
    digest = hashlib.sha1()
    for path in sorted(Path(templates_dir).glob("**/*.html")):
        stat = path.stat()
        digest.update(f"{path.name}:{stat.st_mtime_ns}:{stat.st_size}".encode("utf-8"))
    return digest.hexdigest()


def hash_entity(entity, template_hash: str) -> str:
    """Content hash for one entity: its triples plus the current template fingerprint."""
    digest = hashlib.sha1(template_hash.encode("utf-8"))
    lines = sorted(f"{s} {p} {o}" for s, p, o in entity.subject_triples + entity.object_triples)
    digest.update("\n".join(lines).encode("utf-8"))
    return digest.hexdigest()


def load_manifest(output_dir: Path) -> Dict[str, str]:
    manifest_path = output_dir / MANIFEST_NAME
    if not manifest_path.exists():
        return {}
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def save_manifest(output_dir: Path, manifest: Dict[str, str]) -> None:
    (output_dir / MANIFEST_NAME).write_text(
        json.dumps(manifest, separators=(",", ":")), encoding="utf-8"
    )
