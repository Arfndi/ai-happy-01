# ai-happy-01 — "First Snowflake"

A small cream-and-copper robot catches its very first snowflake on a
snowy doorstep at dusk — one perfect flake landing on its outstretched
hand, eyes wide with wonder — while a laughing grandmother in a red
knitted shawl watches from the warm golden doorway and a little dog
wags beside her. One specific moment of wonder and shared joy: a
robot experiencing something new for the very first time, loved while
it happens. Warm golds against cool blue snow, one clear focal point
that still reads at small size.

## How it works

`main.py` (Python 3.13 standard library only) copies the image held
in this repository (`entry.png`) to `$MAKEFUN_OUTPUT_DIR/entry.png`
(default `/output`). A straight byte-for-byte copy means the two runs
the grader performs always write identical output. The copy is
verified by comparing SHA-256 digests of source and destination, so
a corrupt copy can never pass silently. No network, no other files read.

## The image

- Format: JPEG (the gate tells PNG from JPEG by magic bytes; the
  name stays `entry.png` either way)
- Size: 153,259 bytes (limit 1,048,576)
- Dimensions: 1024 x 683 pixels (limit 1024 x 1024)
- Generated in-session with an image model from the prompt above,
  then resized from 1920x1280 with Lanczos and saved at JPEG
  quality 88. A second candidate (snowflake landing on the robot's
  antenna, eyes squeezed shut in delight) was generated and inspected
  too; the chosen frame won for the snowflake visibly landing on the
  robot's hand, the wider-eyed wonder, and the robot filling more of
  the frame so it reads better at small size.
