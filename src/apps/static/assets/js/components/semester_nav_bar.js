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

// function to populate semester nav Bar
document.addEventListener('DOMContentLoaded', function () {

    var fiscalDropdown = document.getElementById("fiscal-term-drop-down");

    var startDate = document.getElementById('start-date-label');
    var endDate = document.getElementById('end-date-label');

    fiscalData.then(data => {
        fiscalData = data;
        startDate.innerText = `Start Date: ${data[0].start_date}`;
        endDate.innerText = `Start Date: ${data[0].end_date}`;
        data.forEach(option => {
            const newOption = document.createElement("option");
            newOption.value = option.id;
            newOption.text = option.semester;
            fiscalDropdown.add(newOption);
        });

        semesterNavBarCallback(data, 0);
    })

    fiscalDropdown.addEventListener('change', function () {

        startDate.innerText = `Start Date: ${fiscalData[fiscalDropdown.selectedIndex].start_date}`;
        endDate.innerText = `Start Date: ${fiscalData[fiscalDropdown.selectedIndex].end_date}`;

        semesterNavBarCallback(fiscalData, fiscalDropdown.selectedIndex);
    });

});