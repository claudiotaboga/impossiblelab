"""House standard for every episode from #02 on. Change pacing here, not in the individual scripts."""
DUR = 16.5          # seconds; +10% vs episode 01 (15.0)
FPS = 24
FRAMES = int(DUR * FPS)   # 396

VOICE = "af_heart"
VOICE_SPEED = 1.00  # Kokoro speed; ep. 01 used 1.10 (lower = slower)

START = 0.20        # silence before the first line
GAP = 0.20          # pause between lines (ep. 01: 0.10)
CARD_MIN = 1.0      # seconds reserved at the end for THE REAL SCIENCE card

# Budget check: speech + pauses must leave room for the end card.
MAX_SPEECH = DUR - CARD_MIN - START  # minus GAP * (lines - 1), checked in timeline.py
