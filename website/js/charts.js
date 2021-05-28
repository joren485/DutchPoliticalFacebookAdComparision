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

const FIRST_DATE = new Date((new Date()).getFullYear() - 1, (new Date()).getMonth(), (new Date()).getDate());

function getDaysArray() {
    let dates = [];
    let now = Date.now();
    for (let dt = new Date(FIRST_DATE); dt <= now; dt.setDate(dt.getDate() + 1)) {
        dates.push(new Date(dt));
    }
    return dates;
}

function generateLineGraphConfig(canvas) {

    let data = $(canvas).data("data");
    let labels = $(canvas).data("labels");
    let is_general_chart = labels.includes("VVD");

    let config = {
        type: 'line',
        data: {
            labels: getDaysArray(),
            datasets: []
        },
        options: {
            animation: false,
            datasets: {
                line: {
                    pointRadius: 0,
                }
            },
            scales: {
                x: {
                    type: "time",
                    time: {
                        tooltipFormat: "YYYY-MM-DD",
                    },
                    min: FIRST_DATE,
                    max: Date.now(),
                },
                y: {
                    stacked: !is_general_chart,
                    ticks: {
                        callback: function (value, index, values) {
                            return canvas.id.includes("spending") ? "€" + value : value;
                        }
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: $(canvas).data("title"),
                    font: {
                        size: 16,
                    },
                },

                legend: {
                    position: "bottom",
                },

                tooltip: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function (context) {
                            let sum = context.chart.config._config.data.datasets.reduce(
                                (total, arg) => total + arg.data[context.dataIndex], 0
                            );
                            let percentage = (context.raw / sum * 100).toFixed(2);
                            let value = canvas.id.includes("spending") ? "€" + context.raw.toFixed(2) : context.raw;
                            return context.dataset.label + ": " + value + " (" + percentage + "%)";
                        }
                    }
                },

                zoom: {
                    zoom: {
                        drag:{
                            enabled: true,
                        },
                        mode: 'x',
                    },
                },
            }
        }
    }

    labels.forEach(function (item, index) {
        config.data.datasets.push(
            {
                label: item,
                data: data[index],
                backgroundColor: COLORS[index],
                borderColor: COLORS[index],
                borderWidth: 1,
                fill: !is_general_chart,
            });
    });

    return config
}

function generateBarChart(canvas) {

    let config = {
        type: 'bar',
        data: {
            labels: $(canvas).data("labels"),
            datasets: [{
                data: $(canvas).data("data"),
                backgroundColor: COLORS,
                maxBarThickness: 30,
            }],
        },
        options: {
            animation: false,
            indexAxis: 'y',
            aspectRatio: 1,

            scales: {
                x: {
                    ticks: {
                        callback: function (value, index, values) {
                            return canvas.id.includes("spending") ? "€" + value : value;
                        },
                    }
                }
            },

            plugins: {
                title: {
                    display: true,
                    text: $(canvas).data("title"),
                    font: {
                        size: 16
                    },
                },

                legend: {
                    display: false,
                },

                tooltip: {
                    mode: "y",
                    intersect: false,
                    callbacks: {
                        label: function (context) {
                            let sum = context.dataset.data.reduce((a, b) => a + b, 0);
                            let percentage = (context.raw / sum * 100).toFixed(2);

                            let value = canvas.id.includes("spending") ? "€" + context.raw.toFixed(2) : context.raw;
                            return value + " (" + percentage + "%)";
                        }
                    }
                }
            }
        }
    }
    return config
}

$(document).ready(function () {
    $("canvas").each(function (index, canvas) {
            if (canvas.id.includes("per-date")) {
                new Chart(canvas, generateLineGraphConfig(canvas));
            } else {
                new Chart(canvas, generateBarChart(canvas));
            }
        }
    );
});
