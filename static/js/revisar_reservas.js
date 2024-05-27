$(document).ready(function() {
    var reservationsList = $('#reservationsList');
    var noReservationsMessage = $('#noReservationsMessage');

    moment.locale('es');

    function loadReservations() {
        $.ajax({
            url: '/getReservas',
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                reservationsList.empty();
                if (data.reservas && data.reservas.length > 0) {
                    $.each(data.reservas, function(index, reserva) {
                        var day = reserva[1]; 
                        var hour = reserva[2];
                        var date = moment(reserva[3]).format('dddd, D [de] MMMM [de] YYYY'); 
                        var servicio = reserva[4]; 
                        var reservationItem = $('<li>')
                            .addClass('list-group-item d-flex justify-content-between align-items-center')
                            .text(day + ' a las ' + hour + ' (' + date + ') - ' + servicio);
                        var deleteButton = $('<button>')
                            .addClass('btn btn-danger btn-sm delete-reserva')
                            .text('X')
                            .attr('data-id', reserva[0])
                            .on('click', function() {
                                var id = $(this).attr('data-id');
                                cancelarReserva(id);
                            });
                        reservationItem.append(deleteButton);
                        reservationsList.append(reservationItem);
                    });
                    noReservationsMessage.hide();
                } else {
                    noReservationsMessage.show();
                }
            },
            error: function(error) {
                console.error('Error:', error);
                noReservationsMessage.show();
            }
        });
    }

    function cancelarReserva(id) {
        $.ajax({
            url: '/cancelar_reserva/' + id,
            type: 'DELETE',
            success: function(response) {
                alert(response.message);
                loadReservations();
            },
            error: function(error) {
                console.error('Error:', error);
                alert('Error al eliminar la reserva.');
            }
        });
    }

    loadReservations();
});
