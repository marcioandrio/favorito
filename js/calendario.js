function gerarCalendario(data) {
    const calendario = document.getElementById("calendario");
    calendario.innerHTML = ""; // Limpa o calendário anterior
  
    const ano = data.getFullYear();
    const mes = data.getMonth();
    const primeiroDia = new Date(ano, mes, 1).getDay();
    const ultimoDia = new Date(ano, mes + 1, 0).getDate();
  
    const mesNome = data.toLocaleString("default", { month: "long" });
  
    let html = `
      <div class="mes">${mesNome} ${ano}</div>
      <div class="semana">
        <span>Dom</span><span>Seg</span><span>Ter</span><span>Qua</span>
        <span>Qui</span><span>Sex</span><span>Sáb</span>
      </div>
      <div class="dias">
    `;
  
    for (let i = 0; i < primeiroDia; i++) {
      html += "<span></span>"; // Dias vazios antes do primeiro dia
    }
  
    const hoje = new Date();
    const hojeDia = hoje.getDate();
    const hojeMes = hoje.getMonth();
    const hojeAno = hoje.getFullYear();
  
    for (let dia = 1; dia <= ultimoDia; dia++) {
      const isHoje = dia === hojeDia && mes === hojeMes && ano === hojeAno;
      const classeHoje = isHoje ? "hoje" : "";
      html += `<span class="${classeHoje}">${dia}</span>`;
    }
  
    html += "</div>";
    calendario.innerHTML = html;
  }
  
  function atualizarCalendario() {
    const agora = new Date();
    gerarCalendario(agora);
    console.log("Calendário atualizado");
  }
  
  document.addEventListener("DOMContentLoaded", function() {
    atualizarCalendario(); // Gera o calendário inicial
    setInterval(atualizarCalendario, 60000); // Atualiza a cada minuto
  });