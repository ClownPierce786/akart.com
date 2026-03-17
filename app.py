import os
import base64
from flask import Flask, render_template

app = Flask(__name__)

IMAGE_FOLDER = os.path.join("static", "images")


def encode_images():
    images = []
    seen = set()

    if not os.path.exists(IMAGE_FOLDER):
        return images

    for file in sorted(os.listdir(IMAGE_FOLDER), key=str.lower):

        if file.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            name = file.lower()

            if name in seen:
                continue
            seen.add(name)

            path = os.path.join(IMAGE_FOLDER, file)

            with open(path, "rb") as img:
                encoded = base64.b64encode(img.read()).decode("utf-8")

            ext = file.split(".")[-1].lower()
            if ext == "jpg":
                ext = "jpeg"

            images.append({
                "data": encoded,
                "type": ext,
                "alt": f"AK ART creation {len(images) + 1}",
            })

    return images


@app.route("/")
def home():
    images = encode_images()
    return render_template("index.html", images=images)


if __name__ == "__main__":
    app.run(debug=True)
