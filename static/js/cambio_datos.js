window.onload = function() {
    fetch('/getCurrentEmail')
        .then(response => response.json())
        .then(data => {
            document.getElementById('currentEmail').value = data.currentEmail;
        });
};

function sendAjaxRequest(url, data) {
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => response.json()).then(data => {
        alert(data.message);
    });
}

document.getElementById('changePasswordForm').addEventListener('submit', event => {
    event.preventDefault();
    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    if(newPassword.length < 6){
        alert("La nueva contraseña debe tener al menos 6 caracteres.");
    } else {
        sendAjaxRequest('/changePassword', { currentPassword, newPassword });
    }
});

document.getElementById('changeEmailForm').addEventListener('submit', event => {
    event.preventDefault();
    const newEmail = document.getElementById('newEmail').value;
    sendAjaxRequest('/changeEmail', { newEmail });
});