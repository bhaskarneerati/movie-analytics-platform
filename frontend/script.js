/**
 * Movie Analytics Platform - Frontend Logic
 */

const API_BASE = "http://127.0.0.1:8000/api/v1/movies";

const MovieUI = {
    // Current state
    activeEndpoint: null,

    /**
     * Get the limit value from input
     */
    getLimit() {
        const input = document.getElementById("limitInput");
        let val = parseInt(input.value, 10);
        if (isNaN(val) || val < 1) val = 10;
        return Math.min(val, 50);
    },

    /**
     * Show loading spinner
     */
    showLoading() {
        const output = document.getElementById("output");
        output.innerHTML = '<div class="loader"></div>';
    },

    /**
     * Main data loading orchestration
     */
    async loadData(type) {
        this.activeEndpoint = type;
        this.updateUIState(type);
        this.showLoading();

        let url = `${API_BASE}/${type}`;
        if (this.isRankedType(type)) {
            url += `?limit=${this.getLimit()}`;
        }

        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

            const data = await response.json();
            this.render(data.results);
        } catch (error) {
            console.error("Fetch error:", error);
            this.renderError(error.message);
        }
    },

    /**
     * Update UI states (buttons and visibility)
     */
    updateUIState(type) {
        // Update Buttons
        const buttons = document.querySelectorAll('.button-group button');
        buttons.forEach(btn => {
            btn.classList.remove('active');
            if (btn.id.includes(type.split('-').pop())) {
                btn.classList.add('active');
            }
        });

        // Toggle Limit Input Visibility
        const limitGroup = document.getElementById('limit-input-group');
        if (this.isRankedType(type)) {
            limitGroup.style.display = 'flex';
            limitGroup.style.opacity = '1';
        } else {
            limitGroup.style.display = 'none';
        }
    },

    /**
     * Check if the category supports limiting
     */
    isRankedType(type) {
        return type === 'most-popular' || type === 'top-rated';
    },

    /**
     * Render the data into a premium table
     */
    render(data) {
        const output = document.getElementById("output");

        if (!data || data.length === 0) {
            output.innerHTML = '<div class="empty-state"><p>No data found for this period.</p></div>';
            return;
        }

        const keys = Object.keys(data[0]);

        let html = `
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            ${keys.map(k => `<th>${this.formatHeader(k)}</th>`).join('')}
                        </tr>
                    </thead>
                    <tbody>
                        ${data.map((row, idx) => `
                            <tr>
                                <td>${idx + 1}</td>
                                ${keys.map(k => `<td>${this.formatValue(k, row[k])}</td>`).join('')}
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;

        output.innerHTML = html;
    },

    /**
     * Format header names for display
     */
    formatHeader(key) {
        return key.replace(/_/g, ' ').toUpperCase();
    },

    /**
     * Format values based on data type (e.g., adding pills for ratings)
     */
    formatValue(key, value) {
        if (key.includes('rating') || key.includes('average')) {
            return `<span class="rating-pill">${Number(value).toFixed(2)}</span>`;
        }
        if (key === 'popularity') {
            return `<span class="popularity-score">${Number(value).toLocaleString()}</span>`;
        }
        if (key === 'vote_count' || key === 'movie_count') {
            return `<strong>${Number(value).toLocaleString()}</strong>`;
        }
        return value;
    },

    /**
     * Render error state
     */
    renderError(msg) {
        const output = document.getElementById("output");
        output.innerHTML = `
            <div class="empty-state">
                <p style="color: #f85149;">⚠️ <strong>Error:</strong> ${msg}</p>
                <small>Make sure the API server is running at ${API_BASE}</small>
            </div>
        `;
    }
};