import { useState } from 'react';
import { Language } from '../types/app.types';

export function useLanguage() {
  const [language, setLanguage] = useState<Language>('hi');

  const changeLanguage = (lang: Language) => {
    setLanguage(lang);
  };

  return {
    language,
    changeLanguage,
  };
}
