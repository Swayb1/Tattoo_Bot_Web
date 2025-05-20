import os
from flask import Flask, render_template, send_from_directory, jsonify
from flask import Flask, render_template, request, jsonify, send_from_directory, url_for


app = Flask(__name__)

# Define style data manually
style_data = {
    "American_Traditional": {
        "image": "images/American_Traditional.jpg",
        "description": "Bold lines and bright colors rooted in sailor tattoo culture.",
        "audio": "audio/American_Traditional/description.mp3"
    },
    "Tribal": {
        "image": "images/Tribal.jpg",
        "description": "Geometric designs from indigenous cultures around the world.",
        "audio": "audio/Tribal/description.mp3"
    },
    "Neo_Traditional": {
        "image": "images/Neo_Traditional.jpg",
        "description": "Colores intensos, sombreado detallado y versiones modernas de los motivos clásicos del estilo tradicional americano.",
        "audio": "audio/Neo_Traditional/description.mp3"
    },
    "Japanese": {
        "image": "images/Japanese.jpg",
        "description": "Traditional motifs like koi fish, dragons, and samurai with bold outlines and flowing composition.",
        "audio": "audio/Japanese/description.mp3"
    },
    "Realism": {
        "image": "images/Realism.jpg",
        "description": "Highly detailed tattoos resembling real-life portraits, nature, or objects with photo-like precision.",
        "audio": "audio/Realism/description.mp3"
    },
    "Watercolor": {
        "image": "images/Watercolor.jpg",
        "description": "Uses soft gradients, splashes, and brushstroke effects to mimic watercolor painting techniques.",
        "audio": "audio/Watercolor/description.mp3"
    },
    "Geometric": {
        "image": "images/Geometric.jpg",
        "description": "Focuses on symmetry, shapes, and patterns often with clean lines and mathematical precision.",
        "audio": "audio/Geometric/description.mp3"
    },
    "Minimalist": {
        "image": "images/Minimalist.jpg",
        "description": "Clean, simple designs with minimal detail, often using fine lines and subtle elements.",
        "audio": "audio/Minimalist/description.mp3"
    },
    "Blackwork": {
        "image": "images/Blackwork.jpg",
        "description": "Blackwork uses solid black ink to create bold designs, ranging from abstract geometry to dark illustrative art.",
        "audio": "audio/Blackwork/description.mp3"
    },
    "Trash_Polka": {
        "image": "images/Trash_Polka.jpg",
        "description": "Trash Polka combines photorealism with abstract elements, bold black strokes, and splashes of red for a chaotic, collage-like effect.",
        "audio": "audio/Trash_Polka/description.mp3"
    }
}

@app.route('/')
def home():
    return render_template('index.html', styles=style_data)

@app.route('/play_audio/<style>')
def play_audio(style):
    if style in style_data:
        audio_path = style_data[style]['audio']
        # Get only relative path from 'static'
        rel_path = os.path.relpath(audio_path, 'C:/Users/swayb1/Desktop/tattooey_bot/static')
        return send_from_directory('static', rel_path)
    return "Audio not found", 404

@app.route('/style/<style_name>')
def show_style(style_name):
    image_dir = os.path.join('static', 'images', style_name)
    if not os.path.exists(image_dir):
        return f"No images found for style: {style_name}", 404
    images = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png')) and f != 'thumb.jpg']
    return render_template('style.html', style_name=style_name, images=images)

@app.route('/static/images/<style_name>/<filename>')
def serve_image(style_name, filename):
    return send_from_directory(f'static/images/{style_name}', filename)

if __name__ == '__main__':
    app.run(debug=True)
