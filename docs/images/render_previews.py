#!/usr/bin/env python3
"""Render illustrative README previews, NOT device/LVGL screenshots.

Requires Pillow and PyYAML, and the source commit in this repository's Git
object database. Reads only committed source/fonts, never a live device.
"""
import io
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFont
import yaml

SOURCE = "6a3e0df44246fb215c65ae22a25bbdee5bf0980c"
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SCALE = 3


def committed(path):
    return subprocess.check_output(["git", "show", f"{SOURCE}:{path}"], cwd=ROOT)


class Loader(yaml.SafeLoader):
    pass


Loader.add_multi_constructor("!", lambda loader, tag, node: loader.construct_scalar(node))
config = yaml.load(committed("clock.yaml"), Loader=Loader)
widgets = {}


def index(value):
    if isinstance(value, dict):
        if "id" in value and isinstance(value["id"], str):
            widgets[value["id"]] = value
        for child in value.values():
            index(child)
    elif isinstance(value, list):
        for child in value:
            index(child)


index(config["lvgl"])
fonts = {
    f["id"]: ImageFont.truetype(io.BytesIO(committed(f["file"])), f["size"] * SCALE)
    for f in config["font"]
}


def color(value):
    if isinstance(value, int):
        return f"#{value:06x}"
    return value


class Preview:
    def __init__(self, background="black"):
        self.image = Image.new("RGBA", (240 * SCALE, 240 * SCALE), background)
        self.draw = ImageDraw.Draw(self.image)

    def box(self, ident, fill=None, outline=None, center=(120, 120)):
        w = widgets[ident]
        cx, cy = center[0] + w.get("x", 0), center[1] + w.get("y", 0)
        width, height = w["width"], w["height"]
        rect = tuple(round(n * SCALE) for n in
                     (cx - width / 2, cy - height / 2, cx + width / 2, cy + height / 2))
        self.draw.rounded_rectangle(
            rect, radius=w.get("radius", 0) * SCALE,
            fill=color(fill if fill is not None else w.get("bg_color", "black")),
            outline=color(outline) if outline is not None else None,
            width=max(1, w.get("border_width", 0) * SCALE))

    def text(self, ident, text, fill=None, center=(120, 120)):
        w = widgets[ident]
        self.draw.text(((center[0] + w.get("x", 0)) * SCALE,
                        (center[1] + w.get("y", 0)) * SCALE), text,
                       font=fonts[w["text_font"]], anchor="mm",
                       fill=color(fill if fill is not None else w["text_color"]))

    def save(self, name):
        mask = Image.new("L", self.image.size)
        ImageDraw.Draw(mask).ellipse((0, 0, 240 * SCALE - 1, 240 * SCALE - 1), fill=255)
        self.image.putalpha(mask)
        self.image.resize((240, 240), Image.Resampling.LANCZOS).save(OUT / name)


# Example values only. Dynamic colors/text follow update_alarm_status_ui.
clock = Preview()
clock.text("clock_time_label", "06:30")
clock.box("clock_divider")
clock.box("clock_status_pill", 0x17351F)
clock.text("clock_status_pill_label", "ON", 0xB8F5C1, (120, 136))
clock.text("clock_next_label", "Ring in 30m")
clock.text("clock_countdown_label", "Today 07:00")
clock.save("clock-preview.png")

away = Preview("#003e44")
away.text("clock_time_label", "06:30", 0xF4FFFF)
away.box("clock_divider", 0x8DECF2)
away.box("clock_status_pill", 0xB6F7FF)
away.text("clock_status_pill_label", "AWAY", "black", (120, 136))
away.text("clock_next_label", "Away Mode Active", 0xF4FFFF)
away.box("clock_resume_button", "#003e44", 0x4DD9E4)
away.text("clock_resume_label", "TAP TO RESUME", center=(120, 204))
away.save("away-preview.png")

media = Preview()
media.text("media_status_label", "NOW PLAYING")
media.text("media_title_label", "Example track")
media.text("media_artist_label", "Example artist")
media.box("media_progress_bar")
media.draw.rounded_rectangle((32 * SCALE, 130 * SCALE, 100 * SCALE, 134 * SCALE),
                             radius=2 * SCALE, fill="#4dd9e4")
media.box("media_control_dock")
media.box("media_play_pause_button", center=(120, 184))
media.box("media_stop_icon", center=(66, 184))
media.box("media_pause_bar_left", center=(120, 184))
media.box("media_pause_bar_right", center=(120, 184))
for ident in ("media_next_chevron_left", "media_next_chevron_right"):
    w = widgets[ident]
    points = [tuple(int(n) for n in p.split(",")) for p in w["points"]]
    points = [((159 + x) * SCALE, (173 + y) * SCALE) for x, y in points]
    media.draw.line(points, fill=color(w["line_color"]), width=w["line_width"] * SCALE,
                    joint="curve")
    for x, y in points:
        r = 2 * SCALE
        media.draw.ellipse((x-r, y-r, x+r, y+r), fill=color(w["line_color"]))
media.box("media_next_bar", center=(174, 184))
media.save("media-preview.png")
print(f"Rendered 3 illustrative previews from {SOURCE}; no device contacted.")
