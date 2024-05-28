window.onload = function () {
    generateCalendar(0);
    setInterval(() => generateCalendar(0), 24 * 60 * 60 * 1000);

    document.getElementById('nextWeekButton').addEventListener('click', function() {
        weekOffset++;
        generateCalendar(weekOffset);
    });

    document.getElementById('prevWeekButton').addEventListener('click', function() {
        if (weekOffset > 0) {
            weekOffset--;
            generateCalendar(weekOffset);
        }
    });
};

let weekOffset = 0;

function generateCalendar(offset) {
    const loadingMessage = document.getElementById('loadingMessage');
    const table = document.getElementById('reservasTable');
    
    loadingMessage.style.display = 'block';
    table.style.display = 'none';

    fetch('/getAllReservas')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        }) 
        .then(reservas => {
            const days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
            const hours = ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'];

            table.innerHTML = '';

            const headRow = table.insertRow(0);
            headRow.insertCell(0);

            const today = new Date();
            today.setDate(today.getDate() + (offset * 7)); 

            while (today.getDay() !== 1) {
                today.setDate(today.getDate() - 1);
            }

            days.forEach((day, i) => {
                const date = new Date(today);
                date.setDate(today.getDate() + i);

                const displayDate = date.toLocaleDateString('es-ES', {
                    weekday: 'long', year: 'numeric', month: 'numeric', day: 'numeric'
                });

                const cell = headRow.insertCell();
                cell.innerHTML = displayDate.charAt(0).toUpperCase() + displayDate.slice(1);
            });

            const now = new Date();

            hours.forEach((hour, i) => {
                const row = table.insertRow(-1);
                const timeCell = row.insertCell(0);
                timeCell.innerHTML = hour;

                days.forEach((day, j) => {
                    const cell = row.insertCell(-1);
                    const date = new Date(today);
                    date.setDate(today.getDate() + j);

                    const [hourPart, minutePart] = hour.split(':');
                    date.setHours(hourPart, minutePart, 0, 0);

                    // Restar 2 horas al tiempo de la reserva
                    date.setHours(date.getHours() + 2); // Cambiamos a +2 para mostrar correctamente la hora real en el calendario

                    const datetime = date.toISOString().slice(0, 16).replace('T', ' ');

                    const reservationTime = new Date(date);

                    if (j === 5 && i > 10) {
                        cell.innerHTML = 'Cerrado';
                    } else if (reservationTime < now) {
                        cell.innerHTML = 'No disponible';
                    } else {
                        if (reservas[datetime]) {
                            cell.innerHTML = 'Reservado';
                        } else {
                            cell.innerHTML = `<button data-datetime="${datetime}" onclick="openForm(this)">Reservar</button>`;
                        }
                    }
                });
            });

            loadingMessage.style.display = 'none';
            table.style.display = 'table';
        })
        .catch(error => {
            console.error('Error:', error);
            loadingMessage.style.display = 'none';
        });
}

function openForm(button) {
    const datetime = button.getAttribute('data-datetime');
    const confirmServiceButton = document.getElementById('confirmServiceButton');
    
    confirmServiceButton.onclick = function() {
        const serviceSelect = document.getElementById('serviceSelect');
        const servicio = serviceSelect.value;
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
            generateCalendar(weekOffset);
        } else {
            alert(data.message || 'No se pudo realizar la reserva');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });

    $('#serviceModal').modal('hide');
}
