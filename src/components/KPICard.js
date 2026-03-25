function createKPICard(title, value, trendText = null, trendType = null) {
    const card = document.createElement('div');
    card.className = 'card kpi-card';
    
    let trendHtml = '';
    if (trendText) {
        const trendClass = trendType === 'positive' ? 'kpi-trend positive' : 
                           (trendType === 'negative' ? 'kpi-trend negative' : 'kpi-trend');
        trendHtml = `<div class="${trendClass}">${trendText}</div>`;
    }

    card.innerHTML = `
        <div class="card-title">${title}</div>
        <div class="kpi-value">${value}</div>
        ${trendHtml}
    `;
    
    return card;
}
