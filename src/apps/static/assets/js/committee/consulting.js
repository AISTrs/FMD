
var committeeTransactionData;

function semesterNavBarCallback(data, selectedIndex) {
    committeeTransactionData = fetchApiJsonData(`/api/consulting/${data[selectedIndex].id}`);
    committeeTransactionData.then(data => {

        // Extracting dates and amounts
        const dates = data.map(item => item.date);
        const amounts = data.map(item => item.amount);

        const interval = 'month';

        var chartData = aggregateTimeseriesData({ "date": dates, "value": amounts }, interval);

        var customLabels = chartData.date.map((date, index) => `Date: ${date}<br>Amount: $${chartData.aggregateValue[index].toFixed(2)}`);

        timeseriesChart({
            "label": chartData.date,
            "value": chartData.aggregateValue
        }, customLabels, "Timeseries chart of Consulting", interval, 'Amount ($)', 'time-series-chart', {},
            {

                height: 390,
                margin: {
                    r: 20,
                    l: 60,
                    t: 50,
                    b: 50
                }
            });

        customLabels = chartData.date.map((date, index) => `Date: ${date}<br>Amount: $${chartData.value[index].toFixed(2)}`);

        barChart({
            "label": chartData.date,
            "value": chartData.value
        }, customLabels, "Bar Chart of Consulting", interval, 'Amount ($)', 'bar-chart', {},
            {

                height: 390,
                margin: {
                    r: 20,
                    l: 60,
                    t: 50,
                    b: 50
                }
            });

    })
}


