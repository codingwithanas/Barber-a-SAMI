document.addEventListener("DOMContentLoaded", function () {
    var loginBtn = document.getElementById("loginBtn");
    var loginBtnSidebar = document.getElementById("loginBtnSidebar");
    var loginModal = document.getElementById("loginModal");
    var closeLogin = document.querySelector("#loginModal .close");

    var registerLink = document.getElementById("registerLink");
    var registerModal = document.getElementById("registerModal");
    var closeRegister = document.querySelector("#registerModal .close");
    var backToLogin = document.getElementById("backToLogin");

    var forgotPasswordLink = document.getElementById("forgotPasswordLink");
    var forgotPasswordModal = document.getElementById("forgotPasswordModal");
    var closeForgotPassword = document.querySelector("#forgotPasswordModal .close");

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

    if (forgotPasswordLink) {
        forgotPasswordLink.addEventListener("click", function () {
            loginModal.style.display = "none";
            forgotPasswordModal.style.display = "block";
        });
    }

    if (closeForgotPassword) {
        closeForgotPassword.addEventListener("click", function () {
            forgotPasswordModal.style.display = "none";
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

    backToTop.addEventListener("click", function () {
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
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

document.getElementById('menuToggle').addEventListener('click', function() {
    document.getElementById('sidebar').style.display = 'block';
});

document.getElementById('closeBtn').addEventListener('click', function() {
    document.getElementById('sidebar').style.display = 'none';
});

document.addEventListener("DOMContentLoaded", function () {
    var forgotPasswordForm = document.getElementById("forgotPasswordForm");
    var forgotPasswordMessage = document.getElementById("forgotPasswordMessage");

    forgotPasswordForm.addEventListener("submit", function (event) {
        event.preventDefault();
        
        var email = document.getElementById("forgotPasswordEmail").value;
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/forgot_password", true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    forgotPasswordMessage.innerHTML = "<p style='color: green;'>Correo de restablecimiento de contraseña enviado</p>";
                } else {
                    forgotPasswordMessage.innerHTML = "<p style='color: red;'>Correo no encontrado</p>";
                }
            }
        };

        xhr.send("forgotPasswordEmail=" + encodeURIComponent(email));
    });
});
