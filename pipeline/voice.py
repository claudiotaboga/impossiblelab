"""Record the 7 narration lines with Kokoro (af_heart, speed 1.10) and log real lengths."""
import json, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro

LINES = [
    "Whisky is thicker than water.",
    "Ride a bike into a lake of it,",
    "and you sink lower. It's lighter than water.",
    "But every pedal drags. Nearly three times thicker.",
    "Above twenty-six degrees, the air can ignite.",
    "The real casualty? Your chain.",
    "Alcohol strips the oil right off.",
]

k = Kokoro("models/kokoro-v1.0.onnx", "models/voices-v1.0.bin")
out = []
for i, line in enumerate(LINES, 1):
    samples, sr = k.create(line, voice="af_heart", speed=1.10, lang="en-us")
    # trim leading/trailing silence
    a = np.abs(samples); idx = np.where(a > 0.01)[0]
    samples = samples[max(idx[0] - 240, 0): idx[-1] + 480]
    fn = f"vo/line{i}.wav"
    sf.write(fn, samples, sr)
    out.append({"i": i, "text": line, "file": fn, "dur": round(len(samples) / sr, 3), "sr": sr})
    print(i, out[-1]["dur"], line)
json.dump(out, open("vo/lines.json", "w"), indent=1)
print("total speech", round(sum(o["dur"] for o in out), 2))
