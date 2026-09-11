/**
 * FasalNirnay AI - Dashboard & Market Components (Pages 6, 7, 11)
 */
const DashboardComponents = {
    renderHeader() {
        return `
            <div class="px-5 pt-3 pb-2 bg-white flex items-center justify-between border-b border-slate-100 flex-shrink-0">
                <div>
                    <h1 class="text-base font-extrabold text-emerald-900 flex items-center space-x-1.5">
                        <span>Namaste, ${State.profile.name || 'Ravish'}</span>
                        <span>🙏</span>
                    </h1>
                    <div class="flex items-center space-x-1 text-xs text-slate-500 mt-0.5">
                        <span class="text-red-500 text-[10px]">📍</span>
                        <span>${State.profile.district}, ${State.profile.state.substring(0, 2)}</span>
                    </div>
                </div>
                <div class="relative cursor-pointer" onclick="App.openWeatherModal()">
                    <div class="w-9 h-9 rounded-full bg-amber-50 border border-amber-200/60 flex items-center justify-center text-amber-600">
                        <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.9 2 2 2zm6-6v-5c0-3.07-1.63-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.64 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z"/></svg>
                    </div>
                    <span class="absolute top-0.5 right-0.5 w-2 h-2 bg-red-500 rounded-full border-2 border-white"></span>
                </div>
            </div>
        `;
    },

    renderBottomNav() {
        const tab = State.activeTab;
        return `
            <div class="bg-white border-t border-slate-200 px-3 py-2 flex justify-around items-center z-20 flex-shrink-0">
                <button onclick="App.switchTab('home')" class="nav-item flex flex-col items-center py-1 px-2 ${tab === 'home' ? 'active' : 'text-slate-400'}">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
                    <span class="text-[10px] mt-1 font-semibold">${State.t('home')}</span>
                </button>
                <button onclick="App.switchTab('market')" class="nav-item flex flex-col items-center py-1 px-2 ${tab === 'market' ? 'active' : 'text-slate-400'}">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
                    <span class="text-[10px] mt-1 font-semibold">${State.t('market')}</span>
                </button>
                <button onclick="App.switchTab('crops')" class="nav-item flex flex-col items-center py-1 px-2 ${tab === 'crops' ? 'active' : 'text-slate-400'}">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>
                    <span class="text-[10px] mt-1 font-semibold">${State.t('crops')}</span>
                </button>
                <button onclick="App.switchTab('voice')" class="nav-item flex flex-col items-center py-1 px-2 ${tab === 'voice' ? 'active' : 'text-slate-400'}">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/></svg>
                    <span class="text-[10px] mt-1 font-semibold">${State.t('voice')}</span>
                </button>
                <button onclick="App.switchTab('weather')" class="nav-item flex flex-col items-center py-1 px-2 ${tab === 'weather' ? 'active' : 'text-slate-400'}">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 00-9.78 2.096A4.001 4.001 0 003 15z"/></svg>
                    <span class="text-[10px] mt-1 font-semibold">${State.t('weather')}</span>
                </button>
            </div>
        `;
    },

    renderHomeScreen() {
        const weather = State.weatherData || { current_temp_c: 29.5, condition: "Clear", humidity: 58, wind_kph: 12.4 };
        const news = (State.newsData && State.newsData.length > 0) ? State.newsData.slice(0, 3) : [
            { title: "Wheat MSP increased by ₹150/quintal", source: "Government of India", published_at: new Date().toISOString(), category: "Policy" },
            { title: "Heavy rain expected in Punjab next week", source: "IMD Alert", published_at: new Date().toISOString(), category: "Alert" },
            { title: "Cotton prices surge 8% in Nagpur mandi", source: "Mandi Board", published_at: new Date().toISOString(), category: "Sell" }
        ];

        return `
            <div class="flex-1 overflow-y-auto px-5 py-4 space-y-4 bg-slate-50">
                <!-- AI Recommendation Card (Green Gradient) -->
                <div class="bg-ai-gradient rounded-3xl p-5 text-white shadow-md relative overflow-hidden">
                    <div class="flex items-center justify-between">
                        <span class="text-[10px] font-semibold tracking-wider uppercase text-emerald-200">${State.t('aiRecommendation')}</span>
                    </div>
                    <div class="mt-2 flex items-center space-x-2">
                        <h2 class="text-2xl font-extrabold">${State.t('sellNow')}</h2>
                        <span class="text-xl">📈</span>
                    </div>
                    <p class="text-xs text-emerald-100 mt-1 max-w-[240px] leading-relaxed">
                        ${State.t('optimalPriceNotice')}
                    </p>
                    
                    <div class="mt-4 flex items-end justify-between">
                        <div>
                            <span class="text-[10px] text-emerald-200 block">${State.t('predictedPrice')}</span>
                            <div class="flex items-baseline space-x-1">
                                <span class="text-2xl font-extrabold tracking-tight">₹2,145</span>
                                <span class="text-xs text-emerald-200 font-medium">${State.t('perQuintal')}</span>
                            </div>
                        </div>
                        <button onclick="App.switchTab('market')" class="bg-white hover:bg-slate-100 text-emerald-900 font-bold px-4 py-2 rounded-full text-xs shadow-md transition-transform active:scale-95">
                            ${State.t('viewMarkets')}
                        </button>
                    </div>
                </div>

                <!-- Today's Weather Card -->
                <div class="bg-white rounded-3xl p-4 border border-slate-100 shadow-sm">
                    <div class="flex items-center justify-between mb-3">
                        <h3 class="font-bold text-slate-800 text-xs">${State.t('todaysWeather')}</h3>
                        <button onclick="App.switchTab('weather')" class="text-xs font-semibold text-emerald-700 hover:text-emerald-800">${State.t('fullForecast')}</button>
                    </div>
                    
                    <div class="grid grid-cols-4 gap-2 text-center">
                        <div class="bg-slate-50 rounded-2xl p-2">
                            <span class="text-lg block mb-0.5">☀️</span>
                            <span class="text-xs font-bold text-slate-800 block">${weather.current_temp_c}°C</span>
                            <span class="text-[10px] text-slate-500 font-medium">${State.t('clear')}</span>
                        </div>
                        <div class="bg-slate-50 rounded-2xl p-2">
                            <span class="text-lg block mb-0.5 text-blue-500">💧</span>
                            <span class="text-xs font-bold text-slate-800 block">${weather.humidity}%</span>
                            <span class="text-[10px] text-slate-500 font-medium">${State.t('humidity')}</span>
                        </div>
                        <div class="bg-slate-50 rounded-2xl p-2">
                            <span class="text-lg block mb-0.5 text-slate-500">💨</span>
                            <span class="text-xs font-bold text-slate-800 block">${weather.wind_kph} <span class="text-[8px]">km/h</span></span>
                            <span class="text-[10px] text-slate-500 font-medium">${State.t('wind')}</span>
                        </div>
                        <div class="bg-slate-50 rounded-2xl p-2">
                            <span class="text-lg block mb-0.5 text-sky-400">🌧️</span>
                            <span class="text-xs font-bold text-slate-800 block">0 <span class="text-[8px]">mm</span></span>
                            <span class="text-[10px] text-slate-500 font-medium">${State.t('rain')}</span>
                        </div>
                    </div>
                </div>

                <!-- Quick Actions Grid -->
                <div>
                    <h3 class="font-bold text-slate-800 text-xs mb-2.5">${State.t('quickActions')}</h3>
                    <div class="grid grid-cols-2 gap-2.5">
                        <button onclick="App.switchTab('market')" class="bg-white hover:bg-slate-50 border border-slate-100 p-3.5 rounded-2xl shadow-sm text-center flex flex-col items-center justify-center transition-all active:scale-95">
                            <span class="text-2xl mb-1">📊</span>
                            <span class="font-bold text-slate-800 text-xs">${State.t('mandiPrices')}</span>
                        </button>
                        <button onclick="App.switchTab('crops')" class="bg-white hover:bg-slate-50 border border-slate-100 p-3.5 rounded-2xl shadow-sm text-center flex flex-col items-center justify-center transition-all active:scale-95">
                            <span class="text-2xl mb-1">🌾</span>
                            <span class="font-bold text-slate-800 text-xs">${State.t('cropStrategy')}</span>
                        </button>
                        <button onclick="App.switchTab('voice')" class="bg-white hover:bg-slate-50 border border-slate-100 p-3.5 rounded-2xl shadow-sm text-center flex flex-col items-center justify-center transition-all active:scale-95">
                            <span class="text-2xl mb-1">🎙️</span>
                            <span class="font-bold text-slate-800 text-xs">${State.t('voiceAdvisor')}</span>
                        </button>
                        <button onclick="App.openClusterModal()" class="bg-white hover:bg-slate-50 border border-slate-100 p-3.5 rounded-2xl shadow-sm text-center flex flex-col items-center justify-center transition-all active:scale-95">
                            <span class="text-2xl mb-1">🤝</span>
                            <span class="font-bold text-slate-800 text-xs">${State.t('clusterSelling')}</span>
                        </button>
                    </div>
                </div>

                <!-- Page 11: Mandi Updates Feed -->
                <div>
                    <div class="flex items-center justify-between mb-2.5">
                        <div>
                            <h3 class="font-bold text-slate-800 text-xs">${State.t('mandiUpdates')}</h3>
                            <p class="text-[10px] text-slate-500">${State.t('latestFromRegion')}</p>
                        </div>
                    </div>
                    
                    <div class="space-y-2.5">
                        ${news.map(article => {
                            let badgeBg = "bg-blue-600";
                            let badgeText = article.category || "Policy";
                            if (article.category === 'Alert') badgeBg = "bg-red-600";
                            if (article.category === 'Sell') badgeBg = "bg-emerald-600";
                            return `
                                <div class="bg-white p-3.5 rounded-2xl border border-slate-100 shadow-sm flex items-start justify-between space-x-3">
                                    <div class="flex-1">
                                        <h4 class="font-bold text-xs text-slate-800 leading-snug">${article.title}</h4>
                                        <p class="text-[10px] text-slate-400 mt-1">${article.source} • 2h ago</p>
                                    </div>
                                    <span class="text-[10px] font-bold text-white px-2.5 py-0.5 rounded-full ${badgeBg}">${badgeText}</span>
                                </div>
                            `;
                        }).join('')}
                    </div>
                </div>
            </div>
        `;
    },

    renderMarketScreen() {
        const commodities = ["Wheat", "Cotton", "Rice", "Soybean"];
        const markets = ["Nagpur", "Akola", "Amravati", "Wardha"];
        const selCommodity = State.marketData.selectedCommodity;
        const selMarket = State.marketData.selectedMarket;

        return `
            <div class="flex-1 overflow-y-auto px-5 py-4 space-y-4 bg-slate-50">
                <!-- Title & Live Badge -->
                <div class="flex items-center justify-between">
                    <div>
                        <h2 class="text-lg font-extrabold text-slate-900">${State.t('marketIntelligence')}</h2>
                        <p class="text-xs text-slate-500 mt-0.5">${State.t('marketSubtitle')}</p>
                    </div>
                    <div class="flex items-center space-x-1 px-2.5 py-1 bg-red-100 text-red-700 rounded-full font-bold text-[10px]">
                        <span class="w-1.5 h-1.5 bg-red-600 rounded-full animate-pulse"></span>
                        <span>${State.t('live')}</span>
                    </div>
                </div>

                <!-- Select Commodity Pills -->
                <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1.5">${State.t('selectCommodity')}</label>
                    <div class="grid grid-cols-4 gap-2">
                        ${commodities.map(c => `
                            <button onclick="App.selectCommodity('${c}')" class="py-2 px-1 text-xs text-center rounded-xl transition-all ${selCommodity === c ? 'pill-selected' : 'pill-unselected'}">
                                ${c}
                            </button>
                        `).join('')}
                    </div>
                </div>

                <!-- Select Market Pills -->
                <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1.5">${State.t('selectMarket')}</label>
                    <div class="grid grid-cols-4 gap-2">
                        ${markets.map(m => `
                            <button onclick="App.selectMarket('${m}')" class="py-2 px-1 text-xs text-center rounded-xl transition-all ${selMarket === m ? 'pill-selected' : 'pill-unselected'}">
                                ${m}
                            </button>
                        `).join('')}
                    </div>
                </div>

                <!-- Main Predicted Price Card -->
                <div class="bg-white rounded-3xl p-5 border border-slate-100 shadow-sm">
                    <div class="flex items-center justify-between">
                        <span class="text-xs text-slate-500 font-semibold">${State.t('predictedMinPrice')}</span>
                        <span class="bg-emerald-700 text-white font-bold text-[10px] px-2.5 py-1 rounded-full flex items-center space-x-1">
                            <span>✓</span>
                            <span>${State.t('sellNow')}</span>
                        </span>
                    </div>
                    
                    <div class="mt-2 flex items-baseline space-x-1">
                        <span class="text-3xl font-extrabold text-emerald-800">₹${State.marketData.predictedMinPrice.toLocaleString()}</span>
                        <span class="text-xs text-slate-500 font-medium">${State.t('perQuintal')}</span>
                    </div>

                    <!-- Metrics Row: Grade, Confidence, Market -->
                    <div class="mt-4 pt-3 border-t border-slate-100 grid grid-cols-3 gap-2 text-center">
                        <div>
                            <span class="text-[10px] text-slate-400 font-semibold block uppercase">${State.t('grade')}</span>
                            <span class="text-sm font-bold text-slate-800">${State.marketData.grade}</span>
                        </div>
                        <div>
                            <span class="text-[10px] text-slate-400 font-semibold block uppercase">${State.t('confidence')}</span>
                            <span class="text-sm font-bold text-slate-800">${State.marketData.confidence}%</span>
                        </div>
                        <div>
                            <span class="text-[10px] text-slate-400 font-semibold block uppercase">${State.t('market')}</span>
                            <span class="text-sm font-bold text-slate-800">${selMarket}</span>
                        </div>
                    </div>
                </div>

                <!-- Mandi Price Comparison List -->
                <div>
                    <h3 class="font-bold text-slate-800 text-xs mb-2.5">${State.t('mandiPriceComparison')}</h3>
                    <div class="space-y-2">
                        ${State.marketData.comparison.map(comp => `
                            <div class="bg-white p-3.5 rounded-2xl border border-slate-100 shadow-sm flex items-center justify-between">
                                <div>
                                    <h4 class="font-bold text-xs text-slate-900">${comp.market}</h4>
                                    <span class="text-[10px] text-slate-500 font-medium">${comp.distance_km} km</span>
                                </div>
                                <div class="text-right">
                                    <div class="text-xs font-extrabold text-slate-900">₹${comp.price.toLocaleString()}</div>
                                    <span class="text-[10px] font-bold ${comp.trend === 'up' ? 'text-emerald-600' : 'text-red-500'}">
                                        ${comp.trend === 'up' ? '▲' : '▼'} ${comp.change}
                                    </span>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }
};

window.DashboardComponents = DashboardComponents;
