#!/usr/bin/env python3
import os
import re
import sys

CONFIG = os.path.expanduser("~/.config/plasma-org.kde.plasma.desktop-appletsrc")

HIDDEN = [
    "org.kde.plasma.brightness",
    "org.kde.kscreen",
    "org.kde.plasma.mediacontroller",
    "org.kde.plasma.clipboard",
    "org.kde.plasma.cameraindicator",
    "org.kde.plasma.devicenotifier",
    "org.kde.plasma.keyboardlayout",
    "org.kde.plasma.manage-inputmethod",
    "org.kde.kdeconnect",
    "org.kde.plasma.keyboardindicator",
    "org.kde.plasma.weather",
]


def systray_sections(lines):
    section = None
    found = {}

    for index, line in enumerate(lines):
        header = re.match(r"^\[(.+)\]$", line)

        if header:
            section = header.group(1)
            continue

        if line.startswith("knownItems=") and section:
            found[section] = index

    return found


def main():
    if not os.path.exists(CONFIG):
        sys.exit(f"config nao encontrada: {CONFIG}")

    lines = open(CONFIG).read().splitlines()
    sections = systray_sections(lines)

    if not sections:
        sys.exit("nenhuma bandeja do sistema encontrada")

    hidden_line = "hiddenItems=" + ",".join(HIDDEN)
    changed = 0

    for section, known_index in sections.items():
        start = known_index

        while start > 0 and not lines[start].startswith("["):
            start -= 1

        end = start + 1

        while end < len(lines) and not lines[end].startswith("["):
            end += 1

        target = next(
            (i for i in range(start, end) if lines[i].startswith("hiddenItems=")),
            None,
        )

        if target is None:
            lines.insert(known_index, hidden_line)
        else:
            lines[target] = hidden_line

        changed += 1

    open(CONFIG, "w").write("\n".join(lines) + "\n")
    print(f"bandeja limpa em {changed} secao(oes)")


if __name__ == "__main__":
    main()
