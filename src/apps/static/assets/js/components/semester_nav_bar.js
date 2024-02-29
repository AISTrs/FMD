async function initSemesterNavBar() {
    const fiscalData = await fetchApiJsonData("/api/fiscal_data/").then(data => data);
    populateSemesterNavBar(fiscalData);

    return fiscalData
}

// function to populate semester nav Bar
function populateSemesterNavBar(data) {

    const fiscalDropdown = document.getElementById("fiscal-term-drop-down");

    const startDate = document.getElementById('start-date-label');
    const endDate = document.getElementById('end-date-label');

    startDate.innerText = `Start Date: ${data[0].start_date}`;
    endDate.innerText = `End Date: ${data[0].end_date}`;
    data.forEach(option => {
        const newOption = document.createElement("option");
        newOption.value = option.id;
        newOption.text = option.semester;
        fiscalDropdown.add(newOption);
    });

    fiscalDropdown.addEventListener('change', function () {
        startDate.innerText = `Start Date: ${data[fiscalDropdown.selectedIndex].start_date}`;
        endDate.innerText = `End Date: ${data[fiscalDropdown.selectedIndex].end_date}`;
    });
}