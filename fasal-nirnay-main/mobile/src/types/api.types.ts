export interface WeatherData {
    temperature: number;
    feels_like: number;
    humidity: number;
    condition: string;
    rain_probability: number;
    wind_speed: number;
    location: string;
    advice: string;
}

export interface ChatMessage {
    role: 'user' | 'assistant';
    content: string;
    timestamp?: number;
}

export interface ChatRequest {
    message: string;
    language: 'hi' | 'pa' | 'en';
    crop?: string;
    history?: ChatMessage[];
}

export interface ChatResponse {
    reply: string;
    suggestions?: string[];
}

export interface NewsArticle {
    id: string;
    title: string;
    summary: string;
    source: string;
    category: 'scheme' | 'weather' | 'market' | 'pest' | 'general';
    published_at: string;
    url: string;
    thumbnail?: string;
}

export interface PricePrediction {
    predicted_price: number;
    recommendation: 'SELL' | 'HOLD';
    confidence?: number;
}

export interface GradePrediction {
    predicted_grade: string;
    confidence: number;
    all_probabilities: Record<string, number>;
}
