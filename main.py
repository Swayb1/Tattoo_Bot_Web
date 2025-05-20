import tkinter as tk
from tkinter import messagebox, Toplevel
import subprocess
from PIL import Image, ImageTk
import pyttsx3
import os
import sys
import pygame
import requests
from bs4 import BeautifulSoup
import urllib.parse
import tkinter as tk


class TattooBotGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TattooBot")
        self.geometry("700x500")
        self.configure(bg='black')
        self.engine = pyttsx3.init()
        self.selected_styles = []
        self.style_images = []
        self.style_audio = {
            "American_Traditional": [
                "audio/American_Traditional/description.mp3"
            ],
            "Tribal": [
                "audio/Tribal/description.mp3"
            ],
            "Neo-Traditional": [
                "audio/Neo_Traditional/description.mp3"
            ],
            "Japanese": [
                "audio/Japanese/description.mp3"
            ],
            "Realism": [
                "audio/Realism/description.mp3"
            ],
            "Watercolor": [
                "audio/Watercolor/description.mp3"
            ],
            "Geometric": [
                "audio/Geometric/description.mp3"
            ],
            "Minimalist": [
                "audio/Minimalist/description.mp3"
            ],
            "Blackwork": [
                "audio/Blackwork/description.mp3"
            ],
            "Trash_Polka": [
                "audio/Trash_Polka/description.mp3"
            ]
        }
        self.tattoo_styles = {
            "American_Traditional": {
                "image": "images/American_Traditional.jpg",
                "description": "Bold lines, limited colors, and iconic imagery like eagles, skulls, and roses."
            },
            "Tribal": {
                "image": "images/Tribal.jpg",
                "description": "Diseños en tinta negra con patrones geométricos y curvos arraigados en tradiciones indígenas."
            },
            "Neo_Traditional": {
                "image": "images/Neo_Traditional.jpg",
                "description": "Colores intensos, sombreado detallado y versiones modernas de los motivos clásicos del estilo tradicional americano."
            },
            "Japanese": {
                "image": "images/Japanese.jpg",
                "description": "Traditional motifs like koi fish, dragons, and samurai with bold outlines and flowing composition."
            },
            "Realism": {
                "image": "images/Realism.jpg",
                "description": "Highly detailed tattoos resembling real-life portraits, nature, or objects with photo-like precision."
            },
            "Watercolor": {
                "image": "images/Watercolor.jpg",
                "description": "Uses soft gradients, splashes, and brushstroke effects to mimic watercolor painting techniques."
            },
            "Geometric": {
                "image": "images/Geometric.jpg",
                "description": "Focuses on symmetry, shapes, and patterns often with clean lines and mathematical precision."
            },
            "Minimalist": {
                "image": "images/Minimalist.jpg",
                "description": "Clean, simple designs with minimal detail, often using fine lines and subtle elements."
            },
            "Blackwork": {
                "image": "images/Blackwork.jpg",
                "description": "Blackwork uses solid black ink to create bold designs, ranging from abstract geometry to dark illustrative art."
            },
            "Trash_Polka": {
                "image": "images/Trash_Polka.jpg",
                "description": "Trash Polka combines photorealism with abstract elements, bold black strokes, and splashes of red for a chaotic, collage-like effect."
            }
        }
        pygame.mixer.init()
        self.create_widgets()
    def download_images(self, keyword, folder_path, max_images=5):
        search_url = f"https://www.bing.com/images/search?q={urllib.parse.quote(keyword + ' tattoo')}&form=HDRSC2"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        try:
            response = requests.get(search_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            img_tags = soup.find_all("img", {"src": True})
            count = 0
            for img in img_tags:
                img_url = img['src']
                if img_url.startswith('http'):
                    try:
                        img_data = requests.get(img_url).content
                        with open(os.path.join(folder_path, f"{keyword}_{count}.jpg"), 'wb') as f:
                            f.write(img_data)
                        count += 1
                        if count >= max_images:
                            break
                    except Exception:
                        continue
        except Exception as e:
            messagebox.showerror("Download Error", f"Failed to download images for {keyword}: {e}")
    def select_style(self, style, window):
        if style not in self.selected_styles:
            self.selected_styles.append(style)
            self.show_selected_styles()
        if style in self.style_audio:
            for audio in self.style_audio[style]:
                self.play_audio(audio)
            # Open corresponding folder
            folder_path = os.path.join("C:\\Users\\swayb1\\Desktop\\tattooey bot", style)
        if os.path.exists(folder_path):
            try:
                subprocess.Popen(f'explorer "{folder_path}"')
            except Exception as e:
                messagebox.showerror("Folder Error", f"Could not open folder for {style}: {e}")
        else:
            messagebox.showinfo("Info", f"{style} already selected.")
        window.destroy()
    def play_audio(self, file_path):
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                self.update()
        except Exception as e:
            messagebox.showerror("Audio Error", f"Could not play audio: {e}")
    def create_widgets(self):
        try:
            bg_image = Image.open(self.resource_path(r"C:\\Users\\swayb1\\Desktop\\tattooey bot\\tattoo_bot_bg.jpg"))
            bg_image = bg_image.resize((700, 500), Image.Resampling.LANCZOS)
            self.background_photo = ImageTk.PhotoImage(bg_image)
            background_label = tk.Label(self, image=self.background_photo)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load background image: {e}")
        self.chat_history = tk.Text(self, wrap=tk.WORD, bg='white', fg='black', state=tk.DISABLED)
        self.chat_history.place(x=10, y=370, width=680, height=80)
        self.user_input = tk.Entry(self, bg='white', fg='black')
        self.user_input.place(x=10, y=460, width=680)
        self.user_input.bind("<Return>", self.send_message)
        style_button = tk.Button(self, text="Styles", command=self.show_style_dropdown, bg=self.cget("bg"), fg='white', relief='flat')
        style_button.place(x=10, y=10)
        self.finalize_button = tk.Button(self, text="Finalize Tattoo", command=self.finalize_tattoo, bg='white', fg='black')
        self.finalize_button.place(x=550, y=450, width=130)
        self.portfolio_button = tk.Button(self, text="Portfolio", command=self.open_portfolio, bg='white', fg='black')
        self.portfolio_button.place(x=400, y=450, width=130)
        try:
            info_img = Image.open(self.resource_path(r"C:\\Users\\swayb1\\Desktop\\tattooey bot\\josue el hawaii plus number.jpg"))
            info_img = info_img.resize((120, 60), Image.Resampling.LANCZOS)
            self.info_photo = ImageTk.PhotoImage(info_img)
            info_label = tk.Label(self.chat_history, image=self.info_photo, bg='white')
            info_label.place(relx=0.5, rely=1.0, anchor='s', y=-5)
        except Exception as e:
            messagebox.showerror("Image Error", f"Could not load bottom info image: {e}")
    def open_portfolio(self):
        folder = r"C:\Users\swayb1\Desktop\tattooey bot\portfolio de hawaii"
        if os.path.exists(folder):
            try:
                subprocess.Popen(f'explorer "{folder}"')
            except Exception as e:
                messagebox.showerror("Error", f"Could not open portfolio folder: {e}")
        else:
            messagebox.showwarning("Not Found", "Portfolio folder does not exist.")
    def show_style_dropdown(self):
        dropdown = Toplevel(self)
        dropdown.title("Choose Tattoo Style")
        dropdown.geometry("350x500")
        dropdown.configure(bg='black')
        canvas = tk.Canvas(dropdown, bg='black')
        scrollbar = tk.Scrollbar(dropdown, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg='black')
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        for style, info in self.tattoo_styles.items():
            try:
                img = Image.open(self.resource_path(info["image"])).resize((100, 100), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.style_images.append(photo)
                img_label = tk.Label(scroll_frame, image=photo, bg='black')
                img_label.pack(pady=5)
                btn = tk.Button(scroll_frame, text=style, command=lambda s=style: self.select_style(s, dropdown), bg='white', fg='black')
                btn.pack(pady=2, fill=tk.X, padx=10)
                desc_label = tk.Label(scroll_frame, text=info["description"], wraplength=300, justify='left', bg='gray', fg='white')
                desc_label.pack(pady=5, padx=10)
            except Exception as e:
                messagebox.showerror("Error", f"Could not load style image for {style}: {e}")
    def show_selected_styles(self):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, f"Selected Styles: {', '.join(self.selected_styles)}\n")
        self.chat_history.config(state=tk.DISABLED)
    def finalize_tattoo(self):
        if not self.selected_styles:
            messagebox.showwarning("No Styles Selected", "Please select at least one tattoo style.")
        else:
            self.chat_history.config(state=tk.NORMAL)
            self.chat_history.insert(tk.END, f"Finalizing tattoo with styles: {', '.join(self.selected_styles)}\n")
            self.chat_history.config(state=tk.DISABLED)
            self.search_for_tattoo()
    def search_for_tattoo(self):
        for style in self.selected_styles:
            folder_path = os.path.join("C:\\Users\\swayb1\\Desktop\\tattooey bot", style)
            os.makedirs(folder_path, exist_ok=True)
            self.chat_history.config(state=tk.NORMAL)
            self.chat_history.insert(tk.END, f"Searching and downloading images for: {style}\n")
            self.chat_history.config(state=tk.DISABLED)
            self.download_images(style, folder_path)
            try:
                subprocess.Popen(f'explorer "{folder_path}"')
            except Exception as e:
                messagebox.showerror("Error", f"Could not open folder for {style}: {e}")
    def send_message(self, event=None):
        user_message = self.user_input.get().strip()
        if not user_message:
            return
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, f"You: {user_message}\n")
        self.chat_history.config(state=tk.DISABLED)
        self.user_input.delete(0, tk.END)
        # You can add a basic response here or call another function
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, f"TattooBot: Got it! We'll use this info.\n")
        self.chat_history.config(state=tk.DISABLED)
    def get_bot_response(self, message):
        return "This is a sample response. (Implement logic here)"
    def speak_text(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    app = TattooBotGUI()
    app.mainloop()
