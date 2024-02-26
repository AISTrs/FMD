document.addEventListener("DOMContentLoaded", function () {

    const rawData = [
        { date: '2022-01-01', value: 10 },
        { date: '2022-01-02', value: 15 },
        { date: '2022-01-03', value: 13 },
        { date: '2022-01-04', value: 17 },
        { date: '2022-01-05', value: 10 }
          ];
  
      // Create initial chart with daily data
      const initialData = aggregateData(rawData, 'day');
      const layout = { title: 'Time Series Chart with Grouping' };
      Plotly.newPlot('time-series-chart', initialData, layout);

});
