import api from './api';
import { NewsArticle } from '../types/api.types';

export const newsService = {
    getNews: async (language: string, category?: string): Promise<NewsArticle[]> => {
        const { data } = await api.get<NewsArticle[]>('/news', {
            params: { language, category },
        });
        return data;
    },
};
