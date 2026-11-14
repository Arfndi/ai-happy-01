#!/usr/bin/env python3
"""ai-happy-01 — "First Snowflake" entrypoint.

Copies the repo-held entry image to /output/entry.png and verifies the copy
byte-for-byte against its known SHA-256. Deterministic: running it twice
produces identical output.

Usage:
    python3 main.py            # writes /output/entry.png
"""

import hashlib
import os
import shutil
import struct
import sys

EXPECTED_SHA256 = "22e72766b3ac6f94ba784ffe3ae2a55c9d39fc82e608f4e8ca458951c590793b"
SOURCE_NAME = "entry.png"
OUTPUT_DIR = "/output"
OUTPUT_NAME = "entry.png"
MAX_BYTES = 1024 * 1024
MAX_DIMENSION = 1024

# JPEG segment markers that carry a Start Of Frame (dimensions) block.
SOF_MARKERS = {
    0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
    0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
}


def jpeg_dimensions(path):
    """Return (width, height) of a JPEG by parsing its SOF marker.

    Pure stdlib: walks the segment table with struct, no PIL needed.
    Raises ValueError if no SOF marker is found.
    """
    with open(path, "rb") as handle:
        data = handle.read()
    if data[:2] != b"\xff\xd8":
        raise ValueError("not a JPEG (missing SOI marker)")
    pos = 2
    while pos + 1 < len(data):
        if data[pos] != 0xFF:
            raise ValueError("corrupt JPEG segment table")
        marker = data[pos + 1]
        if marker == 0xD8 or marker == 0x01 or 0xD0 <= marker <= 0xD7:
            pos += 2
            continue
        if pos + 4 > len(data):
            raise ValueError("truncated JPEG segment header")
        length = struct.unpack(">H", data[pos + 2:pos + 4])[0]
        if marker in SOF_MARKERS:
            if pos + 9 > len(data):
                raise ValueError("truncated SOF segment")
            height, width = struct.unpack(">HH", data[pos + 5:pos + 9])
            return width, height
        pos += 2 + length
    raise ValueError("no SOF marker found in JPEG")


def validate_output(path):
    """Check the written output against the bounty limits.

    Size must be <= 1 MiB and dimensions <= 1024x1024. Returns the
    (width, height) pair on success; raises ValueError otherwise.
    """
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise ValueError(
            f"output too large: {size} bytes (limit {MAX_BYTES})"
        )
    width, height = jpeg_dimensions(path)
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        raise ValueError(
            f"output too large: {width}x{height} "
            f"(limit {MAX_DIMENSION}x{MAX_DIMENSION})"
        )
    return width, height


def sha256_of(path):
    """Return the hex SHA-256 digest of the file at *path*."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(repo_dir, SOURCE_NAME)
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_NAME)

    if not os.path.isfile(source):
        print(f"error: source image not found: {source}", file=sys.stderr)
        return 1

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    shutil.copyfile(source, output_path)

    actual = sha256_of(output_path)
    if actual != EXPECTED_SHA256:
        print(
            f"error: SHA-256 mismatch for {output_path}\n"
            f"  expected: {EXPECTED_SHA256}\n"
            f"  actual:   {actual}",
            file=sys.stderr,
        )
        return 1

    try:
        width, height = validate_output(output_path)
    except ValueError as exc:
        print(f"error: output validation failed: {exc}", file=sys.stderr)
        return 1

    # Second verification pass: re-read the finished output from disk and
    # confirm the hash again, so a bad write cannot slip through.
    recheck = sha256_of(output_path)
    if recheck != EXPECTED_SHA256:
        print(
            f"error: second verification failed for {output_path}\n"
            f"  expected: {EXPECTED_SHA256}\n"
            f"  actual:   {recheck}",
            file=sys.stderr,
        )
        return 1

    print(
        f"wrote {output_path} ({width}x{height}, "
        f"{os.path.getsize(output_path)} bytes, sha256 {actual})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
