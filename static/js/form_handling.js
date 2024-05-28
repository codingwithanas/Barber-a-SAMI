document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('loginForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        document.getElementById('loginLoading').style.display = 'block'; 
        document.getElementById('loginMessage').innerHTML = '';

        fetch('/login', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('loginLoading').style.display = 'none';
            if (data.message) {
                setTimeout(() => {
                    window.location.href = '/'; 
                }, 2000);
            } else if (data.error) {
                document.getElementById('loginMessage').innerHTML = `<div class="alert alert-danger mt-3">${data.error}</div>`;
            }
        })
        .catch(error => {
            document.getElementById('loginLoading').style.display = 'none';
            document.getElementById('loginMessage').innerHTML = `<div class="alert alert-danger mt-3">Error: ${error}</div>`;
            console.error('Error:', error);
        });
    });

    // Manejo del formulario de registro
    const registerForm = document.getElementById('registerForm');
    const passwordInput = document.getElementById('registerPassword');
    const repeatPasswordInput = document.getElementById('repeatPassword');
    const messageContainer = document.getElementById('registerMessage');

    const passwordIcon = document.createElement('span');
    const repeatPasswordIcon = document.createElement('span');

    passwordIcon.classList.add('icon');
    repeatPasswordIcon.classList.add('icon');
    
    passwordInput.parentNode.appendChild(passwordIcon);
    repeatPasswordInput.parentNode.appendChild(repeatPasswordIcon);

    function validatePasswords() {
        const password = passwordInput.value;
        const repeatPassword = repeatPasswordInput.value;

        if (password.length < 6) {
            messageContainer.innerHTML = `<div class="alert alert-danger mt-3">La contraseña debe tener al menos 6 caracteres.</div>`;
            passwordIcon.innerHTML = '';
            repeatPasswordIcon.innerHTML = '';
            return false;
        }
        if (password !== repeatPassword) {
            messageContainer.innerHTML = `<div class="alert alert-danger mt-3">Las contraseñas no coinciden.</div>`;
            passwordIcon.innerHTML = '';
            repeatPasswordIcon.innerHTML = '&#10060;';  // Red cross
            repeatPasswordIcon.style.color = 'red';
            return false;
        } else {
            messageContainer.innerHTML = '';
            passwordIcon.innerHTML = '&#9989;';  // Green check mark
            passwordIcon.style.color = 'green';
            repeatPasswordIcon.innerHTML = '&#9989;';  // Green check mark
            repeatPasswordIcon.style.color = 'green';
            return true;
        }
    }

    repeatPasswordInput.addEventListener('blur', validatePasswords);

    registerForm.addEventListener('submit', function(event) {
        event.preventDefault();

        if (!validatePasswords()) {
            return;
        }

        const formData = new FormData(this);
        document.getElementById('registerLoading').style.display = 'block';
        messageContainer.innerHTML = '';

        fetch('/register', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('registerLoading').style.display = 'none';
            if (data.message) {
                messageContainer.innerHTML = `<div class="alert alert-success mt-3">Registro exitoso</div>`;
                setTimeout(() => {
                    window.location.href = '/';
                }, 2000);
            } else if (data.error) {
                messageContainer.innerHTML = `<div class="alert alert-danger mt-3">${data.error}</div>`;
            }
        })
        .catch(error => {
            document.getElementById('registerLoading').style.display = 'none'; 
            messageContainer.innerHTML = `<div class="alert alert-danger mt-3">Error: ${error}</div>`;
            console.error('Error:', error);
        });
    });
});
