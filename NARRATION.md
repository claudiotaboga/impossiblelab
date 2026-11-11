# Narration standard (from episode 02)

Pacing lives in `pipeline/config.py`: 15 s reel, Kokoro `af_heart` at speed 1.10 (E4 from TIL-05; TIL-02..04 were 16.5 s at 1.00), 0.20 s pauses, last ~1 s reserved for THE REAL SCIENCE card. `timeline.py` refuses to build if the narration overruns.

## Budget
- Speaking rate: about **3.4 words per second** at speed 1.00, about **3.7** at 1.10.
- Room for speech: about **12.5 s** at 15 s (14 s at 16.5 s), so **40–46 words total**, in **6–7 lines**.
- Every extra word costs clarity elsewhere. Cut before you add.

## Structure (one idea per line)
1. **Hook (≤ 6 words):** a claim that sounds wrong but is true. "Whisky is thicker than water."
2. **Premise:** the impossible situation, concretely. "Ride a bike into a lake of it."
3. **Beat 1, what you'd notice first,** with the reason. "You'd sit lower, because whisky is lighter than water."
4. **Beat 2, the surprise,** with one number. "Yet it's nearly three times thicker. Every pedal drags."
5. **Beat 3, the danger or escalation.** "On a hot day, the air above it can catch fire."
6. **Twist setup (≤ 4 words).** "The real casualty?"
7. **Twist payoff:** short, concrete, slightly funny. "Your chain. Alcohol strips the oil."

## Rules for better narration
- **Say why, not just what.** "You sink lower *because* it's lighter than water" beats "You sink lower. It's lighter."
- **One number per beat, rounded and spoken naturally:** "nearly three times", "about twenty-six degrees". Never a decimal in the voiceover; precise values go on THE REAL SCIENCE card.
- **Plain words.** "Thicker", not "more viscous"; "catch fire", not "ignite".
- **Every number must be checkable** and match the card. Qualify estimates ("about", "nearly").
- **Read it aloud once.** If a line needs a breath in the middle, split it.
