const linkSiga = document.getElementById('linkSiga');
const popup1 = document.getElementById('popup');
const overlay = document.getElementById('overlay');
let url = "https://siga.edubox.pt/auth";

linkSiga.addEventListener('click', function(e) {
    e.preventDefault();
    mostrarPopup();
});

function mostrarPopup() {
    popup1.style.display = 'block';
    overlay.style.display = 'block';
}

function continuar() {
    window.location.href = url;
}

