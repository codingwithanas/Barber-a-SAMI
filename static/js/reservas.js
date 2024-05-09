window.onload = function () {
    generateCalendar();
    setInterval(generateCalendar, 24 * 60 * 60 * 1000); 
};

function generateCalendar() {
    var table = document.getElementById('reservasTable');
    var days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
    var hours = ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'];


    table.innerHTML = '';

    var headRow = table.insertRow(0);
    headRow.insertCell(0);
    days.forEach((day, i) => {
        var date = new Date();
        date.setDate(date.getDate() + i);
        var displayDate = date.toLocaleDateString(); 
        var cell = headRow.insertCell();
        cell.innerHTML = displayDate + ' (' + day + ')';
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
                var date = new Date();
                date.setDate(date.getDate() + j); 
                var datetime = date.toISOString().split('T')[0] + ' ' + hour;
                cell.innerHTML = `<button data-day="${day}" data-hour="${hour}" data-datetime="${datetime}" onclick="openForm(this)">Reservar</button>`;
            }
        });
    });
}

function openForm(button) {
    var datetime = button.getAttribute('data-datetime');

    fetch('/reservarcita', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ datetime: datetime }),
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