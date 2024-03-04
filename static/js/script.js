// Script.js

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

// Controlar el envío del formulario de inicio de sesión
var loginForm = document.getElementById("loginForm");
loginForm.addEventListener("submit", function(event) {
    event.preventDefault(); // Evitar el envío del formulario
    // Aquí puedes agregar la lógica para el inicio de sesión con AJAX u otra tecnología
    console.log("Iniciar sesión...");
});

// Controlar el envío del formulario de registro
var registerForm = document.getElementById("registerForm");
registerForm.addEventListener("submit", function(event) {
    event.preventDefault(); // Evitar el envío del formulario
    // Aquí puedes agregar la lógica para el registro con AJAX u otra tecnología
    console.log("Registrarse...");
});

// Agregar funcionalidad para el botón de volver atrás en el pop-up de registro
backToLogin.addEventListener("click", function(event) {
    event.preventDefault(); // Prevenir el comportamiento predeterminado del enlace
    loginModal.style.display = "block"; // Mostrar el pop-up de iniciar sesión
    registerModal.style.display = "none"; // Ocultar el pop-up de registro
});

// JavaScript para ocultar el navbar al desplazarse hacia abajo
var prevScrollpos = window.pageYOffset;

window.onscroll = function() {
    var currentScrollPos = window.pageYOffset;
    if (prevScrollpos > currentScrollPos) {
        document.querySelector(".navbar").classList.remove("hidden");
    } else {
        document.querySelector(".navbar").classList.add("hidden");
    }
    prevScrollpos = currentScrollPos;
}

var mySwiper = new Swiper('.swiper-container', {
    autoplay: {
        delay: 5000,
    },
});

// Código previo...

// Botón de volver arriba
var backToTop = document.getElementById("backToTop");

// Mostrar el botón de volver arriba cuando se hace scroll hacia abajo
window.onscroll = function() {
    var currentScrollPos = window.pageYOffset;
    
    // Ocultar o mostrar la barra de navegación
    if (prevScrollpos > currentScrollPos) {
        document.querySelector(".navbar").style.top = "0";
    } else {
        document.querySelector(".navbar").style.top = "-50px"; // Ajusta este valor al tamaño de tu navbar
    }
    prevScrollpos = currentScrollPos;
    
    // Mostrar el botón de volver arriba después de un cierto scroll
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        backToTop.style.display = "block";
    } else {
        backToTop.style.display = "none";
    }
};

// Funcionalidad para volver al principio de la página
backToTop.addEventListener("click", function() {
    document.body.scrollTop = 0; // Para Safari
    document.documentElement.scrollTop = 0; // Para Chrome, Firefox, IE y Opera
});
// JavaScript para ocultar el navbar de forma suave al desplazarse hacia abajo
var prevScrollpos = window.pageYOffset;

window.onscroll = function() {
    var currentScrollPos = window.pageYOffset;
    // Ajusta el estilo top del navbar basándose en la posición de desplazamiento
    if (prevScrollpos < currentScrollPos) {
        document.querySelector(".navbar").style.top = "-60px"; // Asegúrate de que este valor sea suficiente para ocultar el navbar
    } else {
        document.querySelector(".navbar").style.top = "0";
    }
    prevScrollpos = currentScrollPos;

    // Mostrar el botón de volver arriba después de un cierto scroll
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        backToTop.style.display = "block";
    } else {
        backToTop.style.display = "none";
    }
};

// Funcionalidad para volver al principio de la página con suavizado
backToTop.addEventListener("click", function() {
    window.scrollTo({top: 0, behavior: 'smooth'});
});
