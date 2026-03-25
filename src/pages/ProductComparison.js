function renderProductComparison() {
    const container = document.createElement('div');
    container.className = 'page-container';
    
    container.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--spacing-lg);">
            <h2 class="page-title" style="margin: 0;">Product Comparison</h2>
            <select class="card" style="padding: 8px 16px; border-color: var(--border-color); outline: none;">
                <option>All Regions</option>
                <option>North America</option>
                <option>Europe</option>
                <option>Asia Pacific</option>
            </select>
        </div>
        
        <div class="chart-grid" style="grid-template-columns: 1fr;">
            <div id="comparison-chart"></div>
        </div>

        <h3 style="margin: var(--spacing-lg) 0 var(--spacing-sm) 0; font-size: 1.1rem;">Detailed Metrics</h3>
        <div id="comparison-table"></div>
    `;

    // Populate Chart
    const chartContainer = container.querySelector('#comparison-chart');
    chartContainer.appendChild(createChartPlaceholder('Cross-Product Sentiment & Volume', '400px', 'Bubble chart (X=Sentiment, Y=Review Volume, Size=Revenue)'));

    // Populate Table
    const tableContainer = container.querySelector('#comparison-table');
    const cols = [
        { key: 'name', label: 'Product Category' },
        { key: 'sentimentScore', label: 'Sentiment (0-100)' },
        { key: 'reviewVolume', label: 'Mentions' },
        { key: 'revenue', label: 'Est. Revenue' },
        { key: 'trend', label: 'YoY Growth' },
        { key: 'backlashRisk', label: 'Backlash Risk' }
    ];
    tableContainer.appendChild(createSentimentTable(mockData.products, cols));

    return container;
}
