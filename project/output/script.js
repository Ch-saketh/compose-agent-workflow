document.addEventListener("DOMContentLoaded", () => {
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
});

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
