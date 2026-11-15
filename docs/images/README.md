# AlarmV1 UI previews

## Source and fidelity

- Source: [`clock.yaml` at `6a3e0df44246fb215c65ae22a25bbdee5bf0980c`](https://github.com/gurgendav/esp-alarm-clock/blob/6a3e0df44246fb215c65ae22a25bbdee5bf0980c/clock.yaml).
- Font files, font sizes, static colors, widget dimensions and center offsets
  come from that committed configuration. Dynamic clock/away colors and labels
  follow `update_alarm_status_ui`; media labels follow `update_media_screen_ui`.
- Rendering uses Pillow, **not the production LVGL renderer**. Font baselines,
  antialiasing, borders, line caps and progress-bar details may differ on-device.
  The previews do not simulate animation, touch, a volume overlay or state changes.
- Each output is 240 × 240 RGBA with transparent corners and a circular mask.
- `clock-preview.png`: example time 06:30, recurring alarm at 07:00. `ON`
  illustrates the externally confirmed readiness state, not an assertion about
  any real installation.
- `away-preview.png`: the same example time with alarms disabled.
- `media-preview.png`: generic example title/artist and illustrative progress,
  with the actual stop/pause/next dock geometry.
- No device capture, private photo, location, Wi-Fi information, Home Assistant
  address, actual listening history or image metadata is used.

The original public `clock.webp` in the repository is a hardware/enclosure photo
of the **earlier analogue interface**; it is not a digital AlarmV1 screenshot.

## Reproduce

From the repository root, with the digital source commit available locally:

```sh
git fetch origin wip/alarm-clock
python -m pip install Pillow PyYAML
python docs/images/render_previews.py
```

The script reads the exact committed YAML and fonts with `git show`; it does not
read local credentials, call Home Assistant, contact the device or change firmware.
The source revision is pinned so a later branch update does not silently change
these illustrations. Review them alongside a new source revision before updating.

Hanken Grotesk is provided under its [OFL font license](https://github.com/gurgendav/esp-alarm-clock/blob/6a3e0df44246fb215c65ae22a25bbdee5bf0980c/assets/HankenGrotesk-OFL.txt).
DejaVu Sans is the existing repository media font; see [DejaVu font licensing](https://dejavu-fonts.github.io/License.html).

[Back to AlarmV1](../../readme.md)
