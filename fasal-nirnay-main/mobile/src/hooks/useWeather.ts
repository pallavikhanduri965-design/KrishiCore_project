import { useQuery } from '@tanstack/react-query';
import * as Location from 'expo-location';
import { weatherService } from '../services/weatherService';
import { useAppStore } from '../store/useAppStore';

export function useWeather() {
    const { location, setLocation } = useAppStore();

    const fetchLocation = async () => {
        if (location) return location;
        const { status } = await Location.requestForegroundPermissionsAsync();
        if (status !== 'granted') throw new Error('Location denied');
        const loc = await Location.getCurrentPositionAsync({});
        const [geo] = await Location.reverseGeocodeAsync(loc.coords);
        const newLoc = {
            lat: loc.coords.latitude,
            lon: loc.coords.longitude,
            district: geo.district ?? geo.city ?? 'Unknown',
            state: geo.region ?? 'Unknown',
        };
        setLocation(newLoc);
        return newLoc;
    };

    return useQuery({
        queryKey: ['weather', location?.lat, location?.lon],
        queryFn: async () => {
            const loc = await fetchLocation();
            return weatherService.getWeather(loc.lat, loc.lon);
        },
        staleTime: 30 * 60 * 1000,
        retry: 2,
    });
}
