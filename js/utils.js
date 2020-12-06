$(document).ready(function () {
    $.getJSON("data.json", function (party_ad_data) {
        $('#last-updated').text(party_ad_data.last_updated);
    });
});