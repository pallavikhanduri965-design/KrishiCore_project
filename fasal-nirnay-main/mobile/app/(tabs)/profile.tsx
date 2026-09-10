import { View, Text, StyleSheet, SafeAreaView, TouchableOpacity, TextInput } from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { useAppStore } from '../../src/store/useAppStore';
import { useLanguage } from '../../src/hooks/useLanguage';
import { COLORS, LANGUAGES, CROPS } from '../../src/utils/constants';
import { Language, CropKey } from '../../src/types/app.types';

export default function ProfileScreen() {
    const { farmerName, selectedCrop, setFarmerName, setSelectedCrop } = useAppStore();
    const { language, changeLanguage } = useLanguage();

    return (
        <SafeAreaView style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.headerTitle}>⚙️ प्रोफ़ाइल</Text>
            </View>

            <View style={styles.scroll}>
                {/* Name */}
                <Text style={styles.label}>आपका नाम</Text>
                <TextInput
                    style={styles.input}
                    value={farmerName}
                    onChangeText={setFarmerName}
                    placeholder="अपना नाम लिखें"
                    placeholderTextColor="#999"
                />

                {/* Language */}
                <Text style={styles.label}>भाषा</Text>
                <View style={styles.row}>
                    {LANGUAGES.map((l) => (
                        <TouchableOpacity
                            key={l.key}
                            style={[styles.pill, language === l.key && styles.pillActive]}
                            onPress={() => changeLanguage(l.key as Language)}
                        >
                            <Text style={[styles.pillText, language === l.key && styles.pillTextActive]}>
                                {l.label}
                            </Text>
                        </TouchableOpacity>
                    ))}
                </View>

                {/* Crop */}
                <Text style={styles.label}>मुख्य फसल</Text>
                <View style={styles.cropGrid}>
                    {CROPS.map((c) => (
                        <TouchableOpacity
                            key={c.key}
                            style={[styles.cropCard, selectedCrop === c.key && styles.cropCardActive]}
                            onPress={() => setSelectedCrop(c.key as CropKey)}
                        >
                            <Text style={styles.cropEmoji}>{c.emoji}</Text>
                            <Text style={[styles.cropLabel, selectedCrop === c.key && styles.cropLabelActive]}>
                                {c.label}
                            </Text>
                        </TouchableOpacity>
                    ))}
                </View>

                {/* App info */}
                <View style={styles.infoCard}>
                    <MaterialCommunityIcons name="leaf" size={20} color={COLORS.greenPrimary} />
                    <Text style={styles.infoText}>FasalNirnay AI v1.0.0</Text>
                </View>
            </View>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#F9FBF7' },
    header: {
        backgroundColor: COLORS.greenPrimary,
        paddingTop: 16, paddingBottom: 16, paddingHorizontal: 20,
    },
    headerTitle: { fontSize: 22, fontWeight: '800', color: 'white' },
    scroll: { padding: 20, gap: 12 },
    label: { fontSize: 15, fontWeight: '700', color: COLORS.textPrimary, marginTop: 8 },
    input: {
        backgroundColor: 'white', borderRadius: 14, paddingHorizontal: 16,
        paddingVertical: 14, fontSize: 16, borderWidth: 1, borderColor: COLORS.border,
    },
    row: { flexDirection: 'row', gap: 10 },
    pill: {
        flex: 1, backgroundColor: 'white', borderRadius: 12, paddingVertical: 12,
        alignItems: 'center', borderWidth: 2, borderColor: COLORS.border,
    },
    pillActive: { borderColor: COLORS.greenPrimary, backgroundColor: COLORS.greenBg },
    pillText: { fontSize: 14, fontWeight: '600', color: COLORS.textSecondary },
    pillTextActive: { color: COLORS.greenPrimary },
    cropGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 10 },
    cropCard: {
        width: '30%', backgroundColor: 'white', borderRadius: 14,
        padding: 12, alignItems: 'center', gap: 4,
        borderWidth: 2, borderColor: COLORS.border,
    },
    cropCardActive: { borderColor: COLORS.greenPrimary, backgroundColor: COLORS.greenBg },
    cropEmoji: { fontSize: 28 },
    cropLabel: { fontSize: 12, fontWeight: '600', color: COLORS.textSecondary },
    cropLabelActive: { color: COLORS.greenPrimary },
    infoCard: {
        flexDirection: 'row', gap: 8, alignItems: 'center',
        backgroundColor: COLORS.greenBg, borderRadius: 12, padding: 14, marginTop: 16,
    },
    infoText: { fontSize: 13, color: COLORS.greenPrimary, fontWeight: '600' },
});