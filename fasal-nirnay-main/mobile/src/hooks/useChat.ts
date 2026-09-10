import { useState, useCallback } from 'react';
import { chatService } from '../services/chatService';
import { speechService } from '../services/speechService';
import { useChatStore } from '../store/useChatStore';
import { useAppStore } from '../store/useAppStore';
import { ChatMessage } from '../types/api.types';

export function useChat() {
    const [isLoading, setIsLoading] = useState(false);
    const { messages, addMessage, clearMessages } = useChatStore();
    const { language, selectedCrop } = useAppStore();

    const send = useCallback(async (text: string) => {
        if (!text.trim() || isLoading) return;

        const userMsg: ChatMessage = { role: 'user', content: text, timestamp: Date.now() };
        addMessage(userMsg);
        setIsLoading(true);

        try {
            const res = await chatService.sendMessage({
                message: text,
                language,
                crop: selectedCrop,
                history: messages.slice(-6),
            });
            const botMsg: ChatMessage = { role: 'assistant', content: res.reply, timestamp: Date.now() };
            addMessage(botMsg);
            speechService.speak(res.reply, language);
        } catch (err: any) {
            addMessage({
                role: 'assistant',
                content: err?.offline
                    ? 'इंटरनेट नहीं है। बाद में कोशिश करें।'
                    : 'कुछ गलत हो गया। फिर कोशिश करें।',
                timestamp: Date.now(),
            });
        } finally {
            setIsLoading(false);
        }
    }, [messages, language, selectedCrop, isLoading]);

    return { messages, isLoading, send, clearMessages };
}
