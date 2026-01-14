import subprocess
from datetime import datetime, timezone
from pathlib import Path

PACKAGE_NAME = "lcedfd"


def initialize(root, version, build_data):
    out = root / "src" / PACKAGE_NAME

    def _git(cmd):
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout.strip()

    def _format(name, value, newline=True):
        return f"{name} = {value!r}" + "\n" if newline else ""

    with open(out / "_version.py", "w") as file:
        file.write(
            _format(
                "COMP_DATE", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            )
        )
        file.write(_format("GIT_HASH", _git(["git", "rev-parse", "--short", "HEAD"])))
        file.write(
            _format(
                "VERSION", _git(["git", "describe", "--tags", "--dirty", "--always"])
            )
        )
