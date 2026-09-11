/**
 * FasalNirnay AI - State Management
 */
const State = {
    // Current user profile
    profile: {
        name: localStorage.getItem('fn_name') || "Ravish",
        state: localStorage.getItem('fn_state') || "Maharashtra",
        district: localStorage.getItem('fn_district') || "Mumbai",
        landArea: localStorage.getItem('fn_land') || "2-5 acres",
        crops: JSON.parse(localStorage.getItem('fn_crops') || '["Wheat", "Rice", "Cotton", "Maize", "Barley", "Sugarcane"]'),
        language: localStorage.getItem('fn_lang') || "hi",
        isOnboarded: localStorage.getItem('fn_onboarded') === "true",
    },

    // Navigation state
    currentScreen: "splash", // splash, onboarding, main
    onboardingStep: 1, // 1 to 4
    activeTab: "home", // home, market, crops, voice, weather

    // Live data cache
    weatherData: null,
    newsData: [],
    marketData: {
        selectedCommodity: "Cotton",
        selectedMarket: "Nagpur",
        predictedMinPrice: 6420,
        grade: "FAQ",
        confidence: 87,
        status: "Sell Now",
        comparison: [
            { market: "Nagpur (Central)", distance_km: 12, price: 6420, change: "+2.1%", trend: "up" },
            { market: "Akola", distance_km: 98, price: 6310, change: "-0.8%", trend: "down" },
            { market: "Amravati", distance_km: 154, price: 6490, change: "+3.2%", trend: "up" },
            { market: "Wardha", distance_km: 76, price: 6380, change: "+1.0%", trend: "up" },
        ]
    },

    // Chat history for voice/text assistant
    chatHistory: [
        {
            sender: "assistant",
            text: "नमस्ते! मैं आपका फसल निर्णय एआई सलाहकार हूँ। आप मुझसे मंडी भाव, मौसम, या फसल रणनीति के बारे में पूछ सकते हैं।",
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            source: "gemini"
        }
    ],

    // Pools state
    activePool: {
        id: "pool_mh_01",
        title: "Shared Logistics Pool",
        route: "Nagpur → Amravati Mandi",
        farmersJoined: 4,
        maxFarmers: 6,
        estimatedSavings: 1200,
        departure: "Thu",
        spotsFilled: 4,
        crop: "Cotton",
        userJoined: false
    },

    nearbyPools: [
        {
            id: "pool_mh_02",
            route: "Nagpur → Wardha",
            departure: "Wed",
            crop: "Cotton",
            distance: "8 km from you",
            farmersJoined: 2,
            maxFarmers: 5,
            savings: 800,
            status: "open"
        },
        {
            id: "pool_mh_03",
            route: "Nagpur → Yavatmal",
            departure: "Fri",
            crop: "Soybean",
            distance: "14 km from you",
            farmersJoined: 3,
            maxFarmers: 6,
            savings: 950,
            status: "open"
        }
    ],

    // Save profile to localStorage
    saveProfile() {
        localStorage.setItem('fn_name', this.profile.name);
        localStorage.setItem('fn_state', this.profile.state);
        localStorage.setItem('fn_district', this.profile.district);
        localStorage.setItem('fn_land', this.profile.landArea);
        localStorage.setItem('fn_crops', JSON.stringify(this.profile.crops));
        localStorage.setItem('fn_lang', this.profile.language);
        localStorage.setItem('fn_onboarded', this.profile.isOnboarded ? "true" : "false");
    },

    // Helper to get translation
    t(key) {
        const lang = this.profile.language || 'en';
        const dict = I18N[lang] || I18N.en;
        return dict[key] || I18N.en[key] || key;
    },

    // Set language
    setLanguage(lang) {
        if (I18N[lang]) {
            this.profile.language = lang;
            this.saveProfile();
            document.documentElement.lang = lang;
        }
    }
};

window.State = State;
