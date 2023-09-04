const btnMobile = document.getElementById("btn-mobile");

function toggleMenu(event) {
  if (event.type === "touchstart") event.preventDefault();
  const menu = document.getElementById("menu");
  menu.classList.toggle("active");
  const active = menu.classList.contains("active");
  event.currentTarget.setAttribute("aria-expanded", active);
  if (active) {
    event.currentTarget.setAttribute("aria-label", "Fechar Menu");
  } else {
    event.currentTarget.setAttribute("aria-label", "Abrir Menu");
  }
}
btnMobile.addEventListener("click", toggleMenu);
btnMobile.addEventListener("touchstart", toggleMenu);

const container = document.getElementById("animation-prog");

// Configurações da animação (substitua 'nome-do-arquivo.json' pelo nome do seu arquivo Lottie)
const animacao = lottie.loadAnimation({
  container: container,
  renderer: "svg",
  loop: true, // Define se a animação deve ser reproduzida em loop
  autoplay: true, // Define se a animação deve começar automaticamente
  path: "assets/image/programer.json", // Caminho para o arquivo JSON da animação
});

const containertwo = document.getElementById("animation-seta");
const animacaotwo = lottie.loadAnimation({
  container: containertwo,
  renderer: "svg",
  loop: true,
  autoplay: true,
  path: "assets/image/seta.json",
});

const containerthree = document.getElementById("animation-seo");

const animacaothree = lottie.loadAnimation({
  container: containerthree,
  renderer: "svg",
  loop: true,
  autoplay: true,
  path: "assets/image/seo.json",
});

const containerfour = document.getElementById("animation-responsible");
const animacaofour = lottie.loadAnimation({
  container: containerfour,
  renderer: "svg",
  loop: true,
  autoplay: true,
  path: "assets/image/responsible.json",
});

const uiux = document.getElementById("animation-uxui");
const animacaosix = lottie.loadAnimation({
  container: uiux,
  renderer: "svg",
  loop: true,
  autoplay: true,
  path: "assets/image/uiux.json",
});

const rowss = document.getElementById("setatwo");
const animacaoseven = lottie.loadAnimation({
  container: setatwo,
  renderer: "svg",
  loop: true,
  autoplay: true,
  path: "assets/image/seta.json",
});

const rowsss = document.getElementById("setasix");
const animacaoeight = lottie.loadAnimation({
  container: setasix,
  renderer: "svg",
  loop: true,
  autoplay: true,
  path: "assets/image/seta.json",
});

const rowssss = document.getElementById("setaseven");
const animacaonine = lottie.loadAnimation({
  container: setaseven,
  renderer: "svg",
  loop: true,
  autoplay: true,
  path: "assets/image/seta.json",
});

$(document).ready(function(){
  const $carousel = $('.carousel');
  const $dots = $('.dot');

  // Verifique se é um dispositivo móvel antes de ativar o carrossel
  if ($(window).width() <= 768) {
    $carousel.slick({
      dots: false,
      infinite: true,
      speed: 300,
      slidesToShow: 1,
      slidesToScroll: 1,
      adaptiveHeight: true// Mantém a altura consistente para projetos de diferentes tamanhos
    });
  }
  $(document).ready(function() {
    // Seletor para o botão "previous"
    const $prevButton = $('.slick-prev');
  
    // Seletor para o botão "next"
    const $nextButton = $('.slick-next');
  
    // Defina o novo texto para o botão "previous" (anterior)
    $prevButton.text('Anterior');
  
    // Defina o novo texto para o botão "next" (próximo)
    $nextButton.text('Próximo');
  });
  
  // Adicione um evento de clique às bolas indicadoras para dispositivos móveis
  $dots.on('click', function() {
    const slideIndex = $(this).data('slide');
    $carousel.slick('slickGoTo', slideIndex);
  });
});




