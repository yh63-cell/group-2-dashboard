function createSentimentTable(data, columns) {
    const container = document.createElement('div');
    container.className = 'card table-card';
    container.innerHTML = `<div class="table-container"><table><thead><tr></tr></thead><tbody></tbody></table></div>`;
    
    const theadTr = container.querySelector('thead tr');
    const tbody = container.querySelector('tbody');

    // Headers
    columns.forEach(col => {
        const th = document.createElement('th');
        th.textContent = col.label;
        theadTr.appendChild(th);
    });

    // Rows
    data.forEach(row => {
        const tr = document.createElement('tr');
        
        columns.forEach(col => {
            const td = document.createElement('td');
            const val = row[col.key];
            
            // Special formatting for Risk Badges
            if (col.key === 'backlashRisk') {
                const badgeClass = val === 'Low' ? 'badge-low' : (val === 'Medium' ? 'badge-medium' : 'badge-high');
                td.innerHTML = `<span class="badge ${badgeClass}">${val} Risk</span>`;
            } else if (col.key === 'sentimentScore') {
                // Color text based on score
                const color = val > 75 ? 'var(--success-color)' : (val < 50 ? 'var(--danger-color)' : 'var(--warning-color)');
                td.innerHTML = `<strong style="color: ${color}">${val}/100</strong>`;
            } else {
                td.textContent = val;
            }
            tr.appendChild(td);
        });
        
        tbody.appendChild(tr);
    });

    return container;
}
