function renderBacklashRisk() {
    const container = document.createElement('div');
    container.className = 'page-container';
    
    container.innerHTML = `
        <h2 class="page-title">Reputational Backlash Risk Analysis</h2>
        
        <div class="card" style="margin-bottom: var(--spacing-lg); border-left: 4px solid var(--danger-color);">
            <div style="display: flex; gap: 20px; align-items: flex-start;">
                <i class="fa-solid fa-fire" style="color: var(--danger-color); font-size: 2rem;"></i>
                <div>
                    <h3 style="font-size: 1.1rem; margin-bottom: 8px;">Critical Alert: ${mockData.overview.backlashMetric}</h3>
                    <p style="color: var(--text-muted);">A product line has breached the critical threshold for social media backlash. A coordinated PR response and immediate investigation is highly advised to protect the broader brand equity.</p>
                </div>
            </div>
        </div>

        <div class="chart-grid">
            <div id="risk-matrix"></div>
            <div class="card">
                <div class="card-title">Risk Factors Explained</div>
                <ul style="margin-top: 15px; padding-left: 20px; color: var(--text-muted);">
                    <li style="margin-bottom: 10px;"><strong>Volume Velocity:</strong> Rapid spike in negative mentions over a 48-hour period.</li>
                    <li style="margin-bottom: 10px;"><strong>Defect Severity:</strong> Issues relate to core functionality (battery failure) rather than minor inconveniences.</li>
                    <li style="margin-bottom: 10px;"><strong>Viral Potential:</strong> Identified influencers echoing the sentiment across major platforms.</li>
                </ul>
            </div>
        </div>

        <h3 style="margin: var(--spacing-lg) 0 var(--spacing-sm) 0; font-size: 1.1rem;">Brand Impact Simulation</h3>
        <div id="impact-chart" class="card"></div>
    `;

    // Charts
    const matrixContainer = container.querySelector('#risk-matrix');
    matrixContainer.appendChild(createChartPlaceholder('Risk Map Matrix', '300px', 'Scatter plot comparing Product Sentiment vs Viral Velocity'));

    const impactContainer = container.querySelector('#impact-chart');
    impactContainer.appendChild(createChartPlaceholder('Projected Brand Sentiment Impact', '250px', 'Line chart showing scenario A (Do Nothing) vs Scenario B (Discontinue)'));

    return container;
}
