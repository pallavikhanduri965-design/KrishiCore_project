import axios from 'axios';
import { Storage } from '../utils/storage';

const api = axios.create({
    baseURL: process.env.EXPO_PUBLIC_API_URL ?? 'http://localhost:8000',
    timeout: 15000,
    headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use((config) => {
    const lang = Storage.get('language') ?? 'hi';
    config.headers['Accept-Language'] = lang;
    return config;
});

api.interceptors.response.use(
    (res) => res,
    (err) => {
        if (!err.response) {
            return Promise.reject({ offline: true, message: 'No internet' });
        }
        return Promise.reject(err.response.data);
    }
);

export default api;
