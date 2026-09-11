/**
 * FasalNirnay AI - Onboarding Components (Pages 1 to 5)
 */
const OnboardingComponents = {
    renderSplash() {
        const lang = State.profile.language;
        return `
            <div class="flex flex-col h-full bg-slate-50 justify-between p-6 select-none">
                <!-- Top Brand Header -->
                <div class="pt-2 flex flex-col items-center">
                    <div class="flex items-center space-x-2 text-emerald-800 font-extrabold text-xl tracking-wide">
                        <span class="text-2xl">🌾</span>
                        <span>${State.t('appName')}</span>
                    </div>
                </div>

                <!-- Hero Image Banner -->
                <div class="my-3 rounded-3xl overflow-hidden shadow-md border border-slate-200/60 bg-gradient-to-b from-amber-100 to-amber-200 relative h-44 flex items-center justify-center">
                    <img src="https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=800&q=80" alt="Wheat Field" class="w-full h-full object-cover" />
                    <div class="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent"></div>
                    <div class="absolute z-10 flex items-center justify-center w-14 h-14 rounded-full bg-white/80 backdrop-blur-md shadow-md text-emerald-800">
                        <svg class="w-6 h-6 fill-current translate-x-0.5" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                    </div>
                </div>

                <!-- Headline & Subtitle -->
                <div class="text-center px-1">
                    <span class="text-[11px] font-bold tracking-widest text-emerald-800 uppercase">${State.t('tagline')}</span>
                    <h1 class="text-2xl font-extrabold text-slate-900 mt-1.5 leading-tight">${State.t('heroTitle')}</h1>
                    <p class="text-xs text-slate-600 mt-1.5 leading-relaxed">${State.t('heroSubtitle')}</p>
                </div>

                <!-- Language Selection -->
                <div class="mt-3">
                    <p class="text-xs text-center text-slate-500 font-medium mb-2">${State.t('chooseLanguage')}</p>
                    <div class="grid grid-cols-4 gap-2">
                        <button onclick="App.changeLanguage('en')" class="py-2.5 px-1 rounded-xl text-xs text-center transition-all ${lang === 'en' ? 'pill-selected' : 'pill-unselected'}">English</button>
                        <button onclick="App.changeLanguage('hi')" class="py-2.5 px-1 rounded-xl text-xs text-center transition-all ${lang === 'hi' ? 'pill-selected' : 'pill-unselected'}">हिन्दी</button>
                        <button onclick="App.changeLanguage('pa')" class="py-2.5 px-1 rounded-xl text-xs text-center transition-all ${lang === 'pa' ? 'pill-selected' : 'pill-unselected'}">ਪੰਜਾਬੀ</button>
                        <button onclick="App.changeLanguage('mr')" class="py-2.5 px-1 rounded-xl text-xs text-center transition-all ${lang === 'mr' ? 'pill-selected' : 'pill-unselected'}">मराठी</button>
                    </div>
                </div>

                <!-- CTA Buttons -->
                <div class="mt-5 space-y-2.5 pb-2">
                    <button onclick="App.startOnboarding()" class="w-full py-3.5 bg-emerald-700 hover:bg-emerald-800 text-white font-semibold rounded-full shadow-md shadow-emerald-700/20 active:scale-[0.98] transition-transform text-sm">
                        ${State.t('getStarted')}
                    </button>
                    <button onclick="App.directSignIn()" class="w-full py-3 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 font-semibold rounded-full active:scale-[0.98] transition-transform text-sm">
                        ${State.t('signIn')}
                    </button>
                </div>
            </div>
        `;
    },

    renderOnboardingStep1() {
        const states = ["Punjab", "Haryana", "Uttar Pradesh", "Rajasthan", "Maharashtra", "Madhya Pradesh"];
        return `
            <div class="flex flex-col h-full bg-slate-50 justify-between p-6">
                <div>
                    <div class="flex items-center justify-between pt-1">
                        <button onclick="App.navigateTo('splash')" class="p-2 rounded-full hover:bg-slate-200 text-slate-600">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
                        </button>
                        <span class="font-bold text-emerald-800 text-base">${State.t('appName')}</span>
                        <span class="text-xs font-semibold text-slate-500">Step 1 of 4</span>
                    </div>

                    <div class="w-full bg-slate-200 h-1.5 rounded-full mt-4 overflow-hidden">
                        <div class="bg-emerald-600 h-full w-1/4 rounded-full transition-all duration-300"></div>
                    </div>

                    <div class="mt-5">
                        <h2 class="text-2xl font-extrabold text-slate-900">${State.t('step1Title')}</h2>
                        <p class="text-xs text-slate-500 mt-1 leading-relaxed">${State.t('step1Subtitle')}</p>
                    </div>

                    <div class="mt-5 space-y-4">
                        <div>
                            <label class="block text-xs font-semibold text-slate-700 mb-1.5">${State.t('yourName')}</label>
                            <input id="input-farmer-name" type="text" value="${State.profile.name}" placeholder="${State.t('namePlaceholder')}"
                                class="w-full px-4 py-2.5 bg-white border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-emerald-600 focus:border-transparent" />
                        </div>

                        <div>
                            <label class="block text-xs font-semibold text-slate-700 mb-2">${State.t('state')}</label>
                            <div class="grid grid-cols-3 gap-2">
                                ${states.map(st => `
                                    <button onclick="App.selectState('${st}')" class="py-2.5 px-1 text-xs text-center rounded-xl transition-all ${State.profile.state === st ? 'pill-selected' : 'pill-unselected'}">
                                        ${st}
                                    </button>
                                `).join('')}
                            </div>
                        </div>

                        <div>
                            <label class="block text-xs font-semibold text-slate-700 mb-1.5">${State.t('districtCity')}</label>
                            <input id="input-farmer-district" type="text" value="${State.profile.district}" placeholder="${State.t('districtPlaceholder')}"
                                class="w-full px-4 py-2.5 bg-white border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-emerald-600 focus:border-transparent" />
                        </div>
                    </div>
                </div>

                <div class="mt-5 pb-2">
                    <button onclick="App.submitStep1()" class="w-full py-3.5 bg-emerald-700 hover:bg-emerald-800 text-white font-semibold rounded-full shadow-md shadow-emerald-700/20 active:scale-[0.98] transition-transform text-sm">
                        ${State.t('continue')}
                    </button>
                </div>
            </div>
        `;
    },

    renderOnboardingStep2() {
        const landOptions = ["< 2 acres", "2-5 acres", "5-10 acres", "10-25 acres", "25+ acres"];
        return `
            <div class="flex flex-col h-full bg-slate-50 justify-between p-6">
                <div>
                    <div class="flex items-center justify-between pt-1">
                        <button onclick="App.setStep(1)" class="p-2 rounded-full hover:bg-slate-200 text-slate-600">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
                        </button>
                        <span class="font-bold text-emerald-800 text-base">${State.t('appName')}</span>
                        <span class="text-xs font-semibold text-slate-500">Step 2 of 4</span>
                    </div>

                    <div class="w-full bg-slate-200 h-1.5 rounded-full mt-4 overflow-hidden">
                        <div class="bg-emerald-600 h-full w-2/4 rounded-full transition-all duration-300"></div>
                    </div>

                    <div class="mt-5">
                        <h2 class="text-2xl font-extrabold text-slate-900">${State.t('step2Title')}</h2>
                        <p class="text-xs text-slate-500 mt-1 leading-relaxed">${State.t('step2Subtitle')}</p>
                    </div>

                    <div class="mt-6">
                        <label class="block text-xs font-semibold text-slate-700 mb-3">${State.t('landArea')}</label>
                        <div class="flex flex-wrap gap-2.5">
                            ${landOptions.map(opt => `
                                <button onclick="App.selectLand('${opt}')" class="py-2.5 px-4 text-xs font-medium rounded-xl transition-all ${State.profile.landArea === opt ? 'pill-selected' : 'pill-unselected'}">
                                    ${opt}
                                </button>
                            `).join('')}
                        </div>
                    </div>
                </div>

                <div class="mt-6 space-y-2.5 pb-2 text-center">
                    <button onclick="App.submitStep2()" class="w-full py-3.5 bg-emerald-700 hover:bg-emerald-800 text-white font-semibold rounded-full shadow-md shadow-emerald-700/20 active:scale-[0.98] transition-transform text-sm">
                        ${State.t('continue')}
                    </button>
                    <button onclick="App.setStep(1)" class="text-xs font-semibold text-slate-600 hover:text-slate-900 py-1">
                        ${State.t('back')}
                    </button>
                </div>
            </div>
        `;
    },

    renderOnboardingStep3() {
        const cropOptions = ["Wheat", "Rice", "Cotton", "Soybean", "Mustard", "Sugarcane", "Maize", "Barley"];
        return `
            <div class="flex flex-col h-full bg-slate-50 justify-between p-6">
                <div>
                    <div class="flex items-center justify-between pt-1">
                        <button onclick="App.setStep(2)" class="p-2 rounded-full hover:bg-slate-200 text-slate-600">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
                        </button>
                        <span class="font-bold text-emerald-800 text-base">${State.t('appName')}</span>
                        <span class="text-xs font-semibold text-slate-500">Step 3 of 4</span>
                    </div>

                    <div class="w-full bg-slate-200 h-1.5 rounded-full mt-4 overflow-hidden">
                        <div class="bg-emerald-600 h-full w-3/4 rounded-full transition-all duration-300"></div>
                    </div>

                    <div class="mt-5">
                        <h2 class="text-2xl font-extrabold text-slate-900">${State.t('step3Title')}</h2>
                        <p class="text-xs text-slate-500 mt-1 leading-relaxed">${State.t('step3Subtitle')}</p>
                    </div>

                    <div class="mt-6">
                        <label class="block text-xs font-semibold text-slate-700 mb-3">${State.t('crops')}</label>
                        <div class="grid grid-cols-3 gap-2.5">
                            ${cropOptions.map(crop => {
                                const isSelected = State.profile.crops.includes(crop);
                                return `
                                    <button onclick="App.toggleCrop('${crop}')" class="py-2.5 px-2 text-xs font-medium text-center rounded-xl transition-all ${isSelected ? 'pill-selected' : 'pill-unselected'}">
                                        ${crop}
                                    </button>
                                `;
                            }).join('')}
                        </div>
                    </div>
                </div>

                <div class="mt-6 space-y-2.5 pb-2 text-center">
                    <button onclick="App.submitStep3()" class="w-full py-3.5 bg-emerald-700 hover:bg-emerald-800 text-white font-semibold rounded-full shadow-md shadow-emerald-700/20 active:scale-[0.98] transition-transform text-sm">
                        ${State.t('continue')}
                    </button>
                    <button onclick="App.setStep(2)" class="text-xs font-semibold text-slate-600 hover:text-slate-900 py-1">
                        ${State.t('back')}
                    </button>
                </div>
            </div>
        `;
    },

    renderOnboardingStep4() {
        return `
            <div class="flex flex-col h-full bg-slate-50 justify-between p-6">
                <div>
                    <div class="flex items-center justify-between pt-1">
                        <button onclick="App.setStep(3)" class="p-2 rounded-full hover:bg-slate-200 text-slate-600">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
                        </button>
                        <span class="font-bold text-emerald-800 text-base">${State.t('appName')}</span>
                        <span class="text-xs font-semibold text-slate-500">Step 4 of 4</span>
                    </div>

                    <div class="w-full bg-slate-200 h-1.5 rounded-full mt-4 overflow-hidden">
                        <div class="bg-emerald-600 h-full w-full rounded-full transition-all duration-300"></div>
                    </div>

                    <div class="mt-5">
                        <h2 class="text-2xl font-extrabold text-slate-900">${State.t('step4Title')}</h2>
                        <p class="text-xs text-slate-500 mt-1 leading-relaxed">${State.t('step4Subtitle')}</p>
                    </div>

                    <div class="mt-6 bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-3">
                        <div class="flex items-center space-x-2 text-slate-900 font-bold text-sm">
                            <span class="text-red-500">📍</span>
                            <span>${State.profile.district}, ${State.profile.state}</span>
                        </div>
                        <div class="text-xs text-slate-700">
                            <span class="font-semibold text-slate-500">Land:</span> ${State.profile.landArea}
                        </div>
                        <div class="text-xs text-slate-700 leading-relaxed">
                            <span class="font-semibold text-slate-500">Crops:</span> ${State.profile.crops.join(', ')}
                        </div>
                    </div>
                </div>

                <div class="mt-6 space-y-2.5 pb-2 text-center">
                    <button onclick="App.finishOnboarding()" class="w-full py-3.5 bg-emerald-700 hover:bg-emerald-800 text-white font-semibold rounded-full shadow-md shadow-emerald-700/20 active:scale-[0.98] transition-transform text-sm flex items-center justify-center space-x-2">
                        <span>${State.t('startGrowing')}</span>
                    </button>
                    <button onclick="App.setStep(3)" class="text-xs font-semibold text-slate-600 hover:text-slate-900 py-1">
                        ${State.t('back')}
                    </button>
                </div>
            </div>
        `;
    }
};

window.OnboardingComponents = OnboardingComponents;
