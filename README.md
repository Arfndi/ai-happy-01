# ai-happy-01 — "First Snowflake"

Entry for the make.fun **ai-happy-01** image bounty: a single happy image of
a small robot catching its very first snowflake.

## The image

`entry.png` is the entry itself: a JPEG, 1024x683, 153,259 bytes. It lives in
this repo and is copied verbatim to the output — the program never
regenerates or alters it, so the submitted image is always the same file.

## How main.py works

`main.py` is Python 3.13, standard library only. It:

1. Copies `entry.png` from the repo directory to `/output/entry.png`.
2. Verifies the copy's SHA-256 against the known digest
   `22e72766b3ac6f94ba784ffe3ae2a55c9d39fc82e608f4e8ca458951c590793b`
   and exits non-zero with a clear error on any mismatch.
3. Validates the output against the bounty limits: at most 1 MiB and at most
   1024x1024 pixels. The size is checked with `os.path.getsize`; the
   dimensions are parsed from the JPEG's SOF marker with `struct` (no PIL).
4. Runs a second verification pass: it re-reads `/output/entry.png` from
   disk and re-checks the hash, so a bad write cannot slip through.

The program is fully deterministic — running it twice produces byte-identical
output.

## How to run it

```sh
python3 main.py
```

That writes `/output/entry.png` and prints its dimensions, size and SHA-256.
Exit code 0 means the copy, the hash, the size/dimension limits and the
second verification pass all succeeded; any failure exits non-zero with an
error message on stderr.

## Files

- `main.py` — the entrypoint described above.
- `entry.png` — the entry image (do not modify; its hash is pinned).
- `LICENSE` — MIT.
- `.makefun/owner.json` — the entrant's payout wallet.
