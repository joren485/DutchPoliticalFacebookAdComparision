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
                }
            }
        };

        let impressionsChartConfig = {
            type: "line",
            data: {
                labels: party_ad_data.dates,
                datasets: []
            },
            options: {
                responsive: true,
                title: {
                    display: true,
                    text: "Average Estimated Impressions per Day",
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
                tooltips: {
                    intersect: false,
                    callbacks: {
                        label: function (tooltipItems, data) {
                            return Math.round(tooltipItems.yLabel);
                        }
                    }
                }
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
                }
            }
        };

        let totalImpressionsChartConfig = {
            type: 'doughnut',
            data: {
                labels: [],
                datasets: [{
                    data: [],
                    backgroundColor: [],
                }]
            },
            options: {
                responsive: true,
                title: {
                    display: true,
                    text: "Total (Estimated) Impressions per Party",
                    fontSize: 18,
                },
                legend: {
                    position: 'bottom',
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

            impressionsChartConfig.data.datasets.push(
                {
                    label: party,
                    data: party_ad_data.parties[party].impressions_data,
                    fill: false,
                    backgroundColor: party_ad_data.parties[party].color,
                    borderColor: party_ad_data.parties[party].color,
                    pointRadius: 0,
                    borderWidth: 2,
                });


            totalSpendChartConfig.data.labels.push(party);
            totalSpendChartConfig.data.datasets[0].data.push(party_ad_data.parties[party].total_spending)
            totalSpendChartConfig.data.datasets[0].backgroundColor.push(party_ad_data.parties[party].color)

            totalImpressionsChartConfig.data.labels.push(party);
            totalImpressionsChartConfig.data.datasets[0].data.push(party_ad_data.parties[party].total_impressions)
            totalImpressionsChartConfig.data.datasets[0].backgroundColor.push(party_ad_data.parties[party].color)
        }

        let spend_chart_context = $("#spend_per_day_chart");
        let spend_chart = new Chart(spend_chart_context, spendChartConfig);

        let total_spend_chart_context = $("#total_spend_chart");
        let total_spend_chart = new Chart(total_spend_chart_context, totalSpendChartConfig);

        let impressions_chart_context = $("#impressions_per_day_chart");
        let impressions_chart = new Chart(impressions_chart_context, impressionsChartConfig);

        let total_impressions_chart_context = $("#total_impressions_chart");
        let total_impressions_chart = new Chart(total_impressions_chart_context, totalImpressionsChartConfig);

        $('#total-spending').text("€" + party_ad_data.total_spending.toFixed(2).toString());
    });
});