document.addEventListener("DOMContentLoaded", function () {

    const tableLabel = document.getElementById('committee-table-label');

    initSemesterNavBar().then(fiscalData => {
        const fiscalDropdown = document.getElementById("fiscal-term-drop-down");

        tableLabel.innerText = `${fiscalData[fiscalDropdown.selectedIndex].semester} expenses budget`;

        fetchApiJsonData(`/api/committee_expense_data/${fiscalData[fiscalDropdown.selectedIndex].id}/`).then(data => {
            populateTable(data);
            plotBarChart(data);
        });
    });

});

// function to populate committee table 
function populateTable(data) {

    var container = document.getElementById("committee-table-container");

    container.innerHTML = "";

    var table = document.createElement('table');
    table.classList.add('table', 'table-bordered');

    var headerRow = document.createElement('tr');
    headerRow.classList.add('committee-table-header');

    const header = ["Committee", "Budget", "Income", "Expenses", "Net", "Usage"]
    header.forEach(key => {
        var headerCell = document.createElement('th');
        headerCell.classList.add('p-6', 'p-lg-1');
        headerCell.textContent = key.charAt(0).toUpperCase() + key.slice(1); // Capitalize first letter
        headerRow.appendChild(headerCell);
    });
    table.appendChild(headerRow);

    data.forEach(function (item) {
        var row = document.createElement('tr');
        row.classList.add('committee-table-row');
        for (var key in item) {
            var cell = document.createElement('td');
            cell.classList.add('p-2');
            cell.textContent = item[key];
            row.appendChild(cell);
        }
        table.appendChild(row);
    });

    container.appendChild(table);
}

function plotBarChart(data) {

    var filteredData = data.filter(item => item.usage !== null);

    var committees = filteredData.map(item => item.committee);
    var usage = filteredData.map(item => parseFloat(item.usage));

    let ctx = document.getElementById("usage-bar-chart");

    let parent = ctx.parentElement;

    ctx.width = parent.clientWidth;
    console.log(parent.clientWidth)
    ctx.height = parent.clientHeight;

    let chart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: committees,
            datasets: [
                {
                    label: "Usage %",
                    data: usage
                }
            ]
        }
    });
}