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
