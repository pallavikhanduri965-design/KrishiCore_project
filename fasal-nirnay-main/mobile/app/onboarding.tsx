import { useState } from 'react';
import {
    View, Text, TouchableOpacity, StyleSheet,
    SafeAreaView, ScrollView,
} from 'react-native';
import { useRouter } from 'expo-router';
import { useAppStore } from '../src/store/useAppStore';
import { useLanguage } from '../src/hooks/useLanguage';
import { COLORS, LANGUAGES, CROPS } from '../src/utils/constants';
import { Language, CropKey } from '../src/types/app.types';

export default function OnboardingScreen() {
    const router = useRouter();
    const { setSelectedCrop, completeOnboarding } = useAppStore();
    const { language, changeLanguage } = useLanguage();
    const [selectedCrop, setLocalCrop] = useState<CropKey>('wheat');
    const [step, setStep] = useState<1 | 2>(1);

    const handleLanguageSelect = (lang: Language) => {
        changeLanguage(lang);
        setStep(2);
    };

    const handleDone = () => {
        setSelectedCrop(selectedCrop);
        completeOnboarding();
        router.replace('/(tabs)');
    };

    return (
        <SafeAreaView style={styles.container}>
            {step === 1 ? (
                <View style={styles.center}>
                    {/* Logo area */}
                    <Text style={styles.logo}>🌾</Text>
                    <Text style={styles.appName}>FasalNirnay</Text>
                    <Text style={styles.tagline}>AI फसल सलाहकार</Text>

                    <Text style={styles.sectionTitle}>अपनी भाषा चुनें</Text>
                    <Text style={styles.sectionTitle2}>Choose Your Language</Text>

                    <View style={styles.langGrid}>
                        {LANGUAGES.map((lang) => (
                            <TouchableOpacity
                                key={lang.key}
                                style={[styles.langCard, language === lang.key && styles.langCardActive]}
                                onPress={() => handleLanguageSelect(lang.key as Language)}
                            >
                                <Text style={styles.langScript}>{lang.script}</Text>
                                <Text style={[styles.langLabel, language === lang.key && styles.langLabelActive]}>
                                    {lang.label}
                                </Text>
                            </TouchableOpacity>
                        ))}
                    </View>
                </View>
            ) : (
                <ScrollView contentContainerStyle={styles.center}>
                    <Text style={styles.logo}>🌱</Text>
                    <Text style={styles.sectionTitle}>अपनी मुख्य फसल चुनें</Text>

                    <View style={styles.cropGrid}>
                        {CROPS.map((crop) => (
                            <TouchableOpacity
                                key={crop.key}
                                style={[styles.cropCard, selectedCrop === crop.key && styles.cropCardActive]}
                                onPress={() => setLocalCrop(crop.key as CropKey)}
                            >
                                <Text style={styles.cropEmoji}>{crop.emoji}</Text>
                                <Text style={[styles.cropLabel, selectedCrop === crop.key && styles.cropLabelActive]}>
                                    {crop.label}
                                </Text>
                            </TouchableOpacity>
                        ))}
                    </View>

                    <TouchableOpacity style={styles.startBtn} onPress={handleDone}>
                        <Text style={styles.startBtnText}>शुरू करें →</Text>
                    </TouchableOpacity>
                </ScrollView>
            )}
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#F9FBF7' },
    center: { flex: 1, alignItems: 'center', justifyContent: 'center', padding: 24, gap: 16 },
    logo: { fontSize: 72 },
    appName: { fontSize: 32, fontWeight: '800', color: COLORS.greenPrimary },
    tagline: { fontSize: 16, color: COLORS.textSecondary, marginBottom: 16 },
    sectionTitle: { fontSize: 22, fontWeight: '700', color: COLORS.textPrimary, textAlign: 'center' },
    sectionTitle2: { fontSize: 16, color: COLORS.textSecondary, marginTop: -8 },
    langGrid: { flexDirection: 'row', gap: 16, marginTop: 8 },
    langCard: {
        width: 100, height: 100, borderRadius: 20,
        backgroundColor: 'white', alignItems: 'center', justifyContent: 'center',
        borderWidth: 2, borderColor: COLORS.border, gap: 8,
        elevation: 2, shadowColor: '#000', shadowOpacity: 0.06, shadowRadius: 8,
    },
    langCardActive: { borderColor: COLORS.greenPrimary, backgroundColor: COLORS.greenBg },
    langScript: { fontSize: 32, fontWeight: '700', color: COLORS.textPrimary },
    langLabel: { fontSize: 13, fontWeight: '600', color: COLORS.textSecondary },
    langLabelActive: { color: COLORS.greenPrimary },
    cropGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 12, justifyContent: 'center' },
    cropCard: {
        width: 100, height: 100, borderRadius: 20,
        backgroundColor: 'white', alignItems: 'center', justifyContent: 'center',
        borderWidth: 2, borderColor: COLORS.border, gap: 6,
        elevation: 2, shadowColor: '#000', shadowOpacity: 0.06, shadowRadius: 8,
    },
    cropCardActive: { borderColor: COLORS.greenPrimary, backgroundColor: COLORS.greenBg },
    cropEmoji: { fontSize: 36 },
    cropLabel: { fontSize: 13, fontWeight: '600', color: COLORS.textSecondary },
    cropLabelActive: { color: COLORS.greenPrimary },
    startBtn: {
        backgroundColor: COLORS.greenPrimary, borderRadius: 16,
        paddingVertical: 18, paddingHorizontal: 48,
        marginTop: 8, width: '100%', alignItems: 'center',
        elevation: 4,
    },
    startBtnText: { fontSize: 20, fontWeight: '800', color: 'white' },
});