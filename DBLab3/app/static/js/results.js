document.getElementById("btn_get_results").addEventListener("click", function() {
    var subjectValue = parseInt(document.querySelector('input[name="subject"]:checked').value);
    var yearValue = parseInt(document.querySelector('input[name="year"]:checked').value);
    var regionValue = parseInt(document.querySelector('input[name="region"]:checked').value);

    var data = {
        subject: subjectValue,
        year: yearValue,
        region: regionValue
    };

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/results', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            drawCharts(response);
        }
    };
    xhr.send(JSON.stringify(data));
});

function drawCharts(data) {
    var barData = data.bar[0];
    var pieData = data.pie[0];

    var barLayout = {
        title: 'Bar Chart',
        // Add any desired layout options
    };
    Plotly.newPlot('bar', [barData], barLayout);

    var pieLayout = {
        title: 'Pie Chart',
        // Add any desired layout options
    };
    Plotly.newPlot('pie', [pieData], pieLayout);
}
