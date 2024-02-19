async function fetchApiJsonData(url) {
    try {
        var data = await fetch(url)
            .then(response => response.json());
        return data;
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

var fiscalData = fetchApiJsonData("/api/fiscal_data/");


// function to move home layout
document.addEventListener('DOMContentLoaded', function () {

    var nav = document.getElementById('base-nav-layout');

    var homeDiv = document.getElementById('home-layout');

    var fiscalDropdown = document.getElementById("fiscal-term-drop-down");

    var startDate = document.getElementById('start-date-label');
    var endDate = document.getElementById('end-date-label');

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
        populateTable(data[0].id);
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

        populateTable(fiscalDropdown.value);

    });

});


// function to populate committee table 
function populateTable(fiscal_id) {

    var container = document.getElementById("tableContainer");

    // Create a table element
    var table = document.createElement('table');
    table.classList.add('table', 'table-bordered');

    // Create table header
    var headerRow = document.createElement('tr');
    headerRow.classList.add('committee-table-header');


    const header = ["Committee", "Budget", "Expenses", "Income", "Net", "Usage"]
    header.forEach(key => {
        var headerCell = document.createElement('th');
        headerCell.classList.add('p-2', 'text-primary');
        headerCell.textContent = key.charAt(0).toUpperCase() + key.slice(1); // Capitalize first letter
        headerRow.appendChild(headerCell);
    });
    table.appendChild(headerRow);

    // Create table rows and cells

    fetchApiJsonData(`/api/committee_expense_data/${fiscal_id}/`)
        .then(data => {

            console.log(data);

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



    // Append the table to the container
    container.appendChild(table);

}
