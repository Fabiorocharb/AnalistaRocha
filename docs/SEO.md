# SEO e publicação

O SEO técnico está preparado para a URL
`https://fabiorocharb.github.io/AnalistaRocha/`.
O layout, o CSS, as animações e os textos visíveis foram preservados nesta revisão.

## O que foi ajustado

- Título e descrição específicos sobre criação de sites personalizados.
- URL canônica única, compartilhada pelo HTML, Open Graph e sitemap.
- Links dos logotipos apontando para a pasta inicial, sem acrescentar `index.html`.
- Dados estruturados em JSON-LD para Fábio Rocha, o site, a página e o serviço.
  As informações correspondem ao conteúdo existente; não foram incluídos
  avaliações, endereço, preços ou qualificações não confirmados.
- Metadados Open Graph e Twitter, com uma prévia PNG de 1200 × 630 pixels,
  produzida a partir do logotipo existente. Essa imagem é usada ao compartilhar
  o link e não aparece no layout da página.
- Descrições alternativas mais específicas para as imagens do portfólio.
- Remoção de cópias de imagens embutidas em definições SVG sem uso. Os sete
  SVGs passaram de 12.487.513 para 6.547.181 bytes, redução de 47,6%, sem
  recompressão dos pixels. Esses valores são tamanhos dos arquivos, não uma
  medição de tempo de carregamento ou de tráfego comprimido.
- `sitemap.xml` com a URL da página. As âncoras de seção não são páginas separadas.
- `.nojekyll` para manter a publicação como arquivos estáticos no GitHub Pages.

## Após enviar as alterações ao GitHub

Validação local realizada nesta revisão: 13 testes passaram. As capturas de
390, 768, 1366 e 1920 pixels ficaram idênticas antes e depois, controlando a
aleatoriedade das animações somente no navegador de teste. A renderização
individual dos sete SVGs também apresentou pixels idênticos aos originais.
Isso verifica a preservação visual; não representa uma nota do Google.

1. Confira se a publicação terminou com sucesso na aba **Actions**.
2. Abra `https://fabiorocharb.github.io/AnalistaRocha/sitemap.xml` e confirme
   que ele está disponível. A imagem `assets/image/compartilhamento.png`
   também precisa ser enviada.
3. No [Google Search Console](https://search.google.com/search-console/),
   adicione ou selecione a propriedade com prefixo de URL
   `https://fabiorocharb.github.io/AnalistaRocha/`. Confirme a propriedade pelo
   método que o Google disponibilizar. Nenhum código de verificação foi inventado
   ou adicionado ao projeto.
4. Em **Sitemaps**, envie `sitemap.xml`. Em **Inspeção de URL**, teste a URL
   inicial publicada e solicite a indexação se necessário.
5. Avalie o endereço publicado no [PageSpeed Insights](https://pagespeed.web.dev/)
   e acompanhe indexação, consultas e desempenho pelo Search Console.

Não foi feita uma solicitação de indexação nem uma medição de Core Web Vitals
durante esta revisão. A confirmação de propriedade exige acesso à sua conta.
Dados estruturados e sitemap não garantem indexação, posição ou resultados
enriquecidos. `Service` descreve o serviço, sem prometer um resultado especial.
O recurso de nome de site do Google não é suportado no nível de subpasta;
o JSON-LD `WebSite` continua descrevendo o site, sem garantir um nome exclusivo
nos resultados para este endereço do GitHub Pages.

## Por que não há um robots.txt nesta pasta

O Google procura esse arquivo na raiz do host:
`https://fabiorocharb.github.io/robots.txt`.
Um arquivo em `/AnalistaRocha/robots.txt` não configuraria o rastreamento do site.
Não é necessário criar um arquivo apenas para permitir acesso. Se futuramente
for necessário controlar o rastreamento, configure a raiz do host, normalmente
no repositório `Fabiorocharb.github.io`, considerando também os outros projetos
publicados nesse mesmo domínio.

## Manutenção

- Se adotar um domínio próprio, atualize a URL em `index.html`, `sitemap.xml`
  e `tests/test_seo.py`. Ajuste também a propriedade no Search Console.
- Se alterar os serviços ou o nome profissional, atualize os metadados e os
  dados estruturados para continuarem coerentes com o conteúdo visível.
- `python scripts/optimize_svg.py` reaplica a remoção conservadora de definições
  de imagens sem uso. O comando é idempotente; compare a aparência se substituir
  os SVGs por novos arquivos.
- `python -m unittest discover -s tests -v` verifica os metadados, os recursos
  locais e os controles do site. Os testes de navegador precisam de Playwright
  e Google Chrome; o teste das animações reais usa a internet.

## Referências

- [Títulos no Google](https://developers.google.com/search/docs/appearance/title-link)
- [Descrições nos resultados](https://developers.google.com/search/docs/appearance/snippet)
- [URL canônica](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
- [Diretrizes de dados estruturados](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)
- [Sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview)
- [Localização do robots.txt](https://developers.google.com/crawling/docs/robots-txt/create-robots-txt)
- [Nome do site e subpastas](https://developers.google.com/search/docs/appearance/site-names)
