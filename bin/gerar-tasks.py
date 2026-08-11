#!/usr/bin/env python3
import os
import sys

STATES = ["normal", "hover", "focus", "minimized", "attention", "progress"]
FAMILIES = ["", "east-", "north-", "west-"]
PARTS = ["center", "top", "bottom", "left", "right",
         "topleft", "topright", "bottomleft", "bottomright"]

LINE_HEIGHT = 1.5
BOX_WIDTH = 8
LINE_WIDTH = 4

OPACITY = {
    "focus": 1.0,
    "hover": 0.6,
    "normal": 0.35,
    "minimized": 0.25,
    "attention": 0.85,
}

SIZE = {
    "center": (BOX_WIDTH, 8),
    "top": (BOX_WIDTH, 1),
    "bottom": (BOX_WIDTH, LINE_HEIGHT),
    "left": (1, 8),
    "right": (1, 8),
    "topleft": (1, 1),
    "topright": (1, 1),
    "bottomleft": (1, LINE_HEIGHT),
    "bottomright": (1, LINE_HEIGHT),
}


def build():
    elements = []
    y = 0

    for family in FAMILIES:
        for state in STATES:
            x = 0

            for part in PARTS:
                width, height = SIZE[part]
                color_class = "ColorScheme-NegativeText" if state == "attention" else "ColorScheme-Text"
                box = f'<rect x="{x}" y="{y}" width="{width}" height="{height}" opacity="0"/>'

                if part == "bottom" and state in OPACITY:
                    line_x = x + (BOX_WIDTH - LINE_WIDTH) / 2
                    box += (f'<rect x="{line_x}" y="{y}" width="{LINE_WIDTH}" '
                            f'height="{height}" opacity="{OPACITY[state]}"/>')

                elements.append(
                    f'<g id="{family}{state}-{part}" class="{color_class}" '
                    f'fill="currentColor">{box}</g>'
                )
                x += width + 4

            y += 14

    elements.append(
        f'<g id="hint-stretch-borders">'
        f'<rect x="0" y="{y + 4}" width="1" height="1" opacity="0"/></g>'
    )

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="200" height="{y + 12}" version="1.1">
<defs id="current-color-scheme">
<style type="text/css">
.ColorScheme-Text {{ color:#eff0f1; }}
.ColorScheme-Background {{ color:#31363b; }}
.ColorScheme-Highlight {{ color:#3daee9; }}
.ColorScheme-NegativeText {{ color:#da4453; }}
.ColorScheme-ButtonFocus {{ color:#3daee9; }}
</style>
</defs>
{chr(10).join(elements)}
</svg>
'''


if __name__ == "__main__":
    default = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "desktoptheme/plasma-jui/widgets/tasks.svg",
    )
    destination = sys.argv[1] if len(sys.argv) > 1 else default

    os.makedirs(os.path.dirname(destination), exist_ok=True)
    open(destination, "w").write(build())

    print(f"tasks.svg gravado em {destination}")
