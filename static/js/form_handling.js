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
                document.getElementById('loginMessage').innerHTML = `<div class="alert alert-success mt-3">Inicio de sesión exitoso</div>`;
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

    document.getElementById('registerForm').addEventListener('submit', function(event) {
        const password = document.getElementById('registerPassword').value;
        if (password.length < 6) {
            event.preventDefault();
            alert("La contraseña debe tener al menos 6 caracteres.");
        } else {
            event.preventDefault();
            const formData = new FormData(this);
            document.getElementById('registerLoading').style.display = 'block';
            document.getElementById('registerMessage').innerHTML = '';
            fetch('/register', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('registerLoading').style.display = 'none';
                if (data.message) {
                    document.getElementById('registerMessage').innerHTML = `<div class="alert alert-success mt-3">Registro exitoso</div>`;
                    setTimeout(() => {
                        window.location.href = '/';
                    }, 2000);
                } else if (data.error) {
                    document.getElementById('registerMessage').innerHTML = `<div class="alert alert-danger mt-3">${data.error}</div>`;
                }
            })
            .catch(error => {
                document.getElementById('registerLoading').style.display = 'none'; 
                document.getElementById('registerMessage').innerHTML = `<div class="alert alert-danger mt-3">Error: ${error}</div>`;
                console.error('Error:', error);
            });
        }
    });
});
