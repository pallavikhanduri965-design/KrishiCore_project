import api from './api';
import { ChatRequest, ChatResponse } from '../types/api.types';

export const chatService = {
    sendMessage: async (payload: ChatRequest): Promise<ChatResponse> => {
        const { data } = await api.post<ChatResponse>('/chat', payload);
        return data;
    },
};
