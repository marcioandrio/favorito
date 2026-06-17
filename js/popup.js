let url = "https://siga.edubox.pt/auth";

const linkSiga = document.getElementById('linkSiga');
const linkInovar = document.getElementById('inovar');
const linkClassroom = document.getElementById('linkClassroom');
const popup1 = document.getElementById('popup');
const overlay = document.getElementById('overlay');

linkSiga.addEventListener('click', function(e) {
    e.preventDefault();
    url = "https://siga.edubox.pt/auth";
    mostrarPopup();
});

linkInovar.addEventListener('click', function(e) {
    e.preventDefault();
    url = "https://aeen.inovarmais.com/consulta/app/index.html#/login";
    mostrarPopup();
});

linkClassroom.addEventListener('click', function(e) {
    e.preventDefault();
    url = "https://classroom.google.com/u/0/s";
    mostrarPopup();
});

function mostrarPopup() {
    popup1.style.display = 'block';
    overlay.style.display = 'block';
}

function continuar() {
    window.location.href = url;
}
