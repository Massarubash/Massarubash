# Ferramentas do MASSARU

Toda imagem em `assets/` é **gerada** pelos scripts desta pasta. Assim você muda cores, textos ou layout
e reconstrói tudo, em vez de editar arquivo por arquivo. Nada aqui roda no GitHub: rode no seu computador e faça o commit do resultado.

## Preparação

```bash
python3 -m pip install -r tools/requirements.txt   # pillow + numpy
python3 tools/build-all.py                         # regenera, otimiza e verifica (cerca de um minuto por causa do GIF)
python3 tools/build-all.py --no-gif                # igual, mas pula o GIF de pintura
```

## O que cada script faz

| Script | Grava em | O que faz |
|---|---|---|
| `graffiti.py` | - | Motor das letras de rua (alfabeto angular, inclinado e tremido), paleta (`PAL`), cena e renderizadores de SVG e GIF |
| `street.py` | - | Elementos de rua: concreto, lambe-lambe, pichação abstrata, setas wildstyle, spray, meio-tom, fita, estêncil e a cena do banner principal |
| `generate-banners.py` | `assets/banners/`, `assets/headers/` | Banner 01 (MASSARU, arte final estática), banners 02-04 (Sobre mim, Habilidades, Instagram + Twitch), 3 painéis de pichação/wildstyle/tag **sem texto** e os cabeçalhos. Tudo, menos o banner 01, se pinta sozinho em loop |
| `generate-dividers.py` | `assets/dividers/` | Sete divisores diferentes (traço de spray, lambe-lambe rasgado, rabisco cursivo, barra de tinta, setas wildstyle, fita de alerta, marcas de tag) com fundo transparente |
| `generate-icons.py` | `assets/icons/`, `assets/social/`, `assets/illustrations/`, `assets/backgrounds/` | Etiquetas de tecnologias, etiquetas das informações pessoais, botões de redes sociais, cards de interesses em estêncil e parede do rodapé |
| `generate-animations.py` | `assets/animations/` | `massaru-painting.gif` (banner principal), tagline animada, tinta escorrendo, spray pintando |
| `optimize-assets.py` | tudo em `assets/` | Minifica os SVGs, otimiza GIFs e avisa quando um arquivo passa do limite de tamanho |
| `verify-assets.py` | - | Confere se todo arquivo usado no `README.md` existe, se os SVG/GIF são válidos e lista o que não está sendo usado |
| `preview-assets.py` | qualquer pasta | Opcional: renderiza SVGs em PNG com Chromium (`pip install playwright`) para você conferir visualmente |
| `build-all.py` | - | Roda tudo acima na ordem certa |

## Edições comuns

**Redes sociais**: a seção tem só Instagram (`@massdvv_`) e Twitch (`@massadv_`), já configurados.
Os links ficam no `README.md` (procure por `instagram.com` e `twitch.tv`) e o texto dos botões fica em `SOCIAL` dentro de `generate-icons.py`.

**Adicionar, remover ou renomear uma tecnologia**
1. Edite a lista `TECH` em `generate-icons.py` (`slug`, texto, nome da cor de `PAL`).
2. Rode `python3 tools/generate-icons.py`.
3. Adicione ou remova a linha `<img src="assets/icons/tech-<slug>.svg">` correspondente no `README.md`.

**Mudar os textos das etiquetas de informações pessoais**: edite `LABELS` em `generate-icons.py` e depois a tabela no `README.md`.

**Mudar as cores**: edite `PAL` em `graffiti.py` (toda a identidade se atualiza na próxima build).

**Mudar as letras principais**: `MAIN` (texto, posição, tamanho, inclinação) e `STYLE_MAIN` (cores, contorno, bloco 3D, `rough` = quanto a borda é destruída) em `street.py`.
O banner estático e o GIF de pintura leem os mesmos valores, então sempre ficam iguais.

**Mudar velocidade e estilo das animações**
- Banners SVG: `T` (duração do loop em segundos) no começo de cada função de banner em `generate-banners.py`.
- Ordem das etapas (spray, contorno, preenchimento, brilho, gotas, detalhes): `STAGES` em `graffiti.py`.
- GIF: `GIF_SIZE` e `GIF_FRAMES` em `generate-animations.py`.

**Textos dentro das imagens**: ficam nos scripts de geração (por exemplo `'SOBRE MIM'` em `generate-banners.py`).
O alfabeto já tem acentos (Á É Í Ó Ú Ã Õ Â Ê Ô Ç). O tremido de cada letra é calculado por `wobble` em `layout()` (0 = letras limpas).
Para acrescentar uma letra ou símbolo, adicione um traço (comandos absolutos `M L C Q`, numa caixa de cerca de 100x120) em `GLYPHS` no `graffiti.py`.

## Como as animações funcionam (e por que funcionam no GitHub)

O README do GitHub não executa JavaScript nem CSS da página, e mostra SVGs por meio de tags `<img>`. Por isso os SVGs usam
**SMIL** (`<animate>`) dentro do próprio arquivo, que os navegadores tocam mesmo dentro de `<img>`. O banner principal é um **GIF**
de verdade, por ser o formato mais compatível (app de celular, prévias de e-mail e links). Os SVGs não carregam nada externo
e não usam fontes: todas as letras são desenhadas como traços, então ficam iguais em qualquer dispositivo.

Limite de tamanho: SVG até cerca de 200 KB, GIF até 2 MB. O `optimize-assets.py` avisa quando passa.

## Mapa de pastas

```
assets/
  banners/        4 banners + 3 painéis de pichação sem texto
  headers/        cabeçalhos de seção + assinatura (rabisco, sem repetir o nome)
  dividers/       7 divisores de seção
  animations/     GIF de pintura, tagline, tinta escorrendo, spray pintando
  social/         botões de redes sociais
  icons/          etiquetas de tecnologias e de informações pessoais
  illustrations/  cards de interesses (estêncil)
  backgrounds/    parede de concreto do rodapé
tools/            geradores, otimizador, verificador
```
