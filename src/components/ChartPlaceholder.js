function createChartPlaceholder(title, height = '300px', description = 'Chart goes here') {
    const container = document.createElement('div');
    container.className = 'card chart-card';
    
    container.innerHTML = `
        <div class="card-title">${title}</div>
        <div class="chart-placeholder" style="height: ${height};">
            <div>
                <i class="fa-solid fa-chart-line" style="font-size: 2rem; margin-bottom: 10px; display: block; text-align: center;"></i>
                <p>[Placeholder] ${description}</p>
                <p style="font-size: 0.75rem; text-align: center; margin-top: 5px;">(Plug real viz library here)</p>
            </div>
        </div>
    `;
    
    return container;
}
