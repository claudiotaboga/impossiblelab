"""House standard for every episode from #02 on. Change pacing here, not in the individual scripts."""
DUR = 15.0          # seconds; E4 (11 Nov 2026, approved by Claudio): back to 15 s + speed 1.10 to test hold vs 16.5 s / 1.00
FPS = 24
FRAMES = int(DUR * FPS)   # 360 at 15 s

VOICE = "af_heart"
VOICE_SPEED = 1.10  # Kokoro speed; 16.5 s reels (TIL-02..04) used 1.00

START = 0.20        # silence before the first line
GAP = 0.20          # pause between lines (ep. 01: 0.10)
CARD_MIN = 1.0      # seconds reserved at the end for THE REAL SCIENCE card

# Budget check: speech + pauses must leave room for the end card.
MAX_SPEECH = DUR - CARD_MIN - START  # minus GAP * (lines - 1), checked in timeline.py
