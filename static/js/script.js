    // Obtener el botón de iniciar sesión y el pop-up de iniciar sesión
    var loginBtn = document.getElementById("loginBtn");
    var loginModal = document.getElementById("loginModal");

    // Obtener el botón de cerrar en el pop-up de iniciar sesión
    var closeLogin = document.querySelector("#loginModal .close");

    // Obtener el botón de registrarse y el pop-up de registrarse
    var registerLink = document.getElementById("registerLink");
    var registerModal = document.getElementById("registerModal");

    // Obtener el botón de cerrar en el pop-up de registrarse
    var closeRegister = document.querySelector("#registerModal .close");

    // Obtener el botón de volver atrás en el pop-up de registro
    var backToLogin = document.getElementById("backToLogin");

    // Mostrar el pop-up de iniciar sesión cuando se hace clic en el botón de iniciar sesión
    loginBtn.addEventListener("click", function() {
        loginModal.style.display = "block";
    });

    // Cerrar el pop-up de iniciar sesión cuando se hace clic en el botón de cerrar
    closeLogin.addEventListener("click", function() {
        loginModal.style.display = "none";
    });

    // Mostrar el pop-up de registrarse cuando se hace clic en el enlace de registrarse
    registerLink.addEventListener("click", function() {
        loginModal.style.display = "none"; // Cerrar el pop-up de iniciar sesión
        registerModal.style.display = "block"; // Mostrar el pop-up de registrarse
    });

    // Cerrar el pop-up de registrarse cuando se hace clic en el botón de cerrar
    closeRegister.addEventListener("click", function() {
        registerModal.style.display = "none";
    });

    // Agregar funcionalidad para el botón de volver atrás en el pop-up de registro
    backToLogin.addEventListener("click", function(event) {
        event.preventDefault(); // Prevenir el comportamiento predeterminado del enlace
        loginModal.style.display = "block"; // Mostrar el pop-up de iniciar sesión
        registerModal.style.display = "none"; // Ocultar el pop-up de registro
    });

    // JavaScript para mostrar u ocultar el navbar de forma suave
    var prevScrollpos = window.pageYOffset;

    window.addEventListener('scroll', function() {
        var currentScrollPos = window.pageYOffset;
        var navbar = document.querySelector('.navbar');
        if (prevScrollpos > currentScrollPos) {
            navbar.style.top = "0";
        } else {
            navbar.style.top = "-60px"; // Ajusta este valor según el tamaño de tu navbar
        }
        prevScrollpos = currentScrollPos;
    });

    // JavaScript para mostrar u ocultar el botón de volver arriba
    var backToTop = document.getElementById("backToTop");

    window.addEventListener('scroll', function() {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            backToTop.style.display = "block";
        } else {
            backToTop.style.display = "none";
        }
    });

    // Funcionalidad para volver al principio de la página con suavizado
    backToTop.addEventListener("click", function() {
        window.scrollTo({top: 0, behavior: 'smooth'});
    });

    document.addEventListener('DOMContentLoaded', function () {
        const loginModal = document.getElementById('loginModal');
        const registerModal = document.getElementById('registerModal');
        const loginForm = document.getElementById('loginForm');
        const registerForm = document.getElementById('registerForm');
        const loginBtn = document.getElementById('loginBtn');
        const registerLink = document.getElementById('registerLink');
        const backToLogin = document.getElementById('backToLogin');
    
        // Mostrar modal de inicio de sesión al hacer clic en "Iniciar sesión"
        loginBtn.addEventListener('click', function () {
            loginModal.style.display = 'block';
        });
    
        // Mostrar modal de registro al hacer clic en "¿No estás registrado?"
        registerLink.addEventListener('click', function () {
            loginModal.style.display = 'none';
            registerModal.style.display = 'block';
        });
    
        // Volver al modal de inicio de sesión al hacer clic en "Volver atrás"
        backToLogin.addEventListener('click', function () {
            registerModal.style.display = 'none';
            loginModal.style.display = 'block';
        });
    });
    