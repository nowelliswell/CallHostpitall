from gtts import gTTS
import pygame
import io
import logging
from tkinter import messagebox

def speak(text):
    """Announce the patient using text-to-speech."""
    try:
        tts = gTTS(text=text, lang='id')
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        
        pygame.mixer.music.load(mp3_fp, 'mp3')
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        logging.error(f"Gagal memutar suara: {str(e)}")
        messagebox.showerror("Error", f"Gagal memutar suara: {str(e)}")