/**
 * FasalNirnay AI - Main Application Controller
 */
const App = {
    async init() {
        // Initialize voice engine
        VoiceHandler.init();

        // Check backend health
        ApiService.checkHealth().then(res => {
            console.log("FasalNirnay Backend Status:", res.status);
        });

        // Determine initial screen
        if (State.profile.isOnboarded) {
            State.currentScreen = "main";
            State.activeTab = "home";
        } else {
            State.currentScreen = "splash";
        }

        // Fetch initial live data
        await this.loadInitialData();

        // Render UI
        this.render();
    },

    async loadInitialData() {
        const crop = State.profile.crops[0] || "Wheat";
        const loc = `${State.profile.district}, ${State.profile.state}`;
        await Promise.allSettled([
            ApiService.getWeather(loc, crop),
            ApiService.getNews(State.profile.state, crop)
        ]);
    },

    render() {
        const appEl = document.getElementById('app-root');
        if (!appEl) return;

        if (State.currentScreen === "splash") {
            appEl.innerHTML = Components.renderSplash();
        } else if (State.currentScreen === "onboarding") {
            switch (State.onboardingStep) {
                case 1:
                    appEl.innerHTML = Components.renderOnboardingStep1();
                    break;
                case 2:
                    appEl.innerHTML = Components.renderOnboardingStep2();
                    break;
                case 3:
                    appEl.innerHTML = Components.renderOnboardingStep3();
                    break;
                case 4:
                    appEl.innerHTML = Components.renderOnboardingStep4();
                    break;
                default:
                    appEl.innerHTML = Components.renderOnboardingStep1();
            }
        } else if (State.currentScreen === "main") {
            let screenContent = "";
            switch (State.activeTab) {
                case "home":
                    screenContent = Components.renderHomeScreen();
                    break;
                case "market":
                    screenContent = Components.renderMarketScreen();
                    break;
                case "crops":
                    screenContent = Components.renderCropStrategyScreen();
                    break;
                case "voice":
                    screenContent = Components.renderVoiceScreen();
                    break;
                case "weather":
                    screenContent = Components.renderWeatherScreen();
                    break;
                case "cluster":
                    screenContent = Components.renderClusterSellingScreen();
                    break;
                default:
                    screenContent = Components.renderHomeScreen();
            }

            appEl.innerHTML = `
                <div class="flex flex-col h-full bg-slate-50 overflow-hidden">
                    ${Components.renderHeader()}
                    ${screenContent}
                    ${Components.renderBottomNav()}
                </div>
            `;
        }
    },

    changeLanguage(lang) {
        State.setLanguage(lang);
        this.render();
        this.showToast(`Language changed to ${lang.toUpperCase()}`);
    },

    navigateTo(screen) {
        State.currentScreen = screen;
        this.render();
    },

    startOnboarding() {
        State.currentScreen = "onboarding";
        State.onboardingStep = 1;
        this.render();
    },

    directSignIn() {
        State.profile.name = "Ravish";
        State.profile.state = "Maharashtra";
        State.profile.district = "Mumbai";
        State.profile.landArea = "2-5 acres";
        State.profile.crops = ["Wheat", "Rice", "Cotton", "Maize", "Barley", "Sugarcane"];
        State.profile.isOnboarded = true;
        State.saveProfile();
        State.currentScreen = "main";
        State.activeTab = "home";
        this.render();
        this.showToast("Signed in as Ravish 🙏");
    },

    setStep(step) {
        State.onboardingStep = step;
        this.render();
    },

    selectState(st) {
        State.profile.state = st;
        this.render();
    },

    submitStep1() {
        const nameInput = document.getElementById('input-farmer-name');
        const distInput = document.getElementById('input-farmer-district');
        if (nameInput && nameInput.value.trim()) State.profile.name = nameInput.value.trim();
        if (distInput && distInput.value.trim()) State.profile.district = distInput.value.trim();
        State.saveProfile();
        this.setStep(2);
    },

    selectLand(area) {
        State.profile.landArea = area;
        this.render();
    },

    submitStep2() {
        State.saveProfile();
        this.setStep(3);
    },

    toggleCrop(crop) {
        const index = State.profile.crops.indexOf(crop);
        if (index > -1) {
            if (State.profile.crops.length > 1) {
                State.profile.crops.splice(index, 1);
            } else {
                this.showToast("Select at least one crop");
            }
        } else {
            State.profile.crops.push(crop);
        }
        this.render();
    },

    submitStep3() {
        State.saveProfile();
        this.setStep(4);
    },

    async finishOnboarding() {
        State.profile.isOnboarded = true;
        State.saveProfile();
        State.currentScreen = "main";
        State.activeTab = "home";
        this.render();
        this.showToast("Welcome to FasalNirnay AI! ✨");
        await this.loadInitialData();
        this.render();
    },

    switchTab(tab) {
        State.activeTab = tab;
        this.render();
    },

    openWeatherModal() {
        this.switchTab('weather');
    },

    openClusterModal() {
        this.switchTab('cluster');
    },

    selectCommodity(c) {
        State.marketData.selectedCommodity = c;
        const prices = { "Cotton": 6420, "Wheat": 2275, "Rice": 2183, "Soybean": 4600 };
        State.marketData.predictedMinPrice = prices[c] || 2500;
        State.marketData.comparison = [
            { market: `${State.marketData.selectedMarket} (Central)`, distance_km: 12, price: State.marketData.predictedMinPrice, change: "+2.1%", trend: "up" },
            { market: "Akola", distance_km: 98, price: Math.round(State.marketData.predictedMinPrice * 0.98), change: "-0.8%", trend: "down" },
            { market: "Amravati", distance_km: 154, price: Math.round(State.marketData.predictedMinPrice * 1.02), change: "+3.2%", trend: "up" },
            { market: "Wardha", distance_km: 76, price: Math.round(State.marketData.predictedMinPrice * 0.99), change: "+1.0%", trend: "up" },
        ];
        this.render();
    },

    selectMarket(m) {
        State.marketData.selectedMarket = m;
        this.selectCommodity(State.marketData.selectedCommodity);
    },

    joinActivePool() {
        if (!State.activePool.userJoined) {
            State.activePool.userJoined = true;
            State.activePool.farmersJoined += 1;
            State.activePool.spotsFilled += 1;
            this.showToast("Joined Shared Logistics Pool! 🎉");
        } else {
            State.activePool.userJoined = false;
            State.activePool.farmersJoined -= 1;
            State.activePool.spotsFilled -= 1;
            this.showToast("Left Pool");
        }
        this.render();
    },

    requestJoinPool(id) {
        this.showToast(`Request sent to pool coordinator for ${id}`);
    },

    openCustomPoolModal() {
        const modal = document.getElementById('custom-pool-modal');
        if (modal) modal.classList.remove('hidden');
    },

    closeCustomPoolModal() {
        const modal = document.getElementById('custom-pool-modal');
        if (modal) modal.classList.add('hidden');
    },

    async runPoolOptimization() {
        const qty = parseFloat(document.getElementById('pool-calc-qty')?.value) || 80;
        const loc = document.getElementById('pool-calc-loc')?.value || State.profile.district;
        const crop = document.getElementById('pool-calc-crop')?.value || "wheat";

        const farmers = [
            { farmer_id: 1, quantity: qty, location: loc, crop: crop },
            { farmer_id: 2, quantity: 60.0, location: "Bahadurgarh", crop: crop }
        ];

        this.showToast("Running 10km Spatial Clustering & ML Optimizer...");
        const result = await ApiService.optimizePool(farmers);
        
        const resBox = document.getElementById('pool-calc-result');
        if (resBox && result && result.pools && result.pools[0]) {
            const p = result.pools[0];
            const rec = p.recommendation || {};
            resBox.innerHTML = `
                <div class="mt-3 p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-xs space-y-1">
                    <div class="font-bold text-emerald-900">Recommended Mandi: ${rec.mandi || 'Amravati'}</div>
                    <div>Predicted Price: ₹${rec.predicted_price || rec.price}/q (${rec.grade || 'FAQ'} Grade)</div>
                    <div>Logistics Cost: ₹${rec.transport_cost || '3.50'}/q (${rec.trucks_needed || 1} truck)</div>
                    <div class="font-extrabold text-emerald-800 text-sm pt-1 border-t border-emerald-200">
                        Net Payout: ₹${rec.net_price?.toFixed(2) || '6416.50'}/quintal
                    </div>
                </div>
            `;
            resBox.classList.remove('hidden');
        }
    },

    async askQuickQuestion(text) {
        this.switchTab('voice');
        await VoiceHandler.handleSpeechResult(text);
    },

    showToast(message) {
        let toast = document.getElementById('app-toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'app-toast';
            toast.className = 'fixed bottom-16 left-1/2 -translate-x-1/2 z-50 bg-slate-900 text-white text-xs px-4 py-2.5 rounded-full shadow-lg transition-opacity duration-300 pointer-events-none opacity-0';
            document.body.appendChild(toast);
        }
        toast.innerText = message;
        toast.classList.remove('opacity-0');
        setTimeout(() => toast.classList.add('opacity-0'), 2500);
    }
};

window.renderVoiceChat = function() {
    const container = document.getElementById('voice-chat-messages');
    if (container) {
        container.innerHTML = State.chatHistory.map(msg => `
            <div class="flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}">
                <div class="max-w-[85%] p-3 rounded-2xl text-xs ${msg.sender === 'user' ? 'bg-emerald-700 text-white rounded-br-none' : 'bg-white border border-slate-200 text-slate-800 rounded-bl-none shadow-sm'}">
                    <p class="leading-relaxed">${msg.text}</p>
                    <div class="mt-1 flex items-center justify-between text-[9px] ${msg.sender === 'user' ? 'text-emerald-200' : 'text-slate-400'}">
                        <span>${msg.timestamp}</span>
                        ${msg.sender === 'assistant' ? `
                            <button onclick="VoiceHandler.speakText('${msg.text.replace(/'/g, "\\'")}')" class="ml-2 text-emerald-700 font-bold hover:underline flex items-center space-x-0.5">
                                <span>🔊</span>
                                <span>Listen</span>
                            </button>
                        ` : ''}
                    </div>
                </div>
            </div>
        `).join('');
        container.scrollTop = container.scrollHeight;
    }
};

window.App = App;

// Bootstrap on DOM ready
document.addEventListener('DOMContentLoaded', () => App.init());
