const COLORS = [
    "#BFC3BA",
    "#60495A",
    "#1A3A3A",
    "#3B429F",
    "#AA7DCE",
    "#F5D7E3",
    "#512500",
    "#84ACCE",
    "#D7D9B1",
    "#7D1D3F",
    "#FF6B35",
    "#F7C59F",
    "#004E89",
    "#050517",
    "#D3D5D7",
    "#B3DEC1",
    "#F7B801",
    "#2D4739",
    "#09814A",
    "#B5BD89",
];

function percentageBarGraph(tooltipItems, data) {
    let dataset = data.datasets[tooltipItems.datasetIndex];
    let value = dataset.data[tooltipItems.index];

    let total = 0;
    dataset.data.forEach(function (element) {
        total += element;
    });

    if (total === 0) {
        return 0;
    }

    return (value / total * 100).toFixed(2);
}

function percentageLineGraph(tooltipItems, data) {

    let total = 0;
    data.datasets.forEach(function (dataset) {
        total += dataset.data[tooltipItems.index]
    });

    if (total === 0){
        return 0;
    }
    return (tooltipItems.yLabel / total * 100).toFixed(2);
}

function getDaysArray() {
    let startDate = new Date("2020-01-01");
    let dates = [];
    let now = new Date();
    for (let dt = new Date(startDate); dt <= now; dt.setDate(dt.getDate() + 1)) {
        dates.push(new Date(dt).toISOString().split('T')[0]);
    }
    return dates;
}

function generateLineGraphConfig(canvas) {

    let data = $(canvas).data("data");
    let labels = $(canvas).data("labels");

    let is_general_chart = labels[-1] === "VVD"

    let scales = {
        xAxes: [{
            ticks: {},
            type: "time",
            time: {
                unit: "day",
                stepSize: 1,
            }
        }],
        yAxes: [{
            ticks: {},
        }]
    };

    let tooltips = {
        mode: 'index',
        intersect: false,
        position: "nearest",
        callbacks: {
            label: function (tooltipItems, data) {
                let percentage = percentageLineGraph(tooltipItems, data);
                return data.datasets[tooltipItems.datasetIndex].label + ": " + tooltipItems.yLabel + " (" + percentage + "%)";
            },
        },
    };
    if (canvas.id.includes("spending")) {

        scales.yAxes[0].ticks.callback = function (value, index, values) {
                return "€" + value;
        };
        tooltips.callbacks.label = function (tooltipItems, data) {
            let percentage = percentageLineGraph(tooltipItems, data);
            return data.datasets[tooltipItems.datasetIndex].label + ": €" + tooltipItems.yLabel.toFixed(2) + " (" + percentage + "%)";
        }
    }

    scales.yAxes[0].stacked = !is_general_chart;

    let graphConfig = {
        type: "line",
        data: {
            labels: getDaysArray(),
            datasets: []
        },
        options: {
            animation: {
                duration: 0
            },
            hover: {
                animationDuration: 0
            },
            responsiveAnimationDuration: 0,
            responsive: true,
            title: {
                display: true,
                text: "Per Date",
                fontSize: 16,
            },
            legend: {
                position: "bottom",
                labels: {padding: 7,},
            },
            scales: scales,
            tooltips: tooltips,
            plugins: {
                zoom: {
                    zoom: {
                        enabled: true,
                        drag: true,
                        mode: "x",
                    }
                }
            },
        },
    };
    labels.forEach(function (item, index) {
        graphConfig.data.datasets.push(
            {
                label: item,
                data: data[index],
                fill: !is_general_chart,
                backgroundColor: COLORS[index],
                borderColor: COLORS[index],
                pointRadius: 0,
                borderWidth: 2,
            });
    });

    return graphConfig;
}

function generateBarChart(canvas) {

    let data = $(canvas).data("data");
    let labels = $(canvas).data("labels");

    let scales = {
        xAxes: [
            {
                ticks: {
                    beginAtZero: true,
                },
            }],
        yAxes: [{}],
    }

    let tooltips = {
        intersect: false,
        callbacks: {
            label: function (tooltipItems, data) {

                let dataset = data.datasets[tooltipItems.datasetIndex];
                let value = dataset.data[tooltipItems.index];

                let percentage = percentageBarGraph(tooltipItems, data);
                return value + " (" + percentage + "%)";
            },
        },
    };

    if (canvas.id.includes("spending")) {
        scales.xAxes[0].ticks.callback = function (value, index, values) {
                return "€" + value;
        };

        tooltips.callbacks.label = function (tooltipItems, data) {

            let dataset = data.datasets[tooltipItems.datasetIndex];
            let value = dataset.data[tooltipItems.index];

            let percentage = percentageBarGraph(tooltipItems, data);
            return "€" + value.toFixed(2) + " (" + percentage + "%)";
        };
    }
    let chartConfig = {
        type: "horizontalBar",
        data: {
            labels: [],
            datasets: [{
                data: [],
                backgroundColor: [],
                maxBarThickness: 30,
            }]
        },
        options: {
            animation: {
                duration: 0
            },
            hover: {
                animationDuration: 0
            },
            responsiveAnimationDuration: 0,
            maintainAspectRatio: false,
            responsive: true,
            title: {
                display: true,
                text: "Total",
                fontSize: 16,
            },
            legend: {
                display: false,
            },
            tooltips: tooltips,
            scales: scales,
        }
    };

    labels.forEach(function (item, index) {
        chartConfig.data.labels.push(item);
        chartConfig.data.datasets[0].data.push(data[index])
        chartConfig.data.datasets[0].backgroundColor.push(COLORS[index])
    });

    return chartConfig;
}