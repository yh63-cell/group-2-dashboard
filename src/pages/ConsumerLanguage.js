function renderConsumerLanguage() {
    const container = document.createElement('div');
    container.className = 'page-container';
    
    container.innerHTML = `
        <h2 class="page-title">Consumer Language & NLP Keywords</h2>
        
        <p style="margin-bottom: var(--spacing-lg); color: var(--text-muted);">
            Displaying the most frequently used phrases and keywords extracted from reviews, social media, and support tickets via natural language processing.
        </p>

        <div class="kpi-grid" style="grid-template-columns: repeat(3, 1fr);">
            <div class="card">
                <div class="card-title">Positive Drivers</div>
                <div id="positive-tags" style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 15px;"></div>
            </div>
            
            <div class="card">
                <div class="card-title">Negative Detractors</div>
                <div id="negative-tags" style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 15px;"></div>
            </div>

            <div class="card">
                <div class="card-title">Mixed / Polarizing</div>
                <div id="mixed-tags" style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 15px;"></div>
            </div>
        </div>

        <div class="card" style="margin-top: var(--spacing-lg);">
            <div class="card-title">Phrase Co-occurrence Network</div>
            <div id="word-blob"></div>
        </div>
    `;

    // Tag clouds
    const posTagContainer = container.querySelector('#positive-tags');
    mockData.keywordTags.positive.forEach(tag => {
        posTagContainer.innerHTML += `<span class="badge" style="background: #ecfdf5; color: #047857; padding: 6px 12px;">${tag}</span>`;
    });

    const negTagContainer = container.querySelector('#negative-tags');
    mockData.keywordTags.negative.forEach(tag => {
        negTagContainer.innerHTML += `<span class="badge" style="background: #fef2f2; color: #b91c1c; padding: 6px 12px;">${tag}</span>`;
    });

    const mixTagContainer = container.querySelector('#mixed-tags');
    mockData.keywordTags.mixed.forEach(tag => {
        mixTagContainer.innerHTML += `<span class="badge" style="background: #fffbeb; color: #b45309; padding: 6px 12px;">${tag}</span>`;
    });

    // Word blob chart
    const wordBlob = container.querySelector('#word-blob');
    wordBlob.appendChild(createChartPlaceholder('Network Graph', '400px', 'Network graph linking context nodes (e.g., "battery" linked to "dies", "awful", "fix")'));

    return container;
}
