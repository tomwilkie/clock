# Analogue Bedside Clock

This project builds an analogue bedside clock out of a M5Stack Dial; the main purpose is to be able to set the time for an alarm routing in Home Assistant by twisting the dial.

I have the alarm routine in Home Assistant slow fade up my bedsite lights, open the shutters, put on the air purifier and start the robot vacuum cleaners in the house.

Tip: if you use adaptive lighting, you can also set that up to control the backlight so its not too bright at night!

<img src="clock.webp" width="600" alt="Analogue Bedside Clock">

You'll need:
- An M5Stack Dial: https://docs.m5stack.com/en/core/M5Dial
- Some 3D printed parts: https://www.printables.com/model/1562621-analogue-alarm-clock-for-home-assistant
- A low profile USB C cable: https://www.amazon.co.uk/dp/B0FMPVZJDP

# Installing esphome & compiling this project on a Mac
```sh
# We'll use pipx to install esphome, and brew to install pipx
$ brew install pipx libmagic cairo

# Install esphome in its own virtual env
$ pipx install esphome

# Add some dependencies to the virtual env
$ pipx runpip esphome install python-magic pillow==11.3.0 cairosvg

# Install the clock (first time - your device name will vary)
$ ~/.local/bin/esphome run --device=/dev/tty.usbmodem31301 clock.yaml

# Install the clock (subsequent times, via WiFi)
$ ~/.local/bin/esphome run clock.yaml
```

# Previewing the clock face
`face.yaml` holds the clock face. `clock.yaml` builds it for the M5Stack Dial, and `preview.yaml` builds the same face for your computer in a 240 x 240 window, using your computer's clock. Two seconds after it starts, the preview shows the alarm circle as a turn of the dial would.

```sh
# The preview needs SDL2
$ brew install sdl2

# Open the face in a window
$ ~/.local/bin/esphome run preview.yaml

# Or save screenshots of the face and the alarm circle as face.bmp and alarm.bmp, then exit
$ ~/.local/bin/esphome compile preview.yaml
$ CLOCK_PREVIEW_OUT=/tmp ./.esphome/build/clock-preview/.pioenvs/clock-preview/program
```
