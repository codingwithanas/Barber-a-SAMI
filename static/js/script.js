    var loginBtn = document.getElementById("loginBtn");
    var loginModal = document.getElementById("loginModal");

    var closeLogin = document.querySelector("#loginModal .close");

    var registerLink = document.getElementById("registerLink");
    var registerModal = document.getElementById("registerModal");

    var closeRegister = document.querySelector("#registerModal .close");

    var backToLogin = document.getElementById("backToLogin");

    loginBtn.addEventListener("click", function() {
        loginModal.style.display = "block";
    });

    closeLogin.addEventListener("click", function() {
        loginModal.style.display = "none";
    });

    registerLink.addEventListener("click", function() {
        loginModal.style.display = "none"; 
        registerModal.style.display = "block"; 
    });

    closeRegister.addEventListener("click", function() {
        registerModal.style.display = "none";
    });

    backToLogin.addEventListener("click", function(event) {
        event.preventDefault(); 
        loginModal.style.display = "block"; 
        registerModal.style.display = "none"; 
    });

    var prevScrollpos = window.pageYOffset;

    window.addEventListener('scroll', function() {
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

    window.addEventListener('scroll', function() {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            backToTop.style.display = "block";
        } else {
            backToTop.style.display = "none";
        }
    });

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
    
        loginBtn.addEventListener('click', function () {
            loginModal.style.display = 'block';
        });
    
        registerLink.addEventListener('click', function () {
            loginModal.style.display = 'none';
            registerModal.style.display = 'block';
        });
    
        backToLogin.addEventListener('click', function () {
            registerModal.style.display = 'none';
            loginModal.style.display = 'block';
        });
    });
    