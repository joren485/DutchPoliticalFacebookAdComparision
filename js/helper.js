function addPercentageToDoughnutLabel(tooltipItem, data) {
    let dataset = data.datasets[tooltipItem.datasetIndex];
    let total = dataset._meta[Object.keys(dataset._meta)[0]].total;
    let current_value = dataset.data[tooltipItem.index];
    let percentage = (current_value / total * 100).toFixed(2);
    return current_value.toFixed(2) + " (" + percentage + "%)";
}

function generateLineGraphConfig(party_ad_data, title, data_key) {
    let graphConfig = {
        type: "line",
        data: {
            labels: party_ad_data.dates,
            datasets: []
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: title,
                fontSize: 18,
            },
            legend: {
                position: 'bottom',
            },
            scales: {
                xAxes: [{
                    type: "time",
                }],
            },
            plugins: {
                zoom: {
                    pan: {
                        enabled: true,
                    },
                    zoom: {
                        enabled: true,
                        drag: false,
                    }
                }
            },
        },
    };

    for (let party in party_ad_data.parties) {
        graphConfig.data.datasets.push(
            {
                label: party,
                data: party_ad_data.parties[party][data_key],
                fill: false,
                backgroundColor: party_ad_data.parties[party].color,
                borderColor: party_ad_data.parties[party].color,
                pointRadius: 0,
                borderWidth: 2,
            });
    }

    return graphConfig;
}

function generateDoughnutChart(party_ad_data, title, data_key) {
    let chartConfig = {
        type: 'doughnut',
        data: {
            labels: [],
            datasets: [{
                data: [],
                backgroundColor: [],
            }]
        },
        options: {
            maintainAspectRatio: false,
            responsive: true,
            title: {
                display: true,
                text: title,
                fontSize: 18,
            },
            legend: {
                position: 'bottom',
            },
            tooltips: {
                callbacks: {
                    label: addPercentageToDoughnutLabel,
                    title: function (tooltipItem, data) {
                        return data.labels[tooltipItem[0].index];
                    }
                }
            },
        }
    };

    for (let party in party_ad_data.parties) {
        chartConfig.data.labels.push(party);
        chartConfig.data.datasets[0].data.push(party_ad_data.parties[party][data_key])
        chartConfig.data.datasets[0].backgroundColor.push(party_ad_data.parties[party].color)
    }

    return chartConfig;

}