"""Record the narration lines with Kokoro (af_heart, speed 1.00) and log real lengths."""
import json, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro
from config import VOICE, VOICE_SPEED

LINES = [
    "One second. Ten metres up.",
    "Flip gravity for one second.",
    "You fall up nearly five metres, gaining speed.",
    "Gravity returns. You still coast to nearly ten.",
    "You drop back at about fifty kilometres an hour.",
    "The safer spot?",
    "Indoors. The ceiling stops you early.",
]

k = Kokoro("models/kokoro-v1.0.onnx", "models/voices-v1.0.bin")
out = []
for i, line in enumerate(LINES, 1):
    samples, sr = k.create(line, voice=VOICE, speed=VOICE_SPEED, lang="en-us")
    # trim leading/trailing silence
    a = np.abs(samples); idx = np.where(a > 0.01)[0]
    samples = samples[max(idx[0] - 240, 0): idx[-1] + 480]
    fn = f"vo/line{i}.wav"
    sf.write(fn, samples, sr)
    out.append({"i": i, "text": line, "file": fn, "dur": round(len(samples) / sr, 3), "sr": sr})
    print(i, out[-1]["dur"], line)
json.dump(out, open("vo/lines.json", "w"), indent=1)
print("total speech", round(sum(o["dur"] for o in out), 2))
