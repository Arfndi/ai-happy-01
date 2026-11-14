"""ai-happy-01 entry: copy the repo-held image to the output directory.

The image is a whole JPEG (named entry.png, as the rules allow) of
1024x683 pixels. Copying the file byte for byte makes the two runs
the grader performs write identical output.
"""

import hashlib
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    src = HERE / "entry.png"
    dst = OUT / "entry.png"
    shutil.copyfile(src, dst)
    # Guard the byte-identical-output rule: the copy must be complete.
    # A size check alone can miss corruption, so verify the digest too.
    assert dst.stat().st_size == src.stat().st_size, "copy incomplete"
    assert _sha256(dst) == _sha256(src), "copy differs from source"
    print(f"wrote {dst} ({dst.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
