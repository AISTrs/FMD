function timeseriesChart(chartData, customLabels, title, xLabel, yLabel, containerName, extraTrace = {}, extraLayout = {}) {

    const trace = {
        x: chartData.label,
        y: chartData.value,
        mode: 'lines+markers',
        type: 'scatter',
        text: customLabels,
        name: 'Timeseries Chart',
        hoverinfo: 'text',
        marker: {
            color: 'green'
        },
        ...extraTrace
    };

    // Creating layout for the chart
    const layout = {
        title: title,
        xaxis: {
            title: xLabel
        },
        yaxis: {
            title: yLabel
        },
        hoverlabel: {
            bgcolor: 'orange',
            font: { color: 'white' }
        },
        hovermode: 'closest',
        ...extraLayout
    };

    // Plotting the chart
    Plotly.newPlot(containerName, [trace], layout);
}

function barChart(chartData, labels, title, xLabel, yLabel, containerName, extraTrace = {}, extraLayout = {}) {
    var trace = {
        x: chartData.label,
        y: chartData.value,
        mode: 'markers',
        text: labels,
        type: 'bar',
        hoverinfo: 'text',
        marker: {
            size: 8,
            color: 'green'
        },
        ...extraTrace
    };

    var layout = {
        title: title,
        xaxis: { title: xLabel },
        yaxis: { title: yLabel },
        hoverlabel: {
            bgcolor: 'orange',
            font: { color: 'white' }
        },
        hovermode: 'closest',
        ...extraLayout
    };

    Plotly.newPlot(containerName, [trace], layout);
}
