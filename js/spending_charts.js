$(document).ready(function () {
    $.getJSON("data.json", function (party_ad_data) {
        let spendChartConfig = {
            type: "line",
            data: {
                labels: party_ad_data.dates,
                datasets: []
            },
            options: {
                responsive: true,
                title: {
                    display: true,
                    text: "Average (Estimated) Spending over Time per Party",
                    fontSize: 18,
                },
                legend: {
                    position: 'bottom',
                },
                scales: {
                    xAxes: [{
                        type: "time",
                    }],
                    yAxes: [{
                        ticks: {
                            callback: function (value, index, values) {
                                return "€" + value.toFixed(2).toString();
                            }
                        }
                    }]
                },
                tooltips: {
                    intersect: false,
                    callbacks: {
                        label: function (tooltipItems, data) {
                            return "€" + tooltipItems.yLabel.toFixed(2).toString();
                        }
                    }
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
            }
        };
        let totalSpendChartConfig = {
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
                    text: "Total (Estimated) Spending per Party",
                    fontSize: 18,
                },
                legend: {
                    position: 'bottom',
                },
                tooltips: {
                    callbacks: {
                        label: function (tooltipItem, data) {
                            return "€" + data.datasets[0].data[tooltipItem.datasetIndex].toFixed(2).toString();
                        }
                    }
                },
            }
        };

        for (let party in party_ad_data.parties) {
            spendChartConfig.data.datasets.push(
                {
                    label: party,
                    data: party_ad_data.parties[party].spending_data,
                    fill: false,
                    backgroundColor: party_ad_data.parties[party].color,
                    borderColor: party_ad_data.parties[party].color,
                    pointRadius: 0,
                    borderWidth: 2,
                });

            totalSpendChartConfig.data.labels.push(party);
            totalSpendChartConfig.data.datasets[0].data.push(party_ad_data.parties[party].total_spending)
            totalSpendChartConfig.data.datasets[0].backgroundColor.push(party_ad_data.parties[party].color)
        }

        new Chart($("#spend_per_day_chart"), spendChartConfig);
        new Chart($("#total_spend_chart"), totalSpendChartConfig);
        $('#total-spending').text("€" + party_ad_data.total_spending.toFixed(2).toString());

    });

});