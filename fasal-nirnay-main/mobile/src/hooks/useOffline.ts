import { useState, useEffect } from 'react';
import NetInfo from '@react-native-community/netinfo';

export function useOffline(): boolean {
    const [isOffline, setIsOffline] = useState(false);

    useEffect(() => {
        const unsub = NetInfo.addEventListener((state) => {
            setIsOffline(!state.isConnected || !state.isInternetReachable);
        });
        return unsub;
    }, []);

    return isOffline;
}
