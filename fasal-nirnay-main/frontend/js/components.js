/**
 * FasalNirnay AI - Master Components Aggregator
 */
const Components = {
    // Onboarding (Pages 1-5)
    renderSplash: () => OnboardingComponents.renderSplash(),
    renderOnboardingStep1: () => OnboardingComponents.renderOnboardingStep1(),
    renderOnboardingStep2: () => OnboardingComponents.renderOnboardingStep2(),
    renderOnboardingStep3: () => OnboardingComponents.renderOnboardingStep3(),
    renderOnboardingStep4: () => OnboardingComponents.renderOnboardingStep4(),

    // Layout & Navigation
    renderHeader: () => DashboardComponents.renderHeader(),
    renderBottomNav: () => DashboardComponents.renderBottomNav(),

    // Main Tabs (Pages 6-11)
    renderHomeScreen: () => DashboardComponents.renderHomeScreen(),
    renderMarketScreen: () => DashboardComponents.renderMarketScreen(),
    renderCropStrategyScreen: () => FeatureComponents.renderCropStrategyScreen(),
    renderClusterSellingScreen: () => FeatureComponents.renderClusterSellingScreen(),
    renderVoiceScreen: () => FeatureComponents.renderVoiceScreen(),
    renderWeatherScreen: () => FeatureComponents.renderWeatherScreen()
};

window.Components = Components;
