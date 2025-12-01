import json
from pathlib import Path
from typing import Callable
import hashlib
from datetime import datetime, timedelta


class ParsingClass:
    def __init__(self, log_dir: str, state_file: str = "state/parsed_state.json"):
        self.log_dir = Path(log_dir)
        self.state_file = Path(state_file)

        # Initializes state
        self.state = self._load_state()

        # Register: pattern -> parsing function
        self.parsers = {}

    def _load_state(self) -> dict:
        if self.state_file.exists():
            with open(self.state) as f:
                return json.load(f)
        return {"parsed_files": {}}

    def _save_state(self):
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, "w") as f:
            json.dump(self.state, f, indent=2)

    def _file_hash(self, file_path: Path) -> str:
        """Creates file hash to detect any changes"""
        hasher = hashlib.md5()
        with open(file_path, "rb") as f:
            hasher.update(f.read())
        return hasher.hexdigest()

    def _marked_as_parsed(self, file_path: Path, file_hash: str):
        self.state["parsed_files"][str(file_path)] = file_hash
        self._save_state()

    def _has_been_parsed(self, file_path: Path, file_hash: str) -> bool:
        return (
            str(file_path) in self.state["parsed_files"]
            and self.state["parsed_files"][str(file_path)] == file_hash
        )

    def register_parsers(self, patterns: str, func: Callable):
        """Registers functions for log types"""
        self.parsers[patterns] = func

    def _recent_dirs(self, days=7):
        cutoff = datetime.now() - timedelta(days=days)
        recent = []

        for d in self.log_dir.iterdir():
            if d.is_dir():
                try:
                    dt = datetime.strptime(d.name, "%Y.%m.%dT%H")
                    if dt >= cutoff:
                        recent.append(d)
                except ValueError:
                    continue
        return recent

    def discover_logs(self):
        logs = []
        for d in self._recent_dirs(days=7):
            for pattern in self.parsers:
                logs.extend(d.rglob(pattern))
        return logs

    def parse_all(self):
        logs = self.discover_logs()
        print(f"Found {len(logs)} logs")

        for log_file in logs:
            file_hash = self._file_hash(log_file)

            if self._has_been_parsed(log_file, file_hash):
                print(f"[SKIP] Already Parsed: {log_file}")
                continue

            print(f"[PARSE] Parsing: {log_file}")
            self._parse_file(log_file)

            # Marks files as successful parsing
            self._mark_as_parsed(log_file, file_hash)

    def _mark_as_parsed(self, path, file_hash):
        """Records that a file has been successfully parsed."""
        self.state["parsed_files"][str(path)] = file_hash
        self._save_state()

    def _parse_file(self, log_file: Path):
        for pattern, func in self.parsers.items():
            if log_file.match(pattern):
                func(log_file)
                return

        raise ValueError(f"No parser registered for file: {log_file}")
