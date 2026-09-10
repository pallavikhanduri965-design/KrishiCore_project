import { create } from 'zustand';
import { ChatMessage } from '../types/api.types';

interface ChatState {
    messages: ChatMessage[];
    addMessage: (msg: ChatMessage) => void;
    clearMessages: () => void;
}

export const useChatStore = create<ChatState>((set) => ({
    messages: [],
    addMessage: (msg) =>
        set((state) => ({ messages: [...state.messages, msg] })),
    clearMessages: () => set({ messages: [] }),
}));
