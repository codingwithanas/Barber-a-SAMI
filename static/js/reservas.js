window.onload = function () {
    generateCalendar();
    setInterval(generateCalendar, 24 * 60 * 60 * 1000);
};

function generateCalendar() {
    fetch('/getAllReservas')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        }) 
        .then(reservas => {
            var table = document.getElementById('reservasTable');
            var days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
            var hours = ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'];

            table.innerHTML = '';

            var headRow = table.insertRow(0);
            headRow.insertCell(0);

            var today = new Date();
            var startOfWeek = today.getDate() - today.getDay() + 1; // Empezar el lunes de esta semana
            today.setDate(startOfWeek);

            days.forEach((day, i) => {
                var date = new Date(today);
                date.setDate(today.getDate() + i);

                var displayDate = date.toLocaleDateString('es-ES', {
                    weekday: 'long', year: 'numeric', month: 'numeric', day: 'numeric'
                });

                var cell = headRow.insertCell();
                cell.innerHTML = displayDate.charAt(0).toUpperCase() + displayDate.slice(1) + ' (' + day + ')';
            });

            hours.forEach((hour, i) => {
                var row = table.insertRow(-1);
                var timeCell = row.insertCell(0);
                timeCell.innerHTML = hour;

                days.forEach((day, j) => {
                    var cell = row.insertCell(-1);
                    var date = new Date(today);
                    date.setDate(today.getDate() + j);
                    var datetime = date.toISOString().split('T')[0] + ' ' + hour;

                    if (j === 5 && i > 10) {
                        cell.innerHTML = 'Cerrado';
                    } else {
                        if (reservas[datetime]) {
                            cell.innerHTML = 'Reservado';
                        } else {
                            cell.innerHTML = `<button data-datetime="${datetime}" onclick="openForm(this)">Reservar</button>`;
                        }
                    }
                });
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function openForm(button) {
    var datetime = button.getAttribute('data-datetime');
    var confirmServiceButton = document.getElementById('confirmServiceButton');
    
    confirmServiceButton.onclick = function() {
        var serviceSelect = document.getElementById('serviceSelect');
        var servicio = serviceSelect.value;
        makeReservation(datetime, servicio);
    };

    $('#serviceModal').modal('show');
}

function makeReservation(datetime, servicio) {
    fetch('/reservarcita', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ datetime: datetime, servicio: servicio }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Reserva realizada con éxito');
            location.reload();
        } else {
            alert(data.message || 'No se pudo realizar la reserva');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
