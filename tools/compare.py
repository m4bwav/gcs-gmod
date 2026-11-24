"""Side-by-side sheet: each screenshot beside the reference photo from about the same viewpoint.
Usage: python tools/compare.py shots/<stamp> [lower]  -> shots/<stamp>/compare.jpg (compare_lower.jpg)"""
import sys
from PIL import Image, ImageDraw

PAIRS = {  # shot -> refs/photos file
    "west_balcony": "GCT_Main_Concourse.jpg",
    "east_balcony": "Grand_Central_main_concourse_facing_Apple_agr.jpg",
    "booth": "Grand_Central_Terminal_51214194734.jpg",
    "vault_up": "Grand_Central_Station_Flag_Ceiling.jpg",
    "floor_east": "GCT_east_windows.jpg",
    "stairs_west": "GCT_west_windows.jpg",
}
LOWER = {  # area 2, under the concourse
    "dining": "Grand_Central_Dining_Concourse_Info.jpg",
    "whisper": "Whispering_Gallery.jpg",
    "oyster": "Grand_Central_Oyster_Bar_Grand_Central_Station_NYC.jpg",
}
d, W, H = sys.argv[1], 640, 400
lower = sys.argv[2:] == ["lower"]
if lower:
    PAIRS = LOWER
sheet = Image.new("RGB", (W * 2, (H + 18) * len(PAIRS)))
draw = ImageDraw.Draw(sheet)
for i, (shot, ref) in enumerate(PAIRS.items()):
    for j, path in enumerate((f"{d}/{shot}.jpg", f"refs/photos/{ref}")):
        im = Image.open(path).convert("RGB")
        im.thumbnail((W, H))
        sheet.paste(im, (j * W, i * (H + 18)))
        draw.text((j * W + 4, i * (H + 18) + H + 3), path, fill="white")
out = f"{d}/compare_lower.jpg" if lower else f"{d}/compare.jpg"
sheet.save(out, quality=85)
print(out)
