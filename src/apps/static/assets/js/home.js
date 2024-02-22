async function fetchApiJsonData(url) {
    try {
        var data = await fetch(url)
            .then(response => response.json());
        return data;
    } catch (error) {
        console.error(`There was a problem with the fetch operation: ${url}`, error);
    }
}

var fiscalData = fetchApiJsonData("/api/fiscal_data/");

var committeeExpenseData;

// function to move home layout
document.addEventListener('DOMContentLoaded', function () {

    var nav = document.getElementById('base-nav-layout');

    var homeDiv = document.getElementById('home-layout');

    var fiscalDropdown = document.getElementById("fiscal-term-drop-down");

    var startDate = document.getElementById('start-date-label');
    var endDate = document.getElementById('end-date-label');
    var tableLabel = document.getElementById('committee-table-label');

    nav.addEventListener('mouseleave', function () {
        homeDiv.style.left = '90px';
    });

    nav.addEventListener('mouseenter', function () {
        homeDiv.style.left = '200px';
    });


    fiscalData.then(data => {
        fiscalData = data;
        startDate.innerText = `Start Date: ${data[0].start_date}`;
        endDate.innerText = `Start Date: ${data[0].end_date}`;
        committeeExpenseData = fetchApiJsonData(`/api/committee_expense_data/${data[0].id}/`)
        tableLabel.innerText = `${data[0].semester} expenses budget`;
        populateTable();
        populateScatterPlot();
        data.forEach(option => {
            const newOption = document.createElement("option");
            newOption.value = option.id;
            newOption.text = option.semester;
            fiscalDropdown.add(newOption);
        });
    })


    fiscalDropdown.addEventListener('change', function () {

        startDate.innerText = `Start Date: ${fiscalData[fiscalDropdown.selectedIndex].start_date}`;
        endDate.innerText = `Start Date: ${fiscalData[fiscalDropdown.selectedIndex].end_date}`;

        committeeExpenseData = fetchApiJsonData(`/api/committee_expense_data/${fiscalDropdown.value}/`)
        populateTable();
        populateScatterPlot();
        tableLabel.innerText = `${fiscalData[fiscalDropdown.selectedIndex].semester} expenses budget`;


    });

});

function populateScatterPlot() {

    committeeExpenseData.then(data => {

        var filteredData = data.filter(item => item.usage !== null);

        var committees = filteredData.map(item => item.committee);
        var usage = filteredData.map(item => parseFloat(item.usage));

        var trace = {
            x: committees,
            y: usage,
            mode: 'markers',
            type: 'bar',
            marker: {
                size: 8,
                color: 'green'
            }
        };

        var layout = {
            title: 'Committee vs Usage',
            xaxis: { title: 'Committee' },
            yaxis: { title: 'Usage %' },
            hoverlabel: {
                bgcolor: 'orange',
                font: { color: 'white' }
            },
            hovermode: 'closest',
            hoverinfo: 'text'
        };

        Plotly.newPlot('committee-scatter-plot', [trace], layout);


    });


}


// function to populate committee table 
function populateTable() {

    var container = document.getElementById("tableContainer");

    container.innerHTML = "";

    var table = document.createElement('table');
    table.classList.add('table', 'table-bordered');

    var headerRow = document.createElement('tr');
    headerRow.classList.add('committee-table-header');


    const header = ["Committee", "Budget", "Income", "Expenses", "Net", "Usage"]
    header.forEach(key => {
        var headerCell = document.createElement('th');
        headerCell.classList.add('p-6', 'text-primary', 'p-lg-1');
        headerCell.textContent = key.charAt(0).toUpperCase() + key.slice(1); // Capitalize first letter
        headerRow.appendChild(headerCell);
    });
    table.appendChild(headerRow);

    committeeExpenseData.then(data => {

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

    });

    container.appendChild(table);

}
