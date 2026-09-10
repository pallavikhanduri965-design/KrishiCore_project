import { useState, useRef } from 'react';
import { Audio } from 'expo-av';
import { speechService } from '../services/speechService';

export function useVoice(language: 'hi' | 'pa' | 'en') {
    const [isRecording, setIsRecording] = useState(false);
    const [isTranscribing, setIsTranscribing] = useState(false);
    const recordingRef = useRef<Audio.Recording | null>(null);

    const startRecording = async () => {
        try {
            await Audio.requestPermissionsAsync();
            await Audio.setAudioModeAsync({ allowsRecordingIOS: true, playsInSilentModeIOS: true });
            const { recording } = await Audio.Recording.createAsync(
                Audio.RecordingOptionsPresets.HIGH_QUALITY
            );
            recordingRef.current = recording;
            setIsRecording(true);
        } catch (e) {
            console.error('Start recording failed:', e);
        }
    };

    const stopRecording = async (): Promise<string> => {
        if (!recordingRef.current) return '';
        setIsRecording(false);
        await recordingRef.current.stopAndUnloadAsync();
        const uri = recordingRef.current.getURI() ?? '';
        recordingRef.current = null;

        if (!uri) return '';
        setIsTranscribing(true);
        try {
            return await speechService.transcribeAudio(uri, language);
        } catch {
            return '';
        } finally {
            setIsTranscribing(false);
        }
    };

    return { isRecording, isTranscribing, startRecording, stopRecording };
}
