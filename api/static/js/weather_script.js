function renderAqiChart(airqualityData) {
    const labels = airqualityData.map(forecast => new Date(forecast.time * 1000).toLocaleString());
    const values = airqualityData.map(forecast => forecast.avg_aqi);
    const ctx = document.getElementById('airQualityChart').getContext('2d');

    // Calculate gradient stops based on data
    function calculateGradientStops(minAqi, maxAqi) {
        const aqiLimits = {good: 1, fair: 2, moderate: 3, poor: 4, veryPoor: 5};
        const aqiColors = {
            good: 'rgba(110, 235, 152, 0.5)',
            fair: 'rgba(228, 232, 21, 0.5)',
            moderate: 'rgba(247, 185, 52, 0.5)',
            poor: 'rgba(235, 50, 40, 0.5)',
            veryPoor: 'rgba(97, 30, 26, 0.5)'
        };

        const stops = [];
        Object.keys(aqiLimits).forEach((key, index, array) => {
            if (minAqi <= aqiLimits[key] && maxAqi >= aqiLimits[key]) {
                let nextLimit = aqiLimits[array[index + 1]] || maxAqi;
                let stopPosition = (aqiLimits[key] - minAqi) / (maxAqi - minAqi);
                let nextStopPosition = (nextLimit - minAqi) / (maxAqi - minAqi);
                stops.push({stop: stopPosition, color: aqiColors[key]});
                if (index === array.length - 1 || nextStopPosition > 1) {
                    stops.push({stop: nextStopPosition, color: aqiColors[key]});
                }
            }
        });
        return stops;
    }

    // Get the min and max AQI values
    const minAqiValue = Math.min(...values);
    const maxAqiValue = Math.max(...values);

    // Create gradient
    let gradientStops = calculateGradientStops(minAqiValue, maxAqiValue);
    let gradient = ctx.createLinearGradient(0, ctx.canvas.clientHeight, 0, 0);
    gradientStops.forEach(stop => {
        // gradient.addColorStop(stop.stop, stop.color);
        console.log(`Adding color stop: ${stop.stop}, ${stop.color}`); // Log the stop position and color
        if (stop.stop < 0 || stop.stop > 1) {
            console.error(`Invalid stop position: ${stop.stop}, color: ${stop.color}`);
        } else {
            gradient.addColorStop(stop.stop, stop.color);
        }
    });

    const aqiChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                label: 'Air quality',
                borderColor: 'black',
                borderWidth: 2,
            }],
        },
        options: {
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        min: 1,
                        max: 5,
                        stepSize: 1,
                        callback: function(value) {
                            switch (value) {
                                case 1: return 'Good';
                                case 2: return 'Fair';
                                case 3: return 'Moderate';
                                case 4: return 'Poor';
                                case 5: return 'Very Poor';
                                default: return '';
                            }
                        }
                    }
                },
                x: {
                    display: false
                }
            },
            plugins:{
                legend: {
                    display: true
                }
            },
            elements: {
                point: {
                    radius: 0
                },
                line: {
                    tension: 0.5
                }
            },
            responsive: true,
            maintainAspectRatio: true
        },
        plugins: [{
            beforeDraw: (chart) => {
                const ctx = chart.ctx;
                const chartArea = chart.chartArea;
                ctx.save();
                ctx.globalCompositeOperation = 'destination-over';
                ctx.fillStyle = gradient;
                ctx.fillRect(chartArea.left, chartArea.top, chartArea.right - chartArea.left, chartArea.bottom - chartArea.top);
                ctx.restore();
            }
        }]
    });
}
renderAqiChart(airquality_forecast);