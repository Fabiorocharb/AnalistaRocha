const btnMobile = document.getElementById('btn-mobile');

function toggleMenu(event) {
  if (event.type === 'touchstart') event.preventDefault();
  const menu = document.getElementById("menu");
  menu.classList.toggle('active');
  const active = menu.classList.contains('active');
  event.currentTarget.setAttribute('aria-expanded', active);
  if (active) {
    event.currentTarget.setAttribute('aria-label', 'Fechar Menu');
  } else {
    event.currentTarget.setAttribute('aria-label', 'Abrir Menu');
  }
}
btnMobile.addEventListener("click", toggleMenu);
btnMobile.addEventListener("touchstart", toggleMenu);


const container = document.getElementById('animation-one');
  
  // Configurações da animação (substitua 'nome-do-arquivo.json' pelo nome do seu arquivo Lottie)
  const animacao = lottie.loadAnimation({
    container: container,
    renderer: 'svg', // ou 'canvas' ou 'html'
    loop: true, // Define se a animação deve ser reproduzida em loop
    autoplay: true, // Define se a animação deve começar automaticamente
    path: 'assets/image/programer.json' // Caminho para o arquivo JSON da animação
  });

  const containertwo = document.getElementById('animation-two');
  
  // Configurações da animação (substitua 'nome-do-arquivo.json' pelo nome do seu arquivo Lottie)
  const animacaotwo = lottie.loadAnimation({
    container: containertwo,
    renderer: 'svg', // ou 'canvas' ou 'html'
    loop: true, // Define se a animação deve ser reproduzida em loop
    autoplay: true, // Define se a animação deve começar automaticamente
    path: 'assets/image/seta.json' // Caminho para o arquivo JSON da animação
  });
  
