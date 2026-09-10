import api from './api';
import { PricePrediction, GradePrediction } from '../types/api.types';

export interface PriceRequest {
    commodity: string;
    variety: string;
    state: string;
    district: string;
    price_history: number[];
}

export const marketService = {
    predictPrice: async (payload: PriceRequest): Promise<PricePrediction> => {
        const { data } = await api.post<PricePrediction>('/predict/price', payload);
        return data;
    },

    predictGrade: async (payload: PriceRequest): Promise<GradePrediction> => {
        const { data } = await api.post<GradePrediction>('/predict/grade', payload);
        return data;
    },
};
