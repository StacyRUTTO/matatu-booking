// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});



$(function () {
    $("#id_date_of_departure").datepicker({
        dateFormat: 'yy-mm-dd',
        changeMonth: true,
        changeYear: true,
        minDate: -0,
        maxDate: "+1M",
    });

});


//inline calender for managemet
$(function () {
    $("#datepicker-admin").datepicker({
        dateFormat: 'yy-mm-dd',
        changeMonth: true,
        changeYear: true,
        minDate: -0,
        maxDate: "+1M",
    });
});


// travelling statistics variable
$(document).on("change", "#filter_tags", function () {
    let date;
    let to;
    let origin;

    var ctx = document.getElementById('myChart').getContext('2d');

    var chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'bar',
        // The data for our dataset
        data: {
            labels: ['4 am', '6 am', '8 am', '10 am', '12 noon', '8 pm'],
            datasets: [{
                label: 'Number of people',
                backgroundColor: ["#3e95cd", "#8e5ea2", "#3cba9f", "#e8c3b9", "#c45850", "#ff6384"],
                data: []
            }]
        },
        options: {
            title: {
                display: true,
                text: ''
            },
            scales: {
                yAxes: [
                    {
                        ticks: {
                            beginAtZero: true,
                            stepSize: 1,

                        }
                    }
                ]
            }
        }
    });



    date = $('#datepicker-admin').val();
    to = $('#id_to').val();
    origin = $('#id_origin').val();

    $.ajax({
        url: "ticket_data/",
        type: "POST",
        data: { to: to, origin: origin, date: date },
        success: function (data) {
            $("#tbody").empty();
            // populate the report table
            $("#number").text(data.number);
            console.log(data.number);
            for (const row in data.report) {
                if (data.report.hasOwnProperty(row)) {
                    const traveller = data.report[row];
                    const tr = `<tr><td>${traveller.name}</td><td>${traveller.phone_no}</td><td>${traveller.time}</td><td>${traveller.seat_no}</td></tr>`;
                    $("#tbody").append(tr);
                }
            }
            // populate the chart
            chart.data.datasets.forEach((dataset) => {
                dataset.data = data.ticket_data;
            });
            chart.options.title.text = `Route ${data.origin} to ${data.to} statistics on ${data.date}`
            chart.update();

            // define the download button
            let to = data.to;
            let origin = data.origin;
            let date = data.date;
            let url = `report/${to}/${origin}/${date}`;
            $("#download_btn").attr("href", url);
        }
    })
})



//jquery
$(document).ready(function () {
    // validate phone number
    $("#id_phone_no").keyup(function (e) {
        let no = $("#id_phone_no").val();
        if (no.length > 10 || isNaN(no)){
            $(this).removeClass("is-invalid");
            $('#error_1_id_phone_no').remove();

            $(this).addClass('is-invalid');
            $(this).after(" <p id='error_1_id_phone_no' class='invalid-feedback'><strong>The phone number is not valid.</strong></p>")
        } else{
            $(this).removeClass("is-invalid");
            $('#error_1_id_phone_no').remove();
        }   
    });

    $("#id_phone_no").focusout(function (e) {
        let no = $("#id_phone_no").val();
        if (no.length > 10 || isNaN(no) || no.length < 10){
            $(this).removeClass("is-invalid");
            $('#error_1_id_phone_no').remove();

            $(this).addClass('is-invalid');
            $(this).after(" <p id='error_1_id_phone_no' class='invalid-feedback'><strong>The phone number is not valid.</strong></p>")
        } else{
            $(this).removeClass("is-invalid");
            $('#error_1_id_phone_no').remove();
        }   
    });

    // validate time of depature
    $('#id_time_of_departure').focusout(function () {
        var time_t = $("#id_time_of_departure").val();
        let time_now = new Date($.now());
        let time_now_hours = time_now.getHours();

        var date_d = $("#id_date_of_departure").val();
        var date = new Date(date_d)
        if (date.getDate() === time_now.getDate()) {
            if (time_t < time_now_hours) {

                $(this).removeClass("is-invalid");
                $('#error_1_id_time_of_departure').remove();


                $(this).addClass('is-invalid');
                $(this).after(" <p id='error_1_id_time_of_departure' class='invalid-feedback'><strong>You cannot choose a time before current time.</strong></p>")
            } else {
                $(this).removeClass("is-invalid");
                $('#error_1_id_time_of_departure').remove();
            }
        } else {
            $(this).removeClass("is-invalid");
            $('#error_1_id_time_of_departure').remove();
        }

    });
    //    select seat
    $('.seat').click(function () {
        var seat_number = $(this).text();
        if ($(this).hasClass('taken')) {
            alert("this seat is taken");
        } else {
            $('#id_seat_no').val(seat_number);
            //    change color of selected cell to blue
            $('td').removeClass('selected');
            $(this).addClass('selected');
        }
    });

    // pay via mpesa
    $("#pay").click(function() {
        Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            type: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'
          }).then((result) => {
            if (result.value) {
              Swal.fire(
                'Deleted!',
                'Your file has been deleted.',
                'success'
              )
            }
          })
    });

    //focusout listener on the fields
    $('#bookingform').focusout(function () {
        //    get details for the query
        var to = $("#id_to").val();
        var fr = $("#id_origin").val();
        var date_d = $("#id_date_of_departure").val();
        var time_t = $("#id_time_of_departure").val();

        if (to != "" && fr != "") {
            $.ajax({
                url: "price/",
                type: "POST",
                data: { to: to, fr: fr },
                success: function (data) {
                    $("#id_price").val(data.price)
                }
            })
        }

        //send data to the sever
        if (to != "" && fr != "" && date_d != "" && time_t != "") {
            $.ajax({
                //    url to which you are sending data
                url: "seat/",
                type: 'POST',
                //    optional
                data: { to: to, fr: fr, date_d: date_d, time_t: time_t },
                //    if transaction is a success
                success: function (data) {
                    // clear the taken first
                    $('td').each(function () {
                        $(this).removeClass('taken');
                        $(this).addClass('seat');
                    })
                    // show the seats taken
                    data.taken_seats.forEach(seat => {
                        $('td').each(function () {
                            seat_no = $(this).text();
                            if (seat_no == seat) {
                                $('#id_seat_no').val('');
                                $(this).removeClass('seat');
                                $(this).addClass('taken');
                            }
                        })
                    })
                }
            });
        };

    });


});
