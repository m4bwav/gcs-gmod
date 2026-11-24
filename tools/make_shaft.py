"""Procedural sun-shaft texture for the end windows: in the photos the morning light falls
through the end windows as long dusty beams (refs/photos/GCT_Main_Concourse_3.jpg).
shaft.vtf (256x256): u runs across the beam (soft edges, streaks from the mullions),
v runs down the beam (bright at the window, fading toward the floor). Used additively.
Writes src/materials/gcs/shaft.vtf and a preview in shots/tex/. Needs pip srctools pillow numpy."""
import numpy as np
from PIL import Image
from srctools import vtf

N = 256
rng = np.random.default_rng(5)
u = np.linspace(0, 1, N)
edge = np.sin(np.pi * u) ** 3                                    # soft sides
streak = 0.75 + 0.25 * np.convolve(rng.random(N + 16), np.ones(17) / 17, "valid")[:N]
streak *= 0.8 + 0.2 * (np.abs(((u * 7) % 1) - 0.5) > 0.06)       # faint mullion gaps
v = np.linspace(0, 1, N)[:, None]
fade = (1 - v) ** 0.9 * np.clip((v - 0.15) * 4, 0, 1) ** 2                        # bright near the window
a = fade * (edge * streak)[None, :]
rgb = np.dstack([a * 255, a * 236, a * 196]).clip(0, 255).astype(np.uint8)
Image.fromarray(rgb).save("shots/tex/shaft.png")
tex = vtf.VTF(N, N, fmt=vtf.ImageFormats.RGB888)
tex.get().copy_from(np.dstack([rgb, np.full((N, N), 255, np.uint8)]).tobytes(), vtf.ImageFormats.RGBA8888)
tex.compute_mipmaps()
with open("src/materials/gcs/shaft.vtf", "wb") as f:
    tex.save(f)
print("wrote src/materials/gcs/shaft.vtf")
