function atualizarRelogio() {
    const agora = new Date();
    const hora = agora.getHours();
    const minuto = agora.getMinutes();
    const segundo = agora.getSeconds();
  
    const rotacaoHora = (hora * 30) + (minuto / 2);
    const rotacaoMinuto = minuto * 6;
    const rotacaoSegundo = segundo * 6;
  
    document.getElementById("ponteiro-hora").style.transform = `translate(-50%, -100%) rotate(${rotacaoHora}deg)`;
    document.getElementById("ponteiro-minuto").style.transform = `translate(-50%, -100%) rotate(${rotacaoMinuto}deg)`;
    document.getElementById("ponteiro-segundo").style.transform = `translate(-50%, -100%) rotate(${rotacaoSegundo}deg)`;
  }
  
  document.addEventListener("DOMContentLoaded", function() {
    atualizarRelogio();
    setInterval(atualizarRelogio, 1000);
  });