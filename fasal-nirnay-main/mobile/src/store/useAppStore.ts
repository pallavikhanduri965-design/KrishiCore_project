import { create } from 'zustand';
import { CropKey } from '../types/app.types';

type AppState = {
  farmerName: string;
  selectedCrop: CropKey;
  setFarmerName: (name: string) => void;
  setSelectedCrop: (crop: CropKey) => void;
};

export const useAppStore = create<AppState>((set) => ({
  farmerName: '',
  selectedCrop: 'wheat',
  setFarmerName: (name) => set({ farmerName: name }),
  setSelectedCrop: (crop) => set({ selectedCrop: crop }),
}));
