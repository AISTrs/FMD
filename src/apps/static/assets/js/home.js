var committeeExpenseData;

function semesterNavBarCallback(data, selectedIndex) {
    var tableLabel = document.getElementById('committee-table-label');

    committeeExpenseData = fetchApiJsonData(`/api/committee_expense_data/${data[selectedIndex].id}/`)
    tableLabel.innerText = `${data[selectedIndex].semester} expenses budget`;
    populateTable();
    populateScatterPlot();
}

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
        headerCell.classList.add('p-6', 'p-lg-1');
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
