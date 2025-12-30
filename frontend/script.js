const API_BASE = "http://127.0.0.1:8000/movies";

function getLimitValue() {
    const input = document.getElementById("limitInput");
    const value = parseInt(input.value, 10);

    if (isNaN(value) || value < 1) {
        return 10;
    }

    return Math.min(value, 50);
}

function renderTable(data) {
    if (!data.length) {
        document.getElementById("output").innerHTML = "<p>No data available</p>";
        return;
    }

    const headers = Object.keys(data[0]);
    let html = "<table><thead><tr>";

    // Add serial number header
    html += "<th>#</th>";

    headers.forEach(h => {
        html += `<th>${h}</th>`;
    });

    html += "</tr></thead><tbody>";

    data.forEach((row, index) => {
        html += "<tr>";

        // Serial number column
        html += `<td>${index + 1}</td>`;

        headers.forEach(h => {
            html += `<td>${row[h]}</td>`;
        });

        html += "</tr>";
    });

    html += "</tbody></table>";
    document.getElementById("output").innerHTML = html;
}

async function fetchAndRender(endpoint) {
    const response = await fetch(`${API_BASE}${endpoint}`);
    const json = await response.json();
    renderTable(json.results);
}

function loadMostPopular() {
    const limit = getLimitValue();
    fetchAndRender(`/most-popular?limit=${limit}`);
}

function loadTopRated() {
    const limit = getLimitValue();
    fetchAndRender(`/top-rated?limit=${limit}`);
}

function loadByGenre() {
    fetchAndRender("/by-genre");
}

function loadYearlyTrends() {
    fetchAndRender("/yearly-trends");
}

function loadLanguageStats() {
    fetchAndRender("/language-stats");
}