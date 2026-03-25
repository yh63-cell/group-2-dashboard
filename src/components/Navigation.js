const Navigation = {
    init(pageList, initialPage) {
        const sidebar = document.getElementById('sidebar');
        
        // Header
        const header = document.createElement('div');
        header.className = 'sidebar-header';
        header.innerHTML = '<h2>OmniTech</h2>';
        sidebar.appendChild(header);

        // Nav List
        const navList = document.createElement('ul');
        navList.className = 'nav-links';
        navList.id = 'nav-links';

        const icons = {
            'Overview': 'fa-solid fa-chart-pie',
            'Product Comparison': 'fa-solid fa-scale-balanced',
            'Feature Insights': 'fa-solid fa-magnifying-glass-chart',
            'Product Detail': 'fa-solid fa-box-open',
            'Backlash Risk': 'fa-solid fa-triangle-exclamation',
            'Consumer Language': 'fa-solid fa-comments',
            'Recommendation': 'fa-solid fa-lightbulb'
        };

        pageList.forEach(page => {
            const li = document.createElement('li');
            li.className = 'nav-item';
            li.dataset.page = page;
            if (page === initialPage) li.classList.add('active');
            
            li.innerHTML = `
                <i class="${icons[page] || 'fa-solid fa-circle'}"></i>
                <span>${page}</span>
            `;
            
            li.addEventListener('click', () => {
                App.navigate(page);
            });
            
            navList.appendChild(li);
        });

        sidebar.appendChild(navList);
    },

    setActive(pageName) {
        const items = document.querySelectorAll('.nav-item');
        items.forEach(item => {
            if (item.dataset.page === pageName) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
    }
};
