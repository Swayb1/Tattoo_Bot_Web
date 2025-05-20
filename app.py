from flask import Flask, render_template, request, url_for, send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'

# Tattoo styles dictionary
tattoo_styles = {
    "American_Traditional": {
        "image": "images/American_Traditional/American_Traditional.jpg",
        "description": "Bold lines, limited colors...",
        "audio": "audio/American_Traditional/description.mp3"
    },
    "Tribal": {
        "image": "images/Tribal/Tribal.jpg",
        "description": "Diseños en tinta negra...",
        "audio": "audio/Tribal/description.mp3"
    },
    "Neo_Traditional": {
        "image": "images/Neo_Traditional/Neo_Traditional.jpg",
        "description": "Colores intensos, sombreado detallado y versiones modernas de los motivos clásicos del estilo tradicional americano.",
        "audio": "audio/Neo_Traditional/description.mp3"
    },
    "Japanese": {
        "image": "images/Japanese/Japanese.jpg",
        "description": "Traditional motifs like koi fish, dragons, and samurai with bold outlines and flowing composition.",
        "audio": "audio/Japanese/description.mp3"
    },
    "Realism": {
        "image": "images/Realism/Realism.jpg",
        "description": "Highly detailed tattoos resembling real-life portraits, nature, or objects with photo-like precision.",
        "audio": "audio/Realism/description.mp3"
    },
    "Watercolor": {
        "image": "images/Watercolor/Watercolor.jpg",
        "description": "Uses soft gradients, splashes, and brushstroke effects to mimic watercolor painting techniques.",
        "audio": "audio/Watercolor/description.mp3"
    },
    "Geometric": {
        "image": "images/Geometric/Geometric.jpg",
        "description": "Focuses on symmetry, shapes, and patterns often with clean lines and mathematical precision.",
        "audio": "audio/Geometric/description.mp3"
    },
    "Minimalist": {
        "image": "images/Minimalist/Minimalist.jpg",
        "description": "Clean, simple designs with minimal detail, often using fine lines and subtle elements.",
        "audio": "audio/Minimalist/description.mp3"
    },
    "Blackwork": {
        "image": "images/Blackwork/Blackwork.jpg",
        "description": "Blackwork uses solid black ink to create bold designs, ranging from abstract geometry to dark illustrative art.",
        "audio": "audio/Blackwork/description.mp3"
    },
    "Trash_Polka": {
        "image": "images/Trash_Polka/Trash_Polka.jpg",
        "description": "Trash Polka combines photorealism with abstract elements, bold black strokes, and splashes of red for a chaotic, collage-like effect.",
        "audio": "audio/Trash_Polka/description.mp3"
    }
}

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Styles grid page
@app.route('/styles')
def styles():
    return render_template('styles.html', styles=tattoo_styles)

# Route to show images for selected style
@app.route('/style/<style_name>')
def show_style(style_name):
    image_dir = os.path.join('static', 'tattoo_styles', style_name)
    if not os.path.exists(image_dir):
        return f"No images found for style: {style_name}", 404
    images = os.listdir(image_dir)
    return render_template('style.html', style_name=style_name, images=images, styles=tattoo_styles)

@app.route('/play_audio/<style>')
def play_audio(style):
    if style in tattoo_styles:
        audio_path = tattoo_styles[style]['audio']
        directory = os.path.join(app.static_folder, os.path.dirname(audio_path))
        filename = os.path.basename(audio_path)
        return send_from_directory(directory, filename)
    return "Audio not found", 404

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0')
