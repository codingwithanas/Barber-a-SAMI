document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('loginForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        fetch('/login', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data); 
        })
        .catch(error => console.error('Error:', error));
    });

    document.getElementById('registerForm').addEventListener('submit', function(event) {
        const password = document.getElementById('registerPassword').value;
        if(password.length < 6){
            event.preventDefault();
            alert("La contraseña debe tener al menos 6 caracteres.");
        } else {
            event.preventDefault();
            const formData = new FormData(this);
            fetch('/register', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
            })
            .catch(error => console.error('Error:', error));
        }
    });
});