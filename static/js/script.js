document.addEventListener("DOMContentLoaded", function () {
    // Variables para el modal de inicio de sesión
    var loginBtn = document.getElementById("loginBtn");
    var loginBtnSidebar = document.getElementById("loginBtnSidebar");
    var loginModal = document.getElementById("loginModal");
    var closeLogin = document.querySelector("#loginModal .close");

    // Variables para el modal de registro
    var registerLink = document.getElementById("registerLink");
    var registerModal = document.getElementById("registerModal");
    var closeRegister = document.querySelector("#registerModal .close");
    var backToLogin = document.getElementById("backToLogin");

    // Mostrar modal de inicio de sesión
    if (loginBtn) {
        loginBtn.addEventListener("click", function () {
            loginModal.style.display = "block";
        });
    }

    if (loginBtnSidebar) {
        loginBtnSidebar.addEventListener("click", function () {
            loginModal.style.display = "block";
        });
    }

    if (closeLogin) {
        closeLogin.addEventListener("click", function () {
            loginModal.style.display = "none";
        });
    }

    // Cambiar a modal de registro
    if (registerLink) {
        registerLink.addEventListener("click", function () {
            loginModal.style.display = "none";
            registerModal.style.display = "block";
        });
    }

    if (closeRegister) {
        closeRegister.addEventListener("click", function () {
            registerModal.style.display = "none";
        });
    }

    if (backToLogin) {
        backToLogin.addEventListener("click", function (event) {
            event.preventDefault();
            loginModal.style.display = "block";
            registerModal.style.display = "none";
        });
    }

    var prevScrollpos = window.pageYOffset;
    window.addEventListener('scroll', function () {
        var currentScrollPos = window.pageYOffset;
        var navbar = document.querySelector('.navbar');
        if (prevScrollpos > currentScrollPos) {
            navbar.style.top = "0";
        } else {
            navbar.style.top = "-60px";
        }
        prevScrollpos = currentScrollPos;
    });

    var backToTop = document.getElementById("backToTop");
    window.addEventListener('scroll', function () {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            backToTop.style.display = "block";
        } else {
            backToTop.style.display = "none";
        }
    });

    var menuToggle = document.getElementById("menuToggle");
    var sidebar = document.getElementById("sidebar");
    var closeBtn = document.getElementById("closeBtn");

    if (menuToggle) {
        menuToggle.addEventListener("click", function () {
            sidebar.style.display = "block";
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener("click", function () {
            sidebar.style.display = "none";
        });
    }

    window.addEventListener("click", function (event) {
        if (event.target === sidebar) {
            sidebar.style.display = "none";
        }
    });
});
