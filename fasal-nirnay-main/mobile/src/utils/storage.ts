import { MMKV } from 'react-native-mmkv';

export const storage = new MMKV({ id: 'fasalnirnay-storage' });

export const Storage = {
    get: (key: string): string | undefined => storage.getString(key),
    set: (key: string, value: string): void => storage.set(key, value),
    delete: (key: string): void => storage.delete(key),
    getBool: (key: string): boolean | undefined => storage.getBoolean(key),
    setBool: (key: string, value: boolean): void => storage.set(key, value),
};
