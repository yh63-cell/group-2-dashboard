function renderOverview() {
    const container = document.createElement('div');
    container.className = 'page-container';
    
    container.innerHTML = `
        <h2 class="page-title">Executive Overview</h2>
        
        <div class="kpi-grid"></div>
        
        <div class="chart-grid">
            <div id="overview-sentiment-trend"></div>
            <div id="overview-reco-card"></div>
        </div>
    `;

    // Populate KPIs
    const kpiGrid = container.querySelector('.kpi-grid');
    kpiGrid.appendChild(createKPICard('Total Reviews Analyzed', mockData.overview.totalReviews.toLocaleString()));
    kpiGrid.appendChild(createKPICard('Average Sentiment', mockData.overview.avgSentiment + '/100', '-3% vs Last Q', 'negative'));
    kpiGrid.appendChild(createKPICard('Critical Backlash Risk', mockData.overview.backlashMetric, 'Requires Action', 'negative'));

    // Populate Charts
    const trendContainer = container.querySelector('#overview-sentiment-trend');
    trendContainer.appendChild(createChartPlaceholder('Overall Sentiment Trend (YTD)', '350px', 'Line chart showing aggregated sentiment decline'));

    const recoContainer = container.querySelector('#overview-reco-card');
    const recoCard = document.createElement('div');
    recoCard.className = 'card';
    recoCard.style.height = '100%';
    recoCard.innerHTML = `
        <div class="card-title">System Recommendation</div>
        <div style="text-align: center; margin-top: var(--spacing-lg);">
            <i class="fa-solid fa-triangle-exclamation" style="font-size: 3rem; color: var(--danger-color); margin-bottom: 20px;"></i>
            <h3 style="font-size: 1.25rem; margin-bottom: 10px;">${mockData.overview.systemRecommendation}</h3>
            <p style="color: var(--text-muted); font-size: 0.9rem;">Automated flag based on lowest sentiment threshold and highest negative review volume.</p>
            <button style="margin-top: 20px; padding: 10px 20px; background: var(--primary-color); color: white; border: none; border-radius: var(--radius); cursor: pointer;" onclick="App.navigate('Recommendation')">View Full Analysis</button>
        </div>
    `;
    recoContainer.appendChild(recoCard);

    return container;
}
