import asyncio
import io
import os
import base64
from gtts import gTTS
from typing import Optional

class TTSService:
    def __init__(self):
        print("✅ TTS Service initialized (Browser-based audio)")
    
    async def generate_audio_base64(self, text: str, lang: str = 'id') -> Optional[str]:
        """Generate audio and return as base64 string for browser playback"""
        try:
            # Run TTS in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            audio_base64 = await loop.run_in_executor(None, self._generate_audio, text, lang)
            return audio_base64
        except Exception as e:
            print(f"TTS Error: {e}")
            return None
    
    def _generate_audio(self, text: str, lang: str = 'id') -> str:
        """Generate audio and return as base64"""
        try:
            # Generate TTS
            tts = gTTS(text=text, lang=lang)
            mp3_fp = io.BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            
            # Convert to base64
            audio_base64 = base64.b64encode(mp3_fp.read()).decode('utf-8')
            print(f"🔊 Audio generated: {text[:50]}...")
            return audio_base64
        except Exception as e:
            print(f"TTS generation error: {e}")
            raise e
    
    def create_announcement(self, patient_name: str, queue_number: int, poly: str) -> str:
        """Create announcement text"""
        return f"Nomor antrian {queue_number}, {patient_name}, silahkan ke {poly}"

# Global TTS service instance
tts_service = TTSService()