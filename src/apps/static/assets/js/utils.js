function aggregateTimeseriesData(data, interval) {
    var dates = data.date;
    var values = data.value;

    var aggregatedDates = [];
    var aggregatedValues = [];
    var aggregatedSums = [];

    var currentIntervalDate = dates[0];
    var intervalTotal = 0;
    var sumTotal = 0;

    for(let i = 0; i < dates.length; i++) {
        if (interval === 'day' && currentIntervalDate !== dates[i]) {
            aggregatedDates.push(formatDate(currentIntervalDate, interval));
            aggregatedValues.push(intervalTotal);
            aggregatedSums.push(sumTotal);
            aggregatedSums
            currentIntervalDate = dates[i];
            intervalTotal = values[i];
        } else if (interval === 'week' && getWeek(dates[i]) !== getWeek(currentIntervalDate)) {
            aggregatedDates.push(formatDate(currentIntervalDate, interval));
            aggregatedValues.push(intervalTotal);
            aggregatedSums.push(sumTotal);
            currentIntervalDate = dates[i];
            intervalTotal = values[i];
        } else if (interval === 'month' && getMonth(dates[i]) !== getMonth(currentIntervalDate)) {
            aggregatedDates.push(formatDate(currentIntervalDate, interval));
            aggregatedValues.push(intervalTotal);
            aggregatedSums.push(sumTotal);
            currentIntervalDate = dates[i];
            intervalTotal = values[i];
        } else {
            intervalTotal += values[i];
        }
        sumTotal += values[i];
    }

    aggregatedDates.push(formatDate(currentIntervalDate, interval));
    aggregatedValues.push(intervalTotal);
    aggregatedSums.push(sumTotal);

    return {
        "date" : aggregatedDates,
        "value" : aggregatedValues,
        "aggregateValue" : aggregatedSums,
    }
}

// Function to get week number from date
function getWeek(date) {
    const d = new Date(date);
    d.setHours(0, 0, 0, 0);
    d.setDate(d.getDate() + 3 - (d.getDay() + 6) % 7);
    const week1 = new Date(d.getFullYear(), 0, 4);
    return 1 + Math.round(((d - week1) / 86400000 - 3 + (week1.getDay() + 6) % 7) / 7);
}

// Function to get month from date
function getMonth(date) {
    return new Date(date).getMonth();
}

function formatDate(date, format) {
    const d = new Date(date);
    const year = d.getUTCFullYear();
    const month = (d.getUTCMonth() + 1).toString().padStart(2, '0');
    const day = d.getUTCDate().toString().padStart(2, '0');
    if (format === 'day') {
        return `${year}-${month}-${day}`;
    } else if (format === 'week') {
        const week = getWeek(date).toString().padStart(2, '0');
        return `${year}-w${week}`;
    } else if (format === 'month') {
        return `${year}-${month}`;
    } else {
        return date; 
    }
}