document.addEventListener("DOMContentLoaded", () => {
    // ----------------------------------------------------
    // Table Interaction Logic
    // ----------------------------------------------------
    const searchInput = document.getElementById("searchInput");
    const filterCategory = document.getElementById("filterCategory");
    const filterAuth = document.getElementById("filterAuth");
    const tableBody = document.getElementById("tableBody");
    const rows = Array.from(tableBody.getElementsByTagName("tr"));

    // Populate dropdowns
    const categories = new Set();
    const auths = new Set();

    rows.forEach(row => {
        const cells = row.getElementsByTagName("td");
        if(cells.length > 3) {
            categories.add(cells[1].innerText.trim());
            auths.add(cells[3].innerText.trim());
        }
    });

    categories.forEach(cat => {
        if(cat && cat !== "-") {
            const option = document.createElement("option");
            option.value = cat;
            option.innerText = cat;
            filterCategory.appendChild(option);
        }
    });

    auths.forEach(auth => {
        if(auth && auth !== "-") {
            const option = document.createElement("option");
            option.value = auth;
            option.innerText = auth;
            filterAuth.appendChild(option);
        }
    });

    // Filter function
    const applyFilters = () => {
        const query = searchInput.value.toLowerCase();
        const catFilter = filterCategory.value;
        const authFilter = filterAuth.value;

        rows.forEach(row => {
            const cells = row.getElementsByTagName("td");
            if(cells.length > 3) {
                const text = row.innerText.toLowerCase();
                const cat = cells[1].innerText.trim();
                const auth = cells[3].innerText.trim();

                const matchesSearch = text.includes(query);
                const matchesCat = catFilter === "" || cat === catFilter;
                const matchesAuth = authFilter === "" || auth === authFilter;

                if (matchesSearch && matchesCat && matchesAuth) {
                    row.style.display = "";
                } else {
                    row.style.display = "none";
                }
            }
        });
    };

    if(searchInput) searchInput.addEventListener("input", applyFilters);
    if(filterCategory) filterCategory.addEventListener("change", applyFilters);
    if(filterAuth) filterAuth.addEventListener("change", applyFilters);

    // ----------------------------------------------------
    // Mermaid Initialization
    // ----------------------------------------------------
    if (window.mermaid) {
        mermaid.initialize({ startOnLoad: true, theme: 'default' });
    }

    // ----------------------------------------------------
    // Chart.js Logic
    // ----------------------------------------------------
    if (window.CHART_DATA && typeof Chart !== "undefined") {
        const data = window.CHART_DATA;

        // Helper function to create charts
        const createChart = (canvasId, type, chartData, title) => {
            const ctx = document.getElementById(canvasId);
            if (!ctx) return;
            
            const labels = Object.keys(chartData);
            const values = Object.values(chartData);

            new Chart(ctx, {
                type: type,
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Count',
                        data: values,
                        backgroundColor: [
                            '#000000',
                            '#4b5563',
                            '#9ca3af',
                            '#d1d5db',
                            '#e5e7eb',
                            '#f3f4f6'
                        ],
                        borderWidth: 1,
                        borderColor: '#ffffff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: type === 'doughnut' || type === 'pie',
                            position: 'right'
                        }
                    },
                    scales: (type === 'bar') ? {
                        y: {
                            beginAtZero: true,
                            ticks: { precision: 0 }
                        }
                    } : {}
                }
            });
        };

        // Render the 4 requested charts
        createChart('authChart', 'doughnut', data.authentication || {}, 'Authentication');
        createChart('apiChart', 'bar', data.api_types || {}, 'API Types');
        createChart('categoryChart', 'bar', data.categories || {}, 'Categories');
        createChart('buildChart', 'doughnut', data.buildability || {}, 'Buildability');
    }
});

// Global sorting function
let sortDirection = false;
function sortTable(columnIndex) {
    const tableBody = document.getElementById("tableBody");
    const rows = Array.from(tableBody.getElementsByTagName("tr"));

    sortDirection = !sortDirection;

    rows.sort((a, b) => {
        const cellA = a.getElementsByTagName("td")[columnIndex]?.innerText || "";
        const cellB = b.getElementsByTagName("td")[columnIndex]?.innerText || "";
        
        // Handle numeric sorting for Confidence column
        if (columnIndex === 10) {
            const valA = parseFloat(cellA) || 0;
            const valB = parseFloat(cellB) || 0;
            return sortDirection ? valA - valB : valB - valA;
        }

        return sortDirection ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
    });

    rows.forEach(row => tableBody.appendChild(row));
}
