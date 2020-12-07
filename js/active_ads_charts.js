$(document).ready(function () {
    $.getJSON("data.json", function (party_ad_data) {

        let activeAdsChartConfig = {
            type: "line",
            data: {
                labels: party_ad_data.dates,
                datasets: []
            },
            options: {
                responsive: true,
                title: {
                    display: true,
                    text: "Ads Active per Day",
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
        let totalActiveAdsChartConfig = {
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
                    text: "Total Ads per Party (" + party_ad_data.total_ads + " total)",
                    fontSize: 18,
                },
                legend: {
                    position: 'bottom',
                },
                tooltips: {
                    callbacks: {
                        label: function (tooltipItem, data) {

                            let dataset = data.datasets[tooltipItem.datasetIndex];
                            let total = dataset._meta[Object.keys(dataset._meta)[0]].total;
                            let current_value = dataset.data[tooltipItem.index];
                            let percentage = (current_value / total * 100).toFixed(2);
                            return current_value.toFixed(2) + " (" + percentage + "%)";
                        },
                        title: function (tooltipItem, data) {
                            return data.labels[tooltipItem[0].index];
                        }
                    }
                },
            }
        };

        for (let party in party_ad_data.parties) {
            activeAdsChartConfig.data.datasets.push(
                {
                    label: party,
                    data: party_ad_data.parties[party].active_ads,
                    fill: false,
                    backgroundColor: party_ad_data.parties[party].color,
                    borderColor: party_ad_data.parties[party].color,
                    pointRadius: 0,
                    borderWidth: 2,
                });

            totalActiveAdsChartConfig.data.labels.push(party);
            totalActiveAdsChartConfig.data.datasets[0].data.push(party_ad_data.parties[party].total_ads)
            totalActiveAdsChartConfig.data.datasets[0].backgroundColor.push(party_ad_data.parties[party].color)

        }

        new Chart($("#active_ads_per_day_chart"), activeAdsChartConfig);
        new Chart($("#total_active_ads_chart"), totalActiveAdsChartConfig);
    });
});