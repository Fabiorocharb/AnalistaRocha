

> ****Status do projeto****: **Concluído✅**

## Executar localmente

Na pasta do projeto, execute `python -m http.server 8000 --bind 127.0.0.1`
e abra http://127.0.0.1:8000. Use um servidor HTTP para carregar os arquivos
JSON das animações; abrir o HTML por `file://` pode bloquear essas requisições.
O site continua estático, sem etapa de compilação.

## Revisão de responsividade — setembro de 2026

- Layout com largura máxima, colunas flexíveis e cartões que crescem com o texto.
- Menu acessível por teclado, com fechamento por link, clique fora e Esc.
- Carrossel com rolagem nativa, botões e indicadores sincronizados, sem jQuery/Slick.
- Ícones alternativos quando o Lottie não carrega e ilustrações estáticas para
  visitantes que preferem movimento reduzido.
- Dimensões reservadas para as imagens, foco visível e links externos protegidos
  com `rel="noopener noreferrer"`.
- Ano do rodapé atualizado automaticamente.

O formulário prepara uma mensagem com nome, email e texto e abre o WhatsApp.
**O visitante confirma o envio no WhatsApp.** Não existe envio de email nem
armazenamento no site. O número utilizado vem do link `#contact-whatsapp` no HTML;
altere esse link se seu contato mudar. Ao abrir o WhatsApp, os campos são limpos
e a página é recarregada. Se o navegador bloquear a nova janela, os dados são
mantidos e um link permite tentar abrir a mensagem preparada. Sem JavaScript, o contato direto
pelos ícones continua disponível.

## Testes de regressão

O SEO técnico, a otimização dos SVGs e os passos de publicação e indexação estão
documentados em [docs/SEO.md](docs/SEO.md). A revisão de SEO preserva o visual
e os textos exibidos na página.

Requer Python, Google Chrome e Playwright:

```sh
python -m pip install playwright
python -m unittest discover -s tests -v
```

Os testes iniciam e encerram um servidor local automaticamente. Verificam
larguras de 320 a 2560 pixels, orientação horizontal, texto a 200%, menu,
carrossel, validação e preparação do contato, ausência de JavaScript e falhas
de CDN. A abertura do WhatsApp é interceptada: nenhuma mensagem é enviada.
O teste de animações reais requer internet. Para salvar capturas de tela,
defina a variável de ambiente `SITE_SCREENSHOT_DIR` com uma pasta de destino.

As verificações automatizadas usam Chrome; Safari e Firefox ainda precisam
de validação específica. As imagens, textos biográficos e destinos externos
do portfólio foram preservados.

<h2> 🎯 Objetivo do projeto:</h2>

**Criar um site que sirva de portifolio e freelancer**

<img src="https://img.shields.io/bower/l/html?style=flat-square"/>

<h2>🎥 image da página: </h2>

![imageanalista](https://github.com/Fabiorocharb/AnalistaRocha/assets/106245486/4e40a09d-904d-4a1a-a2d9-692446e02e06)


<h2>🔗 Link do site: </h2>
https://fabiorocharb.github.io/AnalistaRocha/

<h2>🧰 Site e extensão utilizado:</h2>

<p>✅ https://responsiveviewer.org/ </p>
<p>✅ ResponsivelyApp </p>
<p>✅ Checkbot: SEO,Web Speed and Security Tester - Extensão do Google </p>


<h2>👨‍💻 Tecnologias usadas :</h2>
<div>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original-wordmark.svg" width="6%" />
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original-wordmark.svg" width="6%" />
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original-wordmark.svg" width="6%"/>          
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" width="6%"/>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/canva/canva-original.svg" width="6%"/>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/visualstudio/visualstudio-plain-wordmark.svg" width="10%"/>
          
          
</div>

<h2>📮 Rede social e contatos: </h2>

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/fabiorocharb)
[![Github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Fabiorocharb/Fabiorocharb)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://instagram.com/analistarocha)


