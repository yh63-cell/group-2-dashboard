// Application Global State and Routing
const App = {
    state: {
        currentPage: 'Overview',
        selectedProduct: null
    },

    pages: {
        'Overview': renderOverview,
        'Product Comparison': renderProductComparison,
        'Feature Insights': renderFeatureInsights,
        'Product Detail': renderProductDetail,
        'Backlash Risk': renderBacklashRisk,
        'Consumer Language': renderConsumerLanguage,
        'Recommendation': renderRecommendation
    },

    init() {
        // Initialize Navigation
        Navigation.init(Object.keys(this.pages), this.state.currentPage);
        
        // Render Initial Page
        this.navigate(this.state.currentPage);
    },

    navigate(pageName) {
        if (!this.pages[pageName]) return;
        
        this.state.currentPage = pageName;
        Navigation.setActive(pageName);
        
        const mainContent = document.getElementById('main-content');
        mainContent.innerHTML = '';
        
        // Execute the render function for the page
        const pageContent = this.pages[pageName]();
        mainContent.appendChild(pageContent);
    }
};

// Start App when DOM is ready
document.addEventListener('DOMContentLoaded', async () => {
    if (window.loadRealData) {
        await window.loadRealData();
    }
    App.init();
});
