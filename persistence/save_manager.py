import json
import os
import shutil
import tempfile
from pathlib import Path

CURRENT_SCHEMA = 1

class SaveError(Exception):
    pass

class SaveManager:
    """JSON saves with atomic replacement and one rolling backup."""
    def __init__(self, directory="saves"):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def _paths(self, slot):
        if not slot.replace("_", "").isalnum():
            raise ValueError("Save slot may contain only letters, numbers and underscores.")
        target = self.directory / f"{slot}.json"
        return target, target.with_suffix(".json.bak")

    def save(self, slot, state):
        target, backup = self._paths(slot)
        payload = dict(state)
        payload["schema_version"] = CURRENT_SCHEMA
        fd, temp_name = tempfile.mkstemp(prefix=target.stem, suffix=".tmp", dir=self.directory)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                json.dump(payload, stream, indent=2, ensure_ascii=False)
                stream.flush()
                os.fsync(stream.fileno())
            if target.exists():
                shutil.copy2(target, backup)
            os.replace(temp_name, target)
        finally:
            if os.path.exists(temp_name):
                os.unlink(temp_name)
        return target

    def load(self, slot):
        target, backup = self._paths(slot)
        for candidate in (target, backup):
            if not candidate.exists():
                continue
            try:
                with candidate.open("r", encoding="utf-8") as stream:
                    state = json.load(stream)
                if state.get("schema_version") != CURRENT_SCHEMA:
                    raise SaveError(f"Unsupported save schema: {state.get('schema_version')}")
                return state
            except (json.JSONDecodeError, OSError):
                continue
        raise SaveError(f"No valid save or backup found for slot '{slot}'.")
