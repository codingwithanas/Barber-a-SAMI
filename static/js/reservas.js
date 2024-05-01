window.onload = function () {
    var table = document.getElementById('reservasTable');
    var days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
    var hours = ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00'];

    var headRow = table.insertRow(0);
    headRow.insertCell(0);
    days.forEach(day => {
        var cell = headRow.insertCell();
        cell.innerHTML = day;
    });

    hours.forEach((hour, i) => {
        var row = table.insertRow(-1);
        var timeCell = row.insertCell(0);
        timeCell.innerHTML = hour;

        days.forEach((day, j) => {
            var cell = row.insertCell(-1);
            if (j === 5 && i > 10) {
                cell.innerHTML = 'Cerrado';
            } else {
                var fecha_reserva = new Date().toISOString().split('T')[0];
                cell.innerHTML = `<button data-day="${day}" data-hour="${hour}" data-fecha-reserva="${fecha_reserva}" onclick="openForm(this)">Reservar</button>`;
            }
        });
    });
};

function openForm(button) {
    var day = button.getAttribute('data-day');
    var hour = button.getAttribute('data-hour');
    var fecha_reserva = new Date().toISOString().split('T')[0];

    fetch('/reservarcita', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ day: day, hour: hour, fecha_reserva: fecha_reserva }),
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