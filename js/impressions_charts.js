$(document).ready(function () {
    $.getJSON("data.json", function (party_ad_data) {
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
                maintainAspectRatio: false,
                responsive: true,
                title: {
                    display: true,
                    text: "Total (Estimated) Impressions per Party",
                    fontSize: 18,
                },
                legend: {
                    position: 'bottom',
                },
            },
        };

        for (let party in party_ad_data.parties) {
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

            totalImpressionsChartConfig.data.labels.push(party);
            totalImpressionsChartConfig.data.datasets[0].data.push(party_ad_data.parties[party].total_impressions)
            totalImpressionsChartConfig.data.datasets[0].backgroundColor.push(party_ad_data.parties[party].color)
        }

        new Chart($("#impressions_per_day_chart"), impressionsChartConfig);
        new Chart($("#total_impressions_chart"), totalImpressionsChartConfig);
    });

});