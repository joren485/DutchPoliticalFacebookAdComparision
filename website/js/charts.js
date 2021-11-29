// mpn65 qualitative palette
const COLORS = [
    "#ff0029",
    "#377eb8",
    "#66a61e",
    "#984ea3",
    "#00d2d5",
    "#ff7f00",
    "#af8d00",
    "#7f80cd",
    "#b3e900",
    "#c42e60",
    "#a65628",
    "#f781bf",
    "#8dd3c7",
    "#bebada",
    "#fb8072",
    "#80b1d3",
    "#fdb462",
    "#fccde5",
    "#bc80bd",
    "#ffed6f",
];

const FIRST_DATE = new Date(2020, 8, 1);

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
    return {
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
}

$(document).ready(function () {

    $("canvas").each(function (index, canvas) {
            if (canvas.id.includes("daily")) {
                new Chart(canvas, generateLineGraphConfig(canvas));
            } else {
                new Chart(canvas, generateBarChart(canvas));
            }
        }
    );

    $(".update-charts").on("click", function (){
        let divId = $(this).data("id");
        let data = $(this).data("data");

        let party = $(this).data("party");
        let theme = $(this).data("theme")

        $("#" + divId + " canvas").each(function (index, canvas){
            let chart = Chart.getChart(canvas)

            if(party){
                chart.config.options.plugins.title.text = chart.config.options.plugins.title.text.replace(/ by \w+/, " by " + party);
            }
            if(theme){
                chart.config.options.plugins.title.text = chart.config.options.plugins.title.text.replace(/ about [\w &]+? Distributed/, " about " + theme + " Distributed");
            }

            chart.config.data.datasets[0].data = data[index];
            chart.update();
        })
    });

    $(".first-button").each(function (){
        $(this).click();
    });

});
