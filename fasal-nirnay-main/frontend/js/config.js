/**
 * FasalNirnay AI - API Configuration
 */
const CONFIG = {
    // Dynamically detect API origin or fallback to localhost
    API_BASE_URL: window.location.origin.includes('localhost') || window.location.origin.includes('127.0.0.1')
        ? window.location.origin
        : 'http://127.0.0.1:8000',
    
    ENDPOINTS: {
        WEATHER: '/weather/forecast',
        NEWS: '/news/latest',
        CHAT: '/chat/query',
        STT: '/speech/stt',
        TTS: '/speech/tts',
        POOL: '/pool/',
        HEALTH: '/health',
    },
    
    DEFAULT_LOCATION: 'Mumbai, Maharashtra',
    DEFAULT_DISTRICT: 'Mumbai',
    DEFAULT_STATE: 'Maharashtra',
    DEFAULT_CROP: 'Wheat',
    
    LANGUAGE_CODES: {
        en: 'en-IN',
        hi: 'hi-IN',
        pa: 'pa-IN',
        mr: 'mr-IN'
    }
};

window.CONFIG = CONFIG;
