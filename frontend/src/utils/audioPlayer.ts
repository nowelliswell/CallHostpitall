/**
 * Play audio from base64 string
 */
export const playAudioFromBase64 = (base64Audio: string): Promise<void> => {
  return new Promise((resolve, reject) => {
    try {
      // Create audio element
      const audio = new Audio(`data:audio/mp3;base64,${base64Audio}`);
      
      // Set volume
      audio.volume = 1.0;
      
      // Play audio
      audio.play()
        .then(() => {
          console.log('🔊 Audio playing...');
        })
        .catch((error) => {
          console.error('Audio play error:', error);
          reject(error);
        });
      
      // Resolve when audio ends
      audio.onended = () => {
        console.log('✅ Audio finished');
        resolve();
      };
      
      // Handle errors
      audio.onerror = (error) => {
        console.error('Audio error:', error);
        reject(error);
      };
    } catch (error) {
      console.error('Failed to create audio:', error);
      reject(error);
    }
  });
};

/**
 * Play announcement text using Web Speech API (fallback)
 */
export const speakText = (text: string, lang: string = 'id-ID'): Promise<void> => {
  return new Promise((resolve, reject) => {
    if (!('speechSynthesis' in window)) {
      console.warn('Speech Synthesis not supported');
      reject(new Error('Speech Synthesis not supported'));
      return;
    }

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = lang;
    utterance.rate = 0.9;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;

    utterance.onend = () => {
      console.log('✅ Speech finished');
      resolve();
    };

    utterance.onerror = (error) => {
      console.error('Speech error:', error);
      reject(error);
    };

    window.speechSynthesis.speak(utterance);
  });
};