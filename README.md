# plasma-jui

Tema preto e escala de cinza para o KDE Plasma 6, com painel mínimo e barra de tarefas sem fundo.

Feito e testado no CachyOS com Plasma 6.7 no Wayland.

## O que ele faz

**Esquema de cores `PlasmaJui`** — derivado do Breeze Dark. Cada cor virou cinza puro por luminância; nenhum azul, verde ou vermelho sobrou na interface. Os fundos foram redesenhados numa escala preta:

| Elemento | Cor |
| --- | --- |
| Janelas | `#121212` |
| Listas e campos | `#0a0a0a` |
| Botões | `#202020` |
| Barras de título | `#181818` |
| Seleção | `#464646` |

**Estilo do Plasma `plasma-jui`** — só troca o desenho da barra de tarefas. O fundo atrás de cada ícone sai. No lugar entra uma linha curta embaixo do ícone, com metade da largura dele:

| Estado do app | Linha |
| --- | --- |
| Fechado (só lançador) | nenhuma |
| Minimizado | 25% |
| Aberto | 35% |
| Sob o mouse | 60% |
| Focado | 100% |
| Pedindo atenção | vermelha, 85% |

**Painel** — embaixo, flutuante, 30px, escondido automaticamente. Sem pager, sem espaçadores e sem "mostrar área de trabalho". A bandeja fica com volume, rede, bluetooth e notificações; o resto vai para o menu escondido.

**Resposta** — animações instantâneas (`AnimationDurationFactor=0`) e bordas de tela sem atraso.

**Ícones** — Papirus Dark.

## Instalar

```sh
git clone https://github.com/juicerq/plasma-jui.git
cd plasma-jui
./install.sh
```

O script pede `sudo` uma vez, para instalar o `papirus-icon-theme`. Ele reinicia o `plasmashell` no meio do caminho — sua sessão continua, só o painel pisca.

## Ajustar

A linha da barra de tarefas é gerada por script. Para mudar espessura, largura ou opacidade, edite as constantes no topo de `bin/gerar-tasks.py` e rode:

```sh
python3 bin/gerar-tasks.py
./install.sh
```

`LINE_HEIGHT` é a espessura, `LINE_WIDTH` de `BOX_WIDTH` é a fração da largura do ícone, e `OPACITY` guarda um valor por estado.

## Desfazer

```sh
plasma-apply-colorscheme BreezeDark
plasma-apply-desktoptheme breeze-dark
/usr/lib/plasma-changeicons breeze-dark
kwriteconfig6 --file kdeglobals --group KDE --key AnimationDurationFactor 1
```

O painel volta pelo botão direito nele → Configurar painel.

## Notas

O `plasma-org.kde.plasma.desktop-appletsrc` **não** é versionado. Ele guarda IDs de tela, UUID de atividade e a lista dos seus apps fixados — copiar esse arquivo entre máquinas quebra o painel. Por isso o `install.sh` recria o painel por comando.

Dois detalhes de acabamento que não têm saída por configuração no Plasma 6.7:

- O atraso para o painel escondido sumir é fixo em torno de 500ms, dentro do `plasmashell`. Não depende da velocidade de animação. É o [bug 267277](https://bugs.kde.org/show_bug.cgi?id=267277), aberto desde 2011.
- O clareamento do ícone sob o mouse vem do QML compilado da barra de tarefas. Dá para atenuá-lo escurecendo `DecorationHover` no esquema de cores — aqui ele está em `#404040`. Desligar de vez, não dá.
