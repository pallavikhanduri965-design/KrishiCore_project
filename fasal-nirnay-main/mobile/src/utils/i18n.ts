import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import hi from '../locales/hi.json';
import pa from '../locales/pa.json';
import en from '../locales/en.json';
import { Storage } from './storage';

i18n.use(initReactI18next).init({
    compatibilityJSON: 'v3',
    lng: Storage.get('language') ?? 'hi',
    fallbackLng: 'hi',
    resources: { hi: { translation: hi }, pa: { translation: pa }, en: { translation: en } },
    interpolation: { escapeValue: false },
});

export default i18n;
export const t = (key: string, opts?: object) => i18n.t(key, opts);
