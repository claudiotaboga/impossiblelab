import os, time, overlay
N = 360
for f in range(N):
    nxt = f"frames/{f+1:04d}.png"
    while not (os.path.exists(nxt) or (f == N - 1 and os.path.exists(f"frames/{f:04d}.png") and time.sleep(5) is None)):
        time.sleep(3)
    if not os.path.exists(f"comp/{f:04d}.png"):
        overlay.frame(f).save(f"comp/{f:04d}.png", compress_level=1)
print("OVERLAY_DONE")
