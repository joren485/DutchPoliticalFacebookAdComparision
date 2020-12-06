$(document).ready(function () {
    $.getJSON("data.json", function (party_ad_data) {
        let potentialReachChartConfig = {
            type: "line",
            data: {
                labels: party_ad_data.dates,
                datasets: []
            },
            options: {
                responsive: true,
                title: {
                    display: true,
                    text: "Average Potential Reach per Day",
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
            potentialReachChartConfig.data.datasets.push(
                {
                    label: party,
                    data: party_ad_data.parties[party].potential_reach,
                    fill: false,
                    backgroundColor: party_ad_data.parties[party].color,
                    borderColor: party_ad_data.parties[party].color,
                    pointRadius: 0,
                    borderWidth: 2,
                });
        }

        new Chart($("#potential_reach_per_day_chart"), potentialReachChartConfig);
        $('#missing-potential-reach').text(party_ad_data.missing_potential_reach);
        $('#total-ads').text(party_ad_data.total_ads);
    });
});