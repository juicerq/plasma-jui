#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SHARE="$HOME/.local/share"

if ! pacman -Q papirus-icon-theme >/dev/null 2>&1; then
	echo "==> instalando papirus-icon-theme"
	sudo pacman -S --noconfirm papirus-icon-theme
fi

echo "==> copiando esquema de cores e estilo do Plasma"
mkdir -p "$SHARE/color-schemes" "$SHARE/plasma/desktoptheme"
cp "$REPO/color-schemes/PlasmaJui.colors" "$SHARE/color-schemes/"
rm -rf "$SHARE/plasma/desktoptheme/plasma-jui"
cp -r "$REPO/desktoptheme/plasma-jui" "$SHARE/plasma/desktoptheme/"

echo "==> parando plasmashell"
kquitapp6 plasmashell 2>/dev/null || true
sleep 2

echo "==> limpando a bandeja do sistema"
python3 "$REPO/bin/limpar-bandeja.py"

echo "==> ajustando animacoes e bordas de tela"
kwriteconfig6 --file kdeglobals --group KDE --key AnimationDurationFactor 0
kwriteconfig6 --file kdeglobals --group General --key accentColorFromWallpaper false
kwriteconfig6 --file kwinrc --group ScreenEdges --key TimeThreshold 0
kwriteconfig6 --file kwinrc --group ScreenEdges --key ReActivationThreshold 0
qdbus6 org.kde.KWin /KWin reconfigure

echo "==> movendo as notificacoes para o topo"
kwriteconfig6 --file plasmanotifyrc --group Notifications --key PopupPosition TopCenter

echo "==> iniciando plasmashell"
setsid plasmashell >/dev/null 2>&1 </dev/null &
sleep 7

echo "==> aplicando tema"
plasma-apply-colorscheme PlasmaJui
plasma-apply-desktoptheme plasma-jui
/usr/lib/plasma-changeicons Papirus-Dark

echo "==> montando o painel"
qdbus6 org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript '
panels().forEach(function (panel) {
	panel.widgets().forEach(function (widget) {
		if (widget.type == "org.kde.plasma.pager"
			|| widget.type == "org.kde.plasma.marginsseparator"
			|| widget.type == "org.kde.plasma.panelspacer"
			|| widget.type == "org.kde.plasma.showdesktop") {
			widget.remove();
		}
	});

	panel.location = "bottom";
	panel.lengthMode = "fit";
	panel.floating = true;
	panel.hiding = "autohide";
	panel.height = 30;
});
'

echo "==> pronto"
