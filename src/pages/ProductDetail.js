function renderProductDetail() {
    const container = document.createElement('div');
    container.className = 'page-container';
    
    // Header with dropdown selection
    container.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--spacing-lg);">
            <h2 class="page-title" style="margin: 0;">Product Detail Analysis</h2>
            <select id="product-selector" class="card" style="padding: 8px 16px; border-color: var(--border-color); outline: none;">
                ${mockData.products.map(p => `<option value="${p.id}">${p.name}</option>`).join('')}
            </select>
        </div>
        
        <div class="kpi-grid" id="product-kpis"></div>

        <div class="chart-grid">
            <div id="product-sentiment-breakdown"></div>
            <div id="product-review-highlights" class="card">
                <div class="card-title">Latest Review Verbatims</div>
                <div class="review-list" style="margin-top: 15px; display: flex; flex-direction: column; gap: 15px;"></div>
            </div>
        </div>
    `;

    // Elements
    const selector = container.querySelector('#product-selector');
    const kpiGrid = container.querySelector('#product-kpis');
    const chartContainer = container.querySelector('#product-sentiment-breakdown');
    const reviewList = container.querySelector('.review-list');

    // Render logic
    const updateView = (productId) => {
        try {
            const product = mockData.products.find(p => p.id === productId);
            if (!product) {
                kpiGrid.innerHTML = '<div style="color:var(--danger-color)">Error: Product not found</div>';
                chartContainer.innerHTML = '';
                reviewList.innerHTML = '';
                return;
            }
            
            // Safe Reset
            kpiGrid.replaceChildren();
            chartContainer.replaceChildren();
            reviewList.replaceChildren();

            // KPIs
            kpiGrid.appendChild(createKPICard('Overall Sentiment', (product.sentimentScore || 0) + '/100'));
            kpiGrid.appendChild(createKPICard('Review Volume', (product.reviewVolume || 0).toLocaleString()));
            kpiGrid.appendChild(createKPICard('Backlash Risk Level', product.backlashRisk || 'Unknown', null, null));

            // Chart Placeholder
            chartContainer.appendChild(createChartPlaceholder('Sentiment Time Series', '400px', 'Line/Bar combination over 12 months specifically for ' + product.name));

            // Reviews
            const relevantReviews = mockData.recentComments.filter(r => r.product === productId || (r.product === 'speakers' && productId === 'speakers')); 
            
            if (relevantReviews.length === 0) {
                reviewList.innerHTML = '<p class="text-muted" style="color:var(--text-muted)">No recent reviews fetched in mock data for this selection.</p>';
            } else {
                relevantReviews.forEach(r => {
                    const el = document.createElement('div');
                    el.style.borderLeft = r.sentiment === 'Positive' ? '3px solid var(--success-color)' : (r.sentiment === 'Negative' ? '3px solid var(--danger-color)' : '3px solid var(--warning-color)');
                    el.style.padding = '10px 15px';
                    el.style.background = 'var(--bg-main)';
                    el.style.borderRadius = '0 var(--radius) var(--radius) 0';
                    
                    el.innerHTML = `
                        <div style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 5px;">
                            <strong>${r.sentiment || 'Unknown'}</strong> • Mentions: <span style="text-transform: capitalize;">${r.feature || 'general'}</span>
                        </div>
                        <div style="font-size: 0.95rem;">"${r.text || ''}"</div>
                    `;
                    reviewList.appendChild(el);
                });
            }
        } catch (e) {
            console.error(e);
            kpiGrid.innerHTML = `<div style="color:var(--danger-color)">Render Error: ${e.message}</div>`;
        }
    };

    // Initial render
    // Use App state selectedProduct if possible, else default
    const initialProduct = mockData.products.length > 0 ? mockData.products[0].id : ''; 
    selector.value = initialProduct;
    updateView(initialProduct);

    // Listener
    selector.addEventListener('change', (e) => {
        updateView(e.target.value);
    });

    return container;
}
