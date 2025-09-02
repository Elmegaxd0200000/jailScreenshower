from flask import Flask, jsonify
import mss
from PIL import Image

app = Flask(__name__)

def rgb_to_hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def get_screen_pixels(width=80, height=45):
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # captura pantalla principal
        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", (screenshot.width, screenshot.height), screenshot.rgb)
        img = img.resize((width, height))
        pixels = list(img.getdata())
        # Convertimos a hex
        return [[rgb_to_hex(*pixels[i*width + j]) for j in range(width)] for i in range(height)]

@app.route("/screen")
def screen():
    pixels = get_screen_pixels()
    return jsonify(pixels)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
