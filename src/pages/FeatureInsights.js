function renderFeatureInsights() {
    const container = document.createElement('div');
    container.className = 'page-container';
    
    container.innerHTML = `
        <h2 class="page-title">Feature Level Insights</h2>
        
        <div class="chart-grid">
            <div id="feature-radar"></div>
            <div id="feature-driver-table" class="card">
                <div class="card-title">Key Negative Drivers</div>
                <div style="margin-top: 15px;">
                    <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid var(--border-color);">
                        <span><strong>#1 Battery Defect</strong> (Speakers)</span>
                        <span style="color: var(--danger-color); font-weight: 600;">-45%</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid var(--border-color);">
                        <span><strong>#2 Price/Value Ratio</strong> (Smartwatches)</span>
                        <span style="color: var(--danger-color); font-weight: 600;">-22%</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 10px 0;">
                        <span><strong>#3 Discomfort</strong> (Headphones)</span>
                        <span style="color: var(--warning-color); font-weight: 600;">-12%</span>
                    </div>
                </div>
            </div>
        </div>

        <h3 style="margin: var(--spacing-lg) 0 var(--spacing-sm) 0; font-size: 1.1rem;">Feature Ratings Matrix</h3>
        <div id="feature-matrix" class="card table-container">
            <table>
                <thead>
                    <tr>
                        <th>Product</th>
                        <th>Battery</th>
                        <th>Sound Quality</th>
                        <th>Price/Value</th>
                        <th>Comfort</th>
                        <th>Durability</th>
                    </tr>
                </thead>
                <tbody>
                    ${Object.entries(mockData.featureInsights).map(([productId, features]) => {
                        const productName = mockData.products.find(p => p.id === productId).name;
                        return `
                            <tr>
                                <td style="font-weight: 500;">${productName}</td>
                                ${Object.values(features).map(score => `
                                    <td><span style="color: ${score > 75 ? 'var(--success-color)' : (score < 50 ? 'var(--danger-color)' : 'var(--warning-color)')}; font-weight: 600;">${score}</span></td>
                                `).join('')}
                            </tr>
                        `;
                    }).join('')}
                </tbody>
            </table>
        </div>
    `;

    // Populate Radar Chart
    const radarContainer = container.querySelector('#feature-radar');
    radarContainer.appendChild(createChartPlaceholder('Feature Distribution Analysis', '350px', 'Radar/Spider chart plotting all 5 features across 4 products'));

    return container;
}
