import * as Speech from 'expo-speech';
import api from './api';

const LANG_MAP = { hi: 'hi-IN', pa: 'pa-IN', en: 'en-IN' };

export const speechService = {
    speak: (text: string, language: 'hi' | 'pa' | 'en') => {
        Speech.speak(text, {
            language: LANG_MAP[language],
            rate: 0.85,
            pitch: 1.0,
        });
    },

    stop: () => Speech.stop(),

    transcribeAudio: async (audioUri: string, language: string): Promise<string> => {
        const formData = new FormData();
        formData.append('audio', {
            uri: audioUri,
            type: 'audio/m4a',
            name: 'voice.m4a',
        } as any);
        formData.append('language', language);

        const { data } = await api.post<{ text: string }>('/speech', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });
        return data.text;
    },
};
