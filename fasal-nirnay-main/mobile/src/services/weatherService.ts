import api from './api';
import { WeatherData } from '../types/api.types';

export const weatherService = {
    getWeather: async (lat: number, lon: number): Promise<WeatherData> => {
        const { data } = await api.get<WeatherData>('/weather', {
            params: { lat, lon },
        });
        return data;
    },
};
