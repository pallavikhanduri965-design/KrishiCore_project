/**
 * FasalNirnay AI - Feature Screens & Modals (Pages 8, 9, 10, Weather)
 */
const FeatureComponents = {
    renderCropStrategyScreen() {
        return `
            <div class="flex-1 overflow-y-auto px-5 py-4 space-y-4 bg-slate-50">
                <div class="flex items-center justify-between text-xs text-slate-500">
                    <span class="font-bold text-emerald-800">${State.t('cropStrategy')}</span>
                    <span>• Updated 2 mins ago</span>
                </div>

                <div class="bg-white rounded-2xl p-4 border border-slate-100 shadow-sm text-xs text-slate-700 leading-relaxed">
                    "...your stock now to lock in current gains, and hold 40% for the projected price peak in 2 weeks."
                </div>

                <div>
                    <h3 class="font-bold text-slate-800 text-xs mb-2.5">${State.t('thisWeeksActions')}</h3>
                    <div class="space-y-2.5">
                        <div class="bg-white p-3.5 rounded-2xl border border-slate-100 shadow-sm flex items-center space-x-3">
                            <div class="w-6 h-6 rounded-full bg-emerald-800 text-white font-bold text-xs flex items-center justify-center flex-shrink-0">1</div>
                            <div class="flex-1">
                                <h4 class="font-bold text-xs text-slate-900">Harvest within 10 days</h4>
                                <p class="text-[10px] text-slate-500">Optimal moisture content predicted</p>
                            </div>
                            <span class="text-base">🌾</span>
                        </div>

                        <div class="bg-white p-3.5 rounded-2xl border border-slate-100 shadow-sm flex items-center space-x-3">
                            <div class="w-6 h-6 rounded-full bg-amber-500 text-white font-bold text-xs flex items-center justify-center flex-shrink-0">2</div>
                            <div class="flex-1">
                                <h4 class="font-bold text-xs text-slate-900">Target Amravati Mandi</h4>
                                <p class="text-[10px] text-slate-500">Highest price forecast this week</p>
                            </div>
                            <span class="text-base">🏬</span>
                        </div>

                        <div class="bg-white p-3.5 rounded-2xl border border-slate-100 shadow-sm flex items-center space-x-3">
                            <div class="w-6 h-6 rounded-full bg-slate-700 text-white font-bold text-xs flex items-center justify-center flex-shrink-0">3</div>
                            <div class="flex-1">
                                <h4 class="font-bold text-xs text-slate-900">Arrange transport pooling</h4>
                                <p class="text-[10px] text-slate-500">Save ₹800–1,200 on logistics</p>
                            </div>
                            <span class="text-base">🚛</span>
                        </div>
                    </div>
                </div>

                <div class="bg-white rounded-3xl p-4 border border-slate-100 shadow-sm space-y-3.5">
                    <h3 class="font-bold text-slate-800 text-xs">${State.t('riskAssessment')}</h3>

                    <div>
                        <div class="flex justify-between text-xs mb-1 font-semibold">
                            <span class="text-slate-700">${State.t('weatherRisk')}</span>
                            <span class="text-emerald-600 font-bold">${State.t('low')}</span>
                        </div>
                        <div class="risk-meter">
                            <div class="h-full rounded-full risk-fill-low"></div>
                        </div>
                    </div>

                    <div>
                        <div class="flex justify-between text-xs mb-1 font-semibold">
                            <span class="text-slate-700">${State.t('priceVolatility')}</span>
                            <span class="text-amber-600 font-bold">${State.t('medium')}</span>
                        </div>
                        <div class="risk-meter">
                            <div class="h-full rounded-full risk-fill-medium"></div>
                        </div>
                    </div>

                    <div>
                        <div class="flex justify-between text-xs mb-1 font-semibold">
                            <span class="text-slate-700">${State.t('pestRisk')}</span>
                            <span class="text-emerald-600 font-bold">${State.t('low')}</span>
                        </div>
                        <div class="risk-meter">
                            <div class="h-full rounded-full risk-fill-low"></div>
                        </div>
                    </div>

                    <div>
                        <div class="flex justify-between text-xs mb-1 font-semibold">
                            <span class="text-slate-700">${State.t('marketDemand')}</span>
                            <span class="text-red-500 font-bold">${State.t('high')}</span>
                        </div>
                        <div class="risk-meter">
                            <div class="h-full rounded-full risk-fill-high"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    },

    renderClusterSellingScreen() {
        const pool = State.activePool;
        return `
            <div class="flex-1 overflow-y-auto px-5 py-4 space-y-4 bg-slate-50">
                <div>
                    <h2 class="text-lg font-extrabold text-slate-900">${State.t('clusterSelling')}</h2>
                    <p class="text-xs text-slate-500 mt-0.5 leading-relaxed">${State.t('poolingSave')}</p>
                </div>

                <!-- Featured Active Pool Card (Gold Gradient) -->
                <div class="bg-gold-gradient rounded-3xl p-5 text-white shadow-md relative overflow-hidden">
                    <div class="flex items-center justify-between">
                        <span class="text-[9px] font-bold tracking-wider uppercase bg-black/20 px-2.5 py-1 rounded-full flex items-center space-x-1">
                            <span class="w-1.5 h-1.5 bg-emerald-400 rounded-full"></span>
                            <span>ACTIVE POOL</span>
                        </span>
                        <span class="text-xl">🚛</span>
                    </div>

                    <h3 class="text-base font-extrabold mt-2.5">${pool.title}</h3>
                    <p class="text-xs text-amber-100 font-medium">${pool.route}</p>

                    <div class="grid grid-cols-3 gap-2 mt-3 text-center">
                        <div class="bg-white/10 rounded-2xl p-2">
                            <span class="text-lg font-extrabold block">${pool.farmersJoined}/${pool.maxFarmers}</span>
                            <span class="text-[9px] text-amber-100">${State.t('farmersJoined')}</span>
                        </div>
                        <div class="bg-white/10 rounded-2xl p-2">
                            <span class="text-lg font-extrabold block">₹${pool.estimatedSavings}</span>
                            <span class="text-[9px] text-amber-100">${State.t('estimatedSavings')}</span>
                        </div>
                        <div class="bg-white/10 rounded-2xl p-2">
                            <span class="text-lg font-extrabold block">${pool.departure}</span>
                            <span class="text-[9px] text-amber-100">${State.t('departure')}</span>
                        </div>
                    </div>

                    <div class="mt-3">
                        <div class="flex justify-between text-[10px] text-amber-100 mb-1 font-semibold">
                            <span>Pool Capacity</span>
                            <span>${pool.spotsFilled} of ${pool.maxFarmers} spots filled</span>
                        </div>
                        <div class="w-full bg-black/20 h-1.5 rounded-full overflow-hidden">
                            <div class="bg-white h-full rounded-full" style="width: ${(pool.spotsFilled / pool.maxFarmers) * 100}%"></div>
                        </div>
                    </div>

                    <div class="mt-4">
                        <button onclick="App.joinActivePool()" class="w-full py-2.5 bg-white text-amber-900 font-bold rounded-full shadow hover:bg-slate-100 active:scale-[0.98] transition-transform text-xs">
                            ${pool.userJoined ? '✓ Joined Pool' : State.t('joinThisPool')}
                        </button>
                    </div>
                </div>

                <!-- Available Pools Nearby -->
                <div>
                    <div class="flex items-center justify-between mb-2.5">
                        <h3 class="font-bold text-slate-800 text-xs">${State.t('availablePoolsNearby')}</h3>
                        <button onclick="App.openCustomPoolModal()" class="text-xs font-semibold text-emerald-700 hover:text-emerald-800">+ Calculate Pool</button>
                    </div>

                    <div class="space-y-2.5">
                        ${State.nearbyPools.map(p => `
                            <div class="bg-white p-3.5 rounded-2xl border border-slate-100 shadow-sm">
                                <div class="flex items-center justify-between">
                                    <h4 class="font-bold text-xs text-slate-900">${p.route}</h4>
                                    <span class="bg-blue-600 text-white text-[9px] font-bold px-2 py-0.5 rounded-full">${p.departure}</span>
                                </div>
                                <p class="text-[10px] text-slate-500 mt-0.5">${p.crop} • ${p.distance}</p>
                                
                                <div class="mt-2.5 flex items-center justify-between text-xs">
                                    <span class="text-slate-600 font-semibold text-[11px]">${p.farmersJoined}/${p.maxFarmers} farmers</span>
                                    <span class="font-bold text-emerald-700 text-xs">Save ₹${p.savings}</span>
                                </div>

                                <div class="w-full bg-slate-100 h-1.5 rounded-full mt-1 overflow-hidden">
                                    <div class="bg-emerald-600 h-full rounded-full" style="width: ${(p.farmersJoined / p.maxFarmers) * 100}%"></div>
                                </div>

                                <button onclick="App.requestJoinPool('${p.id}')" class="w-full mt-2.5 py-2 border border-slate-200 hover:bg-slate-50 text-slate-700 font-bold rounded-xl text-xs active:scale-[0.98]">
                                    ${State.t('requestToJoin')}
                                </button>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    },

    renderVoiceScreen() {
        return `
            <div class="flex-1 flex flex-col h-full bg-slate-50 overflow-hidden">
                <div class="px-5 pt-3 pb-1 flex-shrink-0">
                    <h2 class="text-lg font-extrabold text-slate-900">${State.t('voiceAssistant')}</h2>
                    <p class="text-xs text-slate-500 mt-0.5">${State.t('speakPrompt')}</p>
                </div>

                <!-- Big Pulsing Microphone Centerpiece -->
                <div class="my-3 flex flex-col items-center justify-center relative select-none flex-shrink-0">
                    <div id="voice-mic-pulse" class="absolute w-28 h-28 rounded-full bg-emerald-500/20 mic-pulse-ring hidden"></div>
                    <button id="voice-mic-btn" onclick="VoiceHandler.toggleRecording()" class="relative z-10 w-20 h-20 rounded-full bg-emerald-700 text-white flex items-center justify-center shadow-xl shadow-emerald-700/30 transition-all duration-200 active:scale-95">
                        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/></svg>
                    </button>
                    <p id="voice-mic-status" class="mt-2 text-xs font-semibold text-slate-600 flex items-center space-x-1">
                        <span class="w-1.5 h-1.5 rounded-full bg-emerald-600"></span>
                        <span>${State.t('tapToSpeak')}</span>
                    </p>
                </div>

                <!-- Scrollable Container -->
                <div class="flex-1 overflow-y-auto px-5 space-y-3">
                    <div>
                        <h3 class="font-bold text-slate-800 text-[10px] mb-2 uppercase tracking-wider">${State.t('quickQuestions')}</h3>
                        <div class="space-y-1.5">
                            <button onclick="App.askQuickQuestion('What is the best mandi to sell wheat this week?')" class="w-full bg-white p-2.5 rounded-xl border border-slate-100 shadow-sm text-left text-xs font-semibold text-slate-700 flex items-center justify-between hover:bg-slate-50 transition-colors">
                                <div class="flex items-center space-x-2">
                                    <span class="text-amber-500 font-bold">?</span>
                                    <span>What is the best mandi to sell wheat this week?</span>
                                </div>
                                <span class="text-slate-400">→</span>
                            </button>

                            <button onclick="App.askQuickQuestion('Is it going to rain in my area next week?')" class="w-full bg-white p-2.5 rounded-xl border border-slate-100 shadow-sm text-left text-xs font-semibold text-slate-700 flex items-center justify-between hover:bg-slate-50 transition-colors">
                                <div class="flex items-center space-x-2">
                                    <span class="text-blue-500 font-bold">?</span>
                                    <span>Is it going to rain in my area next week?</span>
                                </div>
                                <span class="text-slate-400">→</span>
                            </button>

                            <button onclick="App.askQuickQuestion('क्या मुझे अभी बेचना चाहिए या इंतजार करना चाहिए?')" class="w-full bg-white p-2.5 rounded-xl border border-slate-100 shadow-sm text-left text-xs font-semibold text-slate-700 flex items-center justify-between hover:bg-slate-50 transition-colors">
                                <div class="flex items-center space-x-2">
                                    <span>🇮🇳</span>
                                    <span>क्या मुझे अभी बेचना चाहिए या इंतजार करना चाहिए?</span>
                                </div>
                                <span class="text-slate-400">→</span>
                            </button>

                            <button onclick="App.askQuickQuestion('What grade will my cotton likely get?')" class="w-full bg-white p-2.5 rounded-xl border border-slate-100 shadow-sm text-left text-xs font-semibold text-slate-700 flex items-center justify-between hover:bg-slate-50 transition-colors">
                                <div class="flex items-center space-x-2">
                                    <span class="text-emerald-500 font-bold">?</span>
                                    <span>What grade will my cotton likely get?</span>
                                </div>
                                <span class="text-slate-400">→</span>
                            </button>
                        </div>
                    </div>

                    <!-- Chat Messages Stream -->
                    <div id="voice-chat-messages" class="space-y-2.5 pt-1 pb-4">
                        ${State.chatHistory.map(msg => `
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
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    },

    renderWeatherScreen() {
        const weather = State.weatherData || {
            location: "Mumbai, Maharashtra",
            current_temp_c: 29.5,
            humidity: 58,
            wind_kph: 12.4,
            condition: "Clear",
            forecast: [
                { day: 1, max_temp_c: 32.0, min_temp_c: 22.0, condition: "Sunny", rain_chance_pct: 5 },
                { day: 2, max_temp_c: 31.5, min_temp_c: 21.0, condition: "Partly Cloudy", rain_chance_pct: 15 },
                { day: 3, max_temp_c: 30.0, min_temp_c: 20.5, condition: "Clear", rain_chance_pct: 10 }
            ]
        };

        return `
            <div class="flex-1 overflow-y-auto px-5 py-4 space-y-4 bg-slate-50">
                <div>
                    <h2 class="text-lg font-extrabold text-slate-900">${State.t('todaysWeather')}</h2>
                    <p class="text-xs text-slate-500 mt-0.5">📍 ${weather.location}</p>
                </div>

                <div class="bg-gradient-to-br from-sky-500 to-blue-600 rounded-3xl p-5 text-white shadow-md">
                    <div class="flex items-center justify-between">
                        <div>
                            <span class="text-3xl font-extrabold">${weather.current_temp_c}°C</span>
                            <span class="block text-xs font-semibold text-sky-100 mt-0.5">${weather.condition}</span>
                        </div>
                        <span class="text-4xl">☀️</span>
                    </div>

                    <div class="grid grid-cols-2 gap-2 mt-4 pt-3 border-t border-white/20 text-xs">
                        <div class="flex items-center space-x-1.5">
                            <span>💧</span>
                            <span>Humidity: <strong>${weather.humidity}%</strong></span>
                        </div>
                        <div class="flex items-center space-x-1.5">
                            <span>💨</span>
                            <span>Wind: <strong>${weather.wind_kph} km/h</strong></span>
                        </div>
                    </div>
                </div>

                <div>
                    <h3 class="font-bold text-slate-800 text-xs mb-2.5">3-Day Agricultural Forecast</h3>
                    <div class="space-y-2">
                        ${(weather.forecast || []).map(f => `
                            <div class="bg-white p-3.5 rounded-2xl border border-slate-100 shadow-sm flex items-center justify-between">
                                <div class="flex items-center space-x-3">
                                    <span class="text-xl">${f.rain_chance_pct > 30 ? '🌧️' : '⛅'}</span>
                                    <div>
                                        <h4 class="font-bold text-xs text-slate-900">Day ${f.day}</h4>
                                        <p class="text-[10px] text-slate-500">${f.condition}</p>
                                    </div>
                                </div>
                                <div class="text-right">
                                    <div class="text-xs font-bold text-slate-800">${f.max_temp_c}° / ${f.min_temp_c}°C</div>
                                    <span class="text-[10px] font-semibold text-blue-600">${f.rain_chance_pct}% rain</span>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }
};

window.FeatureComponents = FeatureComponents;
