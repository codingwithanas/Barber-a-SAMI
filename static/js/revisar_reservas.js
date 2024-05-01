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
                $.each(data.reservas, function(index, reserva) {
                    var day = reserva[0];
                    var hour = reserva[1];
                    var reservationItem = $('<li>').addClass('list-group-item').text(day + ' a las ' + hour);
                    reservationsList.append(reservationItem);
                });

                var modifyReservationButton = $('<button>').addClass('btn btn-primary mt-3').text('Modificar Reserva').click(function() {
              
                });

                reservationsList.after(modifyReservationButton); 
            } else {
                noReservationsMessage.show(); 
            }
        },
        error: function(error) {
            console.error('Error:', error);
            noReservationsMessage.show(); 
        }
    });
});
