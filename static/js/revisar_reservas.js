$(document).ready(function() {
    var reservationsList = $('#reservationsList');
    var noReservationsMessage = $('<p>').text('No tienes reservas actualmente.').hide();
    reservationsList.after(noReservationsMessage);

    $.ajax({
        url: '/getReservas',
        type: 'GET',
        dataType: 'json',
        success: function(data) { 
            console.log(data);

            reservationsList.empty();

            if (data.reservas && data.reservas.length > 0) {
                noReservationsMessage.hide();
                $.each(data.reservas, function(index, reserva) {
                    var day = reserva[0];
                    var hour = reserva[1];
                    var fecha_reserva = reserva[2];
                    var reservationItem = $('<li>').addClass('list-group-item').text(day + ' a las ' + hour + ', reservado el ' + fecha_reserva);
                    reservationsList.append(reservationItem);
                });
            } else {
                noReservationsMessage.show();
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
});
