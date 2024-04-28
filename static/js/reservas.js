window.onload = function () {
    var table = document.getElementById('reservasTable');
    var days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
    var hours = ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00'];

    // Crear las filas y columnas de la tabla
    for (var i = 0; i <= hours.length; i++) {
        var row = table.insertRow(i);

        for (var j = 0; j <= days.length; j++) {
            var cell = row.insertCell(j);

            if (i === 0) {
                cell.innerHTML = j > 0 ? days[j - 1] : '';
            } else if (j === 0) {
                cell.innerHTML = hours[i - 1];
            } else {
                if (j == 6 && i > 11) {
                    cell.innerHTML = 'Cerrado';
                } else {
                    cell.innerHTML = '<button onclick="openForm()">Reservar</button>';
                }
            }
        }
    }
};

function openForm(day, hour) {
    fetch('/reservarcita', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ day: day, hour: hour }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Reserva realizada con éxito');
            location.reload();
        } else {
            alert('No se pudo realizar la reserva');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
