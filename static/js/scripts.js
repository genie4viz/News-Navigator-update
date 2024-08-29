document.addEventListener("DOMContentLoaded", function () {
    // Initialize state for each category
    const categoryState = {
        'World': { page: 1, articlesPerPage: 5, totalArticles: 0 },
        'Nation': { page: 1, articlesPerPage: 5, totalArticles: 0 },
        'Business': { page: 1, articlesPerPage: 5, totalArticles: 0 },
        'Technology': { page: 1, articlesPerPage: 5, totalArticles: 0 },
        'Science': { page: 1, articlesPerPage: 5, totalArticles: 0 },
        'Sports': { page: 1, articlesPerPage: 5, totalArticles: 0 }
    };

    // Fetch initial data for each category
    Object.keys(categoryState).forEach(category => {
        fetchNewsForCategory(category);
    });

    function fetchNewsForCategory(category) {
        const { page, articlesPerPage } = categoryState[category];
        fetch(`/fetch_news?category=${category.toUpperCase()}&page=${page}&perPage=${articlesPerPage}`)
            .then(response => response.json())
            .then(data => {
                updateNewsSection(category, data);
                updatePaginationControls(category, data.length);  // Check the number of articles returned
            })
            .catch(error => {
                console.error('Error fetching news:', error);
                document.querySelector('.error-message').textContent = 'Failed to load news. Please try again later.';
            });
    }

    function updateNewsSection(category, newsList) {
        const categoryMap = {
            'World': 'world-news',
            'Nation': 'nation-news',
            'Business': 'business-news',
            'Technology': 'technology-news',
            'Science': 'science-news',
            'Sports': 'sports-news'
        };

        const section = document.querySelector(`#${categoryMap[category]} ul`);

        if (section && Array.isArray(newsList)) {
            section.innerHTML = ''; // Clear current list before adding new items

            newsList.forEach(news => {
                const newsItem = `
                    <li class="news-item">
                        <a href="${news.link}" target="_blank" rel="noopener noreferrer" class="news-title" title="${news.title}">
                            ${truncateText(news.title)}
                        </a>
                        <span class="news-date">${new Date(news.pubDate).toLocaleDateString()}</span>
                    </li>
                `;
                section.innerHTML += newsItem;
            });
        }
    }

    function updatePaginationControls(category, fetchedArticlesCount) {
        const categoryMap = {
            'World': 'world-news',
            'Nation': 'nation-news',
            'Business': 'business-news',
            'Technology': 'technology-news',
            'Science': 'science-news',
            'Sports': 'sports-news'
        };

        const section = document.querySelector(`#${categoryMap[category]}`);
        let paginationControls = section.querySelector('.pagination-controls');

        if (!paginationControls) {
            paginationControls = document.createElement('div');
            paginationControls.classList.add('pagination-controls');

            const prevButton = document.createElement('button');
            prevButton.classList.add('prev-button');
            prevButton.textContent = 'Previous';
            prevButton.disabled = categoryState[category].page === 1;
            prevButton.addEventListener('click', function () {
                if (categoryState[category].page > 1) {
                    categoryState[category].page--;
                    fetchNewsForCategory(category);
                }
            });

            const nextButton = document.createElement('button');
            nextButton.classList.add('next-button');
            nextButton.textContent = 'Next';
            nextButton.addEventListener('click', function () {
                categoryState[category].page++;
                fetchNewsForCategory(category);
            });

            paginationControls.appendChild(prevButton);
            paginationControls.appendChild(nextButton);
            section.appendChild(paginationControls);
        }

        // Disable or enable the Next button based on the fetched articles count
        const nextButton = paginationControls.querySelector('.next-button');
        if (fetchedArticlesCount < categoryState[category].articlesPerPage) {
            nextButton.disabled = true;
        } else {
            nextButton.disabled = false;
        }

        // Disable or enable the Previous button based on the current page number
        const prevButton = paginationControls.querySelector('.prev-button');
        prevButton.disabled = categoryState[category].page === 1;
    }

    function truncateText(text, length = 50) {
        return text.length > length ? text.substring(0, length) + '...' : text;
    }
});
