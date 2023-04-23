function create_barchart(course_num) {

    var chartOptions = {
        responsive: true,
        legend: {
            position: "top", 
            labels: {"fontSize": 14}
        },
        title: {
            display: true,
            text: "Grade Distribution",
            fontSize: 18
        },
        scales: {
            yAxes: [{ticks: {beginAtZero: true}}]
        }
    }

    $.ajax({
        url: "/barchart/"+course_num,
        type: "GET",
        dataType : "json",
        success: function(data) {
            var ctx = document.getElementById('barchart').getContext('2d');
            window.myBar = new Chart(ctx, {
                type: "bar",
                data: data.chart_data,
                options: chartOptions
            });
        },
        error: updateError
    });
}


function displayError(message) {
    $("#error").html(message);
}


function updateError(xhr) {
    if (xhr.status == 0) {
        displayError("Cannot connect to server")
        return
    }

    if (!xhr.getResponseHeader('content-type') == 'application/json') {
        displayError("Received status=" + xhr.status)
        return
    }

    let response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        displayError(response.error)
        return
    }

    displayError(response)
}