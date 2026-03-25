function renderRecommendation() {
    const container = document.createElement('div');
    container.className = 'page-container';
    
    container.innerHTML = `
        <h2 class="page-title">Executive Recommendation</h2>
        
        <div class="card" style="background: var(--primary-color); color: white; margin-bottom: var(--spacing-lg); padding: var(--spacing-xl);">
            <h3 style="font-size: 1.5rem; margin-bottom: 10px;">Primary Action: <strong>${mockData.overview.systemRecommendation}</strong></h3>
            <p style="font-size: 1.1rem; opacity: 0.9;">
                Data indicates a segment has become highly toxic to the OmniTech brand portfolio based on recent NLP analysis. Immediate investigation and potential discontinuation is advised to prevent cross-category reputational damage.
            </p>
        </div>

        <div class="chart-grid">
            <div class="card">
                <div class="card-title">Justification</div>
                <div style="margin-top: 15px;">
                    <div style="display: flex; gap: 15px; margin-bottom: 20px;">
                        <i class="fa-solid fa-arrow-trend-down" style="font-size: 1.5rem; color: var(--danger-color); margin-top: 5px;"></i>
                        <div>
                            <h4 style="font-size: 1rem; margin-bottom: 5px;">Sentiment Risk</h4>
                            <p style="color: var(--text-muted); font-size: 0.9rem;">Overall average sentiment is sitting at ${mockData.overview.avgSentiment}/100, driven by hardware defects and software glitches.</p>
                        </div>
                    </div>
                    
                    <div style="display: flex; gap: 15px; margin-bottom: 20px;">
                        <i class="fa-solid fa-share-nodes" style="font-size: 1.5rem; color: var(--warning-color); margin-top: 5px;"></i>
                        <div>
                            <h4 style="font-size: 1rem; margin-bottom: 5px;">Contagion Risk</h4>
                            <p style="color: var(--text-muted); font-size: 0.9rem;">NLP analysis indicates an increasing number of consumers stating negative opinions, threatening other profitable segments.</p>
                        </div>
                    </div>
                    
                    <div style="display: flex; gap: 15px;">
                        <i class="fa-solid fa-triangle-exclamation" style="font-size: 1.5rem; color: var(--success-color); margin-top: 5px;"></i>
                        <div>
                            <h4 style="font-size: 1rem; margin-bottom: 5px;">Backlash Status</h4>
                            <p style="color: var(--text-muted); font-size: 0.9rem;">The current critical alert level is: ${mockData.overview.backlashMetric}. Focus marketing suppression here.</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="card" style="display: flex; flex-direction: column;">
                <div class="card-title">Expected Outcome</div>
                <div id="outcome-chart" style="flex: 1; display:flex; flex-direction:column;"></div>
            </div>
        </div>
    `;

    const outcomeChart = container.querySelector('#outcome-chart');
    outcomeChart.appendChild(createChartPlaceholder('Brand Sentiment Recovery', '100%', 'Waterfall chart showing sequential sentiment recovery post-discontinuation'));

    return container;
}
