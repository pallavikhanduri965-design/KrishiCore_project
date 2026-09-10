export const formatPrice = (price: number): string =>
    `₹ ${price.toLocaleString('en-IN')}`;

export const formatDate = (iso: string): string => {
    const d = new Date(iso);
    return d.toLocaleDateString('hi-IN', { day: 'numeric', month: 'short' });
};

export const timeAgo = (iso: string): string => {
    const diff = Date.now() - new Date(iso).getTime();
    const mins = Math.floor(diff / 60000);
    if (mins < 60) return `${mins} मिनट पहले`;
    const hrs = Math.floor(mins / 60);
    if (hrs < 24) return `${hrs} घंटे पहले`;
    return `${Math.floor(hrs / 24)} दिन पहले`;
};

export const weatherIcon = (condition: string): string => {
    const map: Record<string, string> = {
        sunny: '☀️', clear: '☀️', cloudy: '☁️',
        rainy: '🌧️', rain: '🌧️', storm: '⛈️',
        fog: '🌫️', windy: '💨', snow: '❄️',
    };
    return map[condition?.toLowerCase()] ?? '🌤️';
};
